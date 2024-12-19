#!/usr/bin/env python3
'''
run_vehicles.launch.py

Runs specified number of vehicles in simulation with controller.
'''
from ros2_utils.launch_manager import LaunchManager
from launch_ros.actions.node import Node
from ament_index_python.packages import get_package_share_directory
from ros2_utils.launch import combine_names
from robot_control.launch.run_vehicles import get_team
import os


def launch_setup(args):
    lm = LaunchManager()
    lm.add_include_launch_description("robot_control", "run_vehicles.launch.py")

    team = get_team(args, args.context)
    log_level = args.log_level.upper()
    tf_processor_args = []
    for namespace, vehicle_args in team.items():
        commander_node = combine_names([namespace, "commander"], ".")
        lm.add_action(
            Node(package="robot_command", executable="commander",
                namespace=namespace, output="screen",
                arguments=[
                    "--ros-args", "--log-level", f"{commander_node}:={log_level}"
                ])
        )
        if "tf_processor" in vehicle_args and isinstance(vehicle_args["tf_processor"], dict) and vehicle_args["tf_processor"]:
            for k, v in vehicle_args["tf_processor"].items():
                if not k.startswith("/"): tf_processor_args += ["--tf-pair", f"{namespace}/{k},{v}"]
        # if vehicle_args["use_darknet"]:
        #     launch_arguments=[
        #         ('namespace', namespace),
        #         ('output', 'log'),
        #     ]
        #     lm.add_include_launch_description("robot_bringup", "darknet_ros.launch.py", launch_arguments)
    if tf_processor_args:
        tf_processor_node = combine_names(["tf_processor"], ".")
        tf_processor_args += ["--ros-args", "--log-level", f"{tf_processor_node}:={log_level}",]
        lm.add_action(
            Node(package="robot_command", executable="tf_processor",
            output="screen",
            arguments=tf_processor_args),
        )
    if args.use_control_center:
        lm.add_action(
            Node(package="robot_command", executable="control_center",
            namespace="hq",
            output="screen"),
        )
    return lm.describe_sub_entities()


# https://github.com/colcon/colcon-core/issues/169
def generate_launch_description():
    lm = LaunchManager()
    lm.add_arg("use_darknet", "False", "Flag for turning on darknet nodes and capabilities on single drone.")
    lm.add_arg("use_control_center", "False", "Flag for turning on control center capabilities.")
    lm.add_include_launch_args("robot_control", "run_vehicles.launch.py")
    # lm.add_include_launch_args("robot_bringup", "darknet_ros.launch.py")
    lm.add_opaque_function(launch_setup, yaml_file=os.environ.get("ROBOT_CONTROL_CONFIG", ""))
    return lm

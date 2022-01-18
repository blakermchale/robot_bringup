#!/usr/bin/env python3
from enum import IntEnum
import os
from ament_index_python.packages import get_package_share_directory
from robot_control.launch.environment import LAUNCH_ARGS
from ros2_utils.launch import get_local_arguments, combine_names
from robot_control.launch.run_vehicles import LAUNCH_ARGS as R_LAUNCH_ARGS, launch_setup as r_launch_setup, extract_namespaces, get_team, SPAWN_LAUNCH_ARGS
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions.node import Node


ROBOT_COMMAND_PKG = get_package_share_directory("robot_command")
ROBOT_BRINGUP_PKG = get_package_share_directory("robot_bringup")


VEHICLE_LAUNCH_ARGS = [
    {"name": "use_darknet",     "default": "false",      "description": "Flag for turning on darknet nodes and capabilities on single drone.",
        "type": "bool"},
]
LAUNCH_ARGS = [
    # {"name": ""}
]
LAUNCH_ARGS += VEHICLE_LAUNCH_ARGS
LAUNCH_ARGS += R_LAUNCH_ARGS
VEHICLE_LAUNCH_ARGS += SPAWN_LAUNCH_ARGS


def launch_setup(context, *args, **kwargs):
    """Allows declaration of launch arguments within the ROS2 context
    """
    ld = r_launch_setup(context, args, kwargs)
    largs = get_local_arguments(LAUNCH_ARGS, context, yaml_file=os.environ["ROBOT_CONTROL_CONFIG"])
    team = get_team(largs, context, default_team_args=VEHICLE_LAUNCH_ARGS)
    log_level = largs["log_level"].upper()
    tf_processor_args = []
    for namespace, vehicle_args in team.items():
        commander_node = combine_names([namespace, "commander"], ".")
        ld += [
            Node(package="robot_command", executable="commander",
                namespace=namespace, output="screen",
                arguments=[
                    "--ros-args", "--log-level", f"{commander_node}:={log_level}"
                ]),
        ]
        if "tf_processor" in vehicle_args and isinstance(vehicle_args["tf_processor"], dict) and vehicle_args["tf_processor"]:
            for k, v in vehicle_args["tf_processor"].items():
                if not k.startswith("/"): tf_processor_args += ["--tf-pair", f"{namespace}/{k},{v}"]
        if vehicle_args["use_darknet"]:
            ld += [
                IncludeLaunchDescription(
                    PythonLaunchDescriptionSource(
                        [ROBOT_BRINGUP_PKG, os.path.sep, 'launch',
                            os.path.sep, 'darknet_ros.launch.py']
                    ),
                    launch_arguments=[
                        ('namespace', namespace),
                        ('output', 'log'),
                    ],
                )
            ]
    if tf_processor_args:
        tf_processor_node = combine_names(["tf_processor"], ".")
        tf_processor_args += ["--ros-args", "--log-level", f"{tf_processor_node}:={log_level}",]
        ld += [
            Node(package="robot_command", executable="tf_processor",
            output="screen",
            arguments=tf_processor_args),
        ]
    return ld

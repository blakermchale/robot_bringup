#!/usr/bin/env python3
'''
darknet_ros.launch.py

Runs specified number of vehicles in simulation with controller.
'''
from ros2_utils.launch_manager import LaunchManager
from launch_ros.actions.node import Node
import os
from ament_index_python.packages import get_package_share_directory


# darknet_ros_share = get_package_share_directory("darknet_ros")
# robot_bringup_share = get_package_share_directory("robot_bringup")
darknet_ros_share = ""
robot_bringup_share = ""

YOLO_MAIN_PATH = os.path.join(darknet_ros_share,"yolo_network_config")
YOLO_WEIGHTS_DEFAULT = os.path.join(YOLO_MAIN_PATH,"weights")
YOLO_CONFIG_DEFAULT = os.path.join(YOLO_MAIN_PATH,"cfg")
ROS_PARAM_DEFAULT = os.path.join(robot_bringup_share,"config","darknet_ros.yaml")
NETWORK_PARAM_DEFAULT = os.path.join(darknet_ros_share,"config","yolov4-tiny.yaml")


def launch_setup(args):
    lm = LaunchManager()
    ns = ""
    if args.namespace:
        ns = f"/{args.namespace}"
    # lm.add_action(
    #     Node(
    #         namespace=f'{args.namespace}/darknet_ros',
    #         package='darknet_ros',
    #         executable='darknet_ros',
    #         name='darknet_ros',
    #         output=args.output,
    #         parameters=[args.ros_param_file, args.network_param_file,
    #         {
    #             "config_path": args.yolo_config_path, 
    #             "weights_path": args.yolo_weights_path,
    #         },
    #         ],
    #         # arguments=[
    #         #             "--ros-args", "--log-level", f"darknet_ros:=DEBUG"
    #         # ],
    #         remappings=[
    #             ("/camera/image_raw", f"{ns}/realsense/color/image_raw"),
    #             ("/darknet_ros/bounding_boxes", f"{ns}/darknet_ros/bounding_boxes"),
    #             ("/darknet_ros/detection_image", f"{ns}/darknet_ros/detection_image"),
    #             ("/darknet_ros/found_object", f"{ns}/darknet_ros/found_object")
    #         ]
    #     )
    # )
    lm.add_action(
        Node(
            namespace=args.namespace,
            package="cv_ros",
            executable="create_bb_tf",
            output=args.output,
        )
    )
    return lm.describe_sub_entities()


def generate_launch_description():   
    lm = LaunchManager()
    lm.add_arg("yolo_weights_path", YOLO_WEIGHTS_DEFAULT, "Path to YOLO weights.")
    lm.add_arg("yolo_config_path", YOLO_CONFIG_DEFAULT, "Path to YOLO config.")
    lm.add_arg("ros_param_file", ROS_PARAM_DEFAULT, "Path to ROS params.")
    lm.add_arg("network_param_file", NETWORK_PARAM_DEFAULT, "Path to network params.")
    lm.add_arg("namespace", "drone_0", "Namespace of node.")
    lm.add_arg("output", "screen", "Where to output darknet and bb tf creation.")
    lm.add_opaque_function(launch_setup)
    return lm

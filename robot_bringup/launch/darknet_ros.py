#!/usr/bin/env python3
import os
from ament_index_python.packages import get_package_share_directory
from ros2_utils.launch import get_local_arguments
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions.node import Node


darknet_ros_share = get_package_share_directory("darknet_ros")
robot_bringup_share = get_package_share_directory("robot_bringup")

YOLO_MAIN_PATH = os.path.join(darknet_ros_share,"yolo_network_config")
YOLO_WEIGHTS_DEFAULT = os.path.join(YOLO_MAIN_PATH,"weights")
YOLO_CONFIG_DEFAULT = os.path.join(YOLO_MAIN_PATH,"cfg")
ROS_PARAM_DEFAULT = os.path.join(robot_bringup_share,"config","darknet_ros.yaml")
NETWORK_PARAM_DEFAULT = os.path.join(darknet_ros_share,"config","yolov2-tiny.yaml")
LAUNCH_ARGS = [
    {"name":"yolo_weights_path",       "default":YOLO_WEIGHTS_DEFAULT,        "description":"Path to YOLO weights."},
    {"name":"yolo_config_path",        "default":YOLO_CONFIG_DEFAULT,         "description":"Path to YOLO config."},
    {"name":"ros_param_file",          "default":ROS_PARAM_DEFAULT,           "description":"Path to ROS params."},
    {"name":"network_param_file",      "default":NETWORK_PARAM_DEFAULT,       "description":"Path to network params."},
    {"name":"namespace",               "default":"drone_0",                   "description":"Namespace of node."}
]

def launch_setup(context, *args, **kwargs):
    """Allows declaration of launch arguments within the ROS2 context
    """
    largs = get_local_arguments(LAUNCH_ARGS, context)
    ld = []
    ld += [
        Node(
            namespace=f'{largs["namespace"]}/darknet_ros',
            package='darknet_ros',
            executable='darknet_ros',
            name='darknet_ros',
            output='screen',
            parameters=[largs["ros_param_file"], largs["network_param_file"],
            {
                "config_path": largs["yolo_config_path"], 
                "weights_path": largs["yolo_weights_path"],
            },
            ],
            # arguments=[
            #             "--ros-args", "--log-level", f"darknet_ros:=DEBUG"
            # ],
            remappings=[
                ("/camera/image_raw/compressed", f"/{largs['namespace']}/realsense/color/image_raw/compressed")
            ]
        ),
        Node(
            namespace=f'{largs["namespace"]}',
            package="cv_ros",
            executable="create_bb_tf",
            output="screen",
        )
    ]
    return ld

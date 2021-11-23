#!/usr/bin/env python3
from enum import IntEnum
import os
from ament_index_python.packages import get_package_share_directory
from ros2_utils.launch import get_local_arguments
from robot_control.launch.run_vehicles import LAUNCH_ARGS as R_LAUNCH_ARGS, launch_setup as r_launch_setup, extract_namespaces
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions.node import Node


LAUNCH_ARGS = R_LAUNCH_ARGS

def launch_setup(context, *args, **kwargs):
    """Allows declaration of launch arguments within the ROS2 context
    """
    ld = r_launch_setup(context, args, kwargs)
    largs = get_local_arguments(LAUNCH_ARGS, context)
    # namespaces = extract_namespaces(largs)
    # for i, namespace in enumerate(namespaces):
    #     pass
    return ld

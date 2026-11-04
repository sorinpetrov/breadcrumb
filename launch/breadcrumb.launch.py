import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    params = os.path.join(get_package_share_directory('breadcrumb'), 'config', 'breadcrumb.yaml')
    return LaunchDescription([
        Node(
            package='breadcrumb',
            executable='breadcrumb_node',
            name='breadcrumb',
            parameters=[params],
            remappings=[('odom', '/odometry/filtered')],
            output='screen',
        ),
    ])

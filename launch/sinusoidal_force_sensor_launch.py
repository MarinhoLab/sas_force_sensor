import os.path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    """Launch the example sinusoidal force sensor node.

    Parameters are loaded from a YAML configuration file. Pass a different
    file with ``config_file:=/path/to/config.yaml``.
    """
    name = LaunchConfiguration('name')
    config_file = LaunchConfiguration('config_file')

    return LaunchDescription([
        DeclareLaunchArgument(
            'name',
            default_value='sinusoidal_force_sensor'
        ),
        DeclareLaunchArgument(
            'config_file',
            default_value=os.path.join(get_package_share_directory('sas_force_sensor'), 'config', 'config.yaml')
        ),
        Node(
            package='sas_force_sensor',
            executable='sinusoidal_force_sensor',
            name=name,
            parameters=[config_file]
        )
    ])

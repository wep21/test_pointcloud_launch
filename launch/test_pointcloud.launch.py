# Copyright 2020 Tier IV, Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import yaml

import launch
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import ComposableNodeContainer, LoadComposableNodes
from launch_ros.descriptions import ComposableNode
from launch.substitutions import EnvironmentVariable
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    launch_arguments = []

    def add_launch_arg(name: str, default_value=None):
        launch_arguments.append(DeclareLaunchArgument(name, default_value=default_value))

    publish_component = ComposableNode(
        package='pcd_publisher',
        plugin='PCDPublisher',
        name='pcd_publisher',
        parameters=[{
            'file_name': [launch.substitutions.ThisLaunchFileDir(), '/sample.pcd']
        }],
    )

    def create_relay_component(x):
        return ComposableNode(
            package='topic_tools',
            plugin='topic_tools::RelayNode',
            name='relay' + str(x),
            parameters=[{
                'input_topic': '/output',
                'output_topic': '/output' + str(x),
                'type': 'sensor_msgs/msg/PointCloud2',
                'history': 'keep_last',
                'depth': 5,
                'reliability': 'best_effort',
            }],
        )

    container = ComposableNodeContainer(
        name='test_pointcloud_container',
        namespace='pointcloud_preprocessor',
        package='rclcpp_components',
        executable='component_container',
        composable_node_descriptions=[
            publish_component,
            *list(map(create_relay_component, list(range(0, 10))))
        ],
        output='screen',
    )

    return launch.LaunchDescription([container])

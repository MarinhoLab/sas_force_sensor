#!/usr/bin/python3
"""
# Copyright (c) 2020-2026 Murilo Marques Marinho
#
#    This file is part of sas_force_sensor.
#
#    sas_force_sensor is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    sas_force_sensor is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with sas_force_sensor.  If not, see <https://www.gnu.org/licenses/>.
#
# #######################################################################################
#
#   Author: Murilo M. Marinho, email: murilomarinho@ieee.org
#
# #######################################################################################
"""
import time
from dqrobotics import *  # Despite what PyCharm might say, this is very much necessary or DQs will not be recognized

from sas_common import rclcpp_init, rclcpp_Node, rclcpp_spin_some, rclcpp_shutdown
from sas_force_sensor import ForceSensorServer, ForceSensorClient


def main(args=None):
    try:
        rclcpp_init()
        node = rclcpp_Node("my_test_force_sensor_node")

        # Initialize the ForceSensorServer
        fss = ForceSensorServer(node, 'my_test_force_sensor')

        # Initialize the ForceSensorClient
        fsc = ForceSensorClient(node, 'my_test_force_sensor')

        # Wait for ForceSensorClient to be enabled
        while not fsc.is_enabled():
            rclcpp_spin_some(node)
            time.sleep(0.1)
            # Send a force/torque reading from the ForceSensorServer to the ForceSensorClient
            # ForceSensorClient will be enabled when a reading is received
            fss.send_force_torque(DQ([1, 2, 3]), DQ([4, 5, 6]))

        # Read the values sent by the ForceSensorServer
        print(fsc.get_force())
        print(fsc.get_torque())
        print(fsc.get_topic_prefix())

        rclcpp_shutdown()

    except KeyboardInterrupt:
        print("Interrupted by user")
    except Exception as e:
        print("Unhandled excepts", e)


if __name__ == '__main__':
    main()

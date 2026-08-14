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
# ################################################################
#
#   Author: Murilo M. Marinho, email: murilomarinho@ieee.org
#
# ################################################################
"""
import time
import multiprocessing as mp
import multiprocessing.managers as mm
import numpy as np

from dqrobotics import *  # noqa: F401, F403 - required for DQ type recognition

from sas_common import (
    rclcpp_init,
    rclcpp_Node,
    rclcpp_spin_some,
    rclcpp_shutdown,
)
from sas_force_sensor import ForceSensorClient
from sas_force_sensor.shared_memory.server import ForceSensorSharedMemoryServer


def force_sensor_gui_node(topic_prefix="sas_force_sensor"):
    """
    ROS 2 node that reads force/torque from a ``ForceSensorClient`` and
    publishes the wrench through shared memory so the GUI can consume it.
    """
    rclcpp_init()
    node = rclcpp_Node("sas_force_sensor_gui_node")

    fsc = ForceSensorClient(node, topic_prefix)

    with mm.SharedMemoryManager() as smm:
        lock = mp.Lock()
        shared_memory_server = ForceSensorSharedMemoryServer(
            shared_memory_manager=smm, lock=lock
        )

        from sas_force_sensor.gui import run as gui_run

        gui_process = mp.Process(
            target=gui_run,
            args=(shared_memory_server.get_shared_memory_receiver_initializer_args(), lock),
        )
        gui_process.start()

        try:
            while True:
                rclcpp_spin_some(node)

                if fsc.is_enabled():
                    force = fsc.get_force()
                    torque = fsc.get_torque()

                    f_vec = np.array(force.vector())
                    t_vec = np.array(torque.vector())
                    wrench = np.concatenate([f_vec, t_vec])
                    shared_memory_server.send_wrench(wrench.tolist())

                shared_memory_server.send_is_open(fsc.is_enabled())

                if shared_memory_server.get_shutdown_flag():
                    print("sas_force_sensor_gui_node::Info::Server shutdown by client.")
                    break

                time.sleep(0.01)

        except KeyboardInterrupt:
            print("sas_force_sensor_gui_node::Info::Shutdown by CTRL+C.")
            shared_memory_server.send_shutdown_flag(True)
        except Exception as e:
            print("sas_force_sensor_gui_node::Error::" + str(e))
            shared_memory_server.send_shutdown_flag(True)
        finally:
            gui_process.join()

    rclcpp_shutdown()
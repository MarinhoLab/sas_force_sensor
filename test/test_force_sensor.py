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
"""Tests for the force sensor client/server implementations.

Covers the shared-memory pair (ForceSensorSharedMemoryServer/Client) and the
ROS WrenchStamped pair exposed through the sas_force_sensor bindings.
"""

import multiprocessing as mp
import multiprocessing.managers as mm
import time

import pytest
import rclpy
from dqrobotics import DQ, vec8
from rclpy.utilities import ok, try_shutdown
from sas_force_sensor.shared_memory.client import ForceSensorSharedMemoryClient
from sas_force_sensor.shared_memory.server import ForceSensorSharedMemoryServer

from sas_common import rclcpp_init, rclcpp_Node, rclcpp_shutdown, rclcpp_spin_some
from sas_force_sensor import ForceSensorClient, ForceSensorServer

TIMEOUT = 15.0


def pure_dq(x, y, z):
    """Build a pure dual quaternion encoding the vector (x, y, z)."""
    return DQ([0.0, x, y, z, 0.0, 0.0, 0.0, 0.0])


@pytest.fixture(scope="module")
def rclpy_context():
    """Initialize the ROS context once for the whole module."""
    if not ok():
        rclpy.init()
    try:
        rclcpp_init()
        cpp_initialized = True
    except RuntimeError:
        cpp_initialized = False
    yield
    if cpp_initialized:
        rclcpp_shutdown()
    try_shutdown()


def test_shared_memory_server_client_round_trip():
    lock = mp.Lock()
    with mm.SharedMemoryManager() as smm:
        server = ForceSensorSharedMemoryServer(shared_memory_manager=smm, lock=lock)
        client = ForceSensorSharedMemoryClient(
            server.get_shared_memory_receiver_initializer_args(), lock)

        assert client.get_wrench() == [0.0] * 6
        assert not client.is_open()

        server.send_is_open(True)
        assert client.is_open()

        wrench = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
        server.send_wrench(wrench)
        assert client.get_wrench() == pytest.approx(wrench)

        # Malformed payloads are ignored.
        server.send_wrench([1.0, 2.0])
        server.send_wrench(None)
        assert client.get_wrench() == pytest.approx(wrench)

        assert not client.get_shutdown_flag()
        client.send_shutdown_flag(True)
        assert server.get_shutdown_flag()


def test_force_sensor_server_client_round_trip(rclpy_context):
    server_node = rclcpp_Node("fs_server_node")
    client_node = rclcpp_Node("fs_client_node")
    prefix = "/test_force_sensor"
    server = ForceSensorServer(server_node, prefix)
    client = ForceSensorClient(client_node, prefix)

    assert server.get_topic_prefix() == prefix
    assert client.get_topic_prefix() == prefix
    with pytest.raises(RuntimeError):
        client.get_force()

    force = pure_dq(1.0, 2.0, 3.0)
    torque = pure_dq(4.0, 5.0, 6.0)
    expected_force = list(vec8(force))
    expected_torque = list(vec8(torque))

    def arrived():
        server.send_force_torque(force, torque)
        return client.is_enabled()

    deadline = time.monotonic() + TIMEOUT
    while time.monotonic() < deadline:
        rclcpp_spin_some(server_node)
        rclcpp_spin_some(client_node)
        if arrived():
            break
        time.sleep(0.005)
    else:
        pytest.fail("force/torque did not arrive in time")

    assert list(vec8(client.get_force())) == pytest.approx(expected_force)
    assert list(vec8(client.get_torque())) == pytest.approx(expected_torque)

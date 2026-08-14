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
from multiprocessing import Lock
from multiprocessing.managers import SharedMemoryManager
from multiprocessing.shared_memory import ShareableList

from sas_force_sensor.shared_memory.common import shared_memory_map


class ForceSensorSharedMemoryServer:
    def __init__(self,
                 shared_memory_manager: SharedMemoryManager,
                 lock: Lock):
        self.shared_memory_manager: SharedMemoryManager = shared_memory_manager
        self.lock: Lock = lock

        self.shareable_wrench: ShareableList = shared_memory_manager.ShareableList(
            [0.0] * 6
        )

        self.connection_information_dict = shared_memory_map
        self.connection_information = shared_memory_manager.ShareableList(
            [False,
             False]
        )

    def get_shared_memory_receiver_initializer_args(self):
        return self.connection_information, self.shareable_wrench

    def send_wrench(self, wrench):
        if wrench is not None:
            if len(wrench) == 6:
                self.lock.acquire()
                for i in range(0, 6):
                    self.shareable_wrench[i] = wrench[i]
                self.lock.release()

    def send_is_open(self, is_open):
        self.lock.acquire()
        self.connection_information[self.connection_information_dict['is_open']] = is_open
        self.lock.release()

    def get_shutdown_flag(self):
        self.lock.acquire()
        shutdown_flag = self.connection_information[self.connection_information_dict['shutdown_flag']]
        self.lock.release()
        return shutdown_flag

    def send_shutdown_flag(self, flag):
        self.lock.acquire()
        self.connection_information[self.connection_information_dict['shutdown_flag']] = flag
        self.lock.release()
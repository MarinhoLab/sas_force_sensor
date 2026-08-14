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
from multiprocessing.shared_memory import ShareableList

from sas_force_sensor.shared_memory.common import shared_memory_map


class ForceSensorSharedMemoryClient:
    def __init__(self,
                 shared_memory_lists_tuple: ShareableList,
                 lock: Lock):
        self.connection_information_dict = shared_memory_map
        self.connection_information, \
        self.shareable_wrench = shared_memory_lists_tuple
        self.lock = lock

    def get_wrench(self):
        self.lock.acquire()
        wrench = list(self.shareable_wrench)
        self.lock.release()
        return wrench

    def is_open(self):
        self.lock.acquire()
        is_open = self.connection_information[self.connection_information_dict['is_open']]
        self.lock.release()
        return is_open

    def send_shutdown_flag(self, flag):
        self.lock.acquire()
        self.connection_information[self.connection_information_dict['shutdown_flag']] = flag
        self.lock.release()

    def get_shutdown_flag(self):
        self.lock.acquire()
        shutdown_flag = self.connection_information[self.connection_information_dict['shutdown_flag']]
        self.lock.release()
        return shutdown_flag
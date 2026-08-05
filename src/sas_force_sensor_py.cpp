/*
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
# ################################################################*/
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/eigen.h>

#include <rclcpp/rclcpp.hpp>

#include <sas_force_sensor/sas_force_sensor_client.hpp>
#include <sas_force_sensor/sas_force_sensor_server.hpp>

namespace py = pybind11;
using FSC = sas::ForceSensorClient;
using FSS = sas::ForceSensorServer;

PYBIND11_MODULE(_sas_force_sensor, m) {

    py::class_<FSC>(m, "ForceSensorClient")
            .def(py::init<const std::shared_ptr<rclcpp::Node>&, const std::string&>(),
                 py::arg("node"),
                 py::arg("topic_prefix") = "GET_FROM_NODE")
            .def("is_enabled",&FSC::is_enabled)
            .def("get_force",&FSC::get_force)
            .def("get_torque",&FSC::get_torque)
            .def("get_topic_prefix",&FSC::get_topic_prefix);

    py::class_<FSS>(m, "ForceSensorServer")
            .def(py::init<const std::shared_ptr<rclcpp::Node>&, const std::string&>(),
                 py::arg("node"),
                 py::arg("topic_prefix") = "GET_FROM_NODE")
            .def("send_force_torque",&FSS::send_force_torque)
            .def("get_topic_prefix",&FSS::get_topic_prefix);

}

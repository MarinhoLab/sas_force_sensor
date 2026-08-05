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
#include <sas_force_sensor/sas_force_sensor_server.hpp>
#include <sas_conversions/sas_conversions.hpp>
#include <sas_common/sas_common.hpp>

namespace sas
{

ForceSensorServer::ForceSensorServer(const std::shared_ptr<Node>& node, const std::string& topic_prefix):
    sas::Object("sas::ForceSensorServer"),
    node_(node),
    topic_prefix_(topic_prefix == "GET_FROM_NODE"? node->get_name() : topic_prefix)
{
    RCLCPP_INFO_STREAM(node_->get_logger(),"::Initializing "+get_class_name()+" with prefix " + topic_prefix_);

    publisher_wrench_ = node->create_publisher<geometry_msgs::msg::WrenchStamped>(topic_prefix_ + "/get/wrench", 1);
}

void ForceSensorServer::send_force_torque(const DQ& force, const DQ& torque) const
{
    publisher_wrench_->publish(dq_to_geometry_msgs_wrench_stamped(force, torque));
}

std::string ForceSensorServer::get_topic_prefix() const
{
    return topic_prefix_;
}

}

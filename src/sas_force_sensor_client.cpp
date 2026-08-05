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
#include <sas_force_sensor/sas_force_sensor_client.hpp>
#include <sas_conversions/sas_conversions.hpp>
#include <sas_common/sas_common.hpp>
using std::placeholders::_1;

namespace sas
{

void ForceSensorClient::_callback_wrench(const geometry_msgs::msg::WrenchStamped& msg)
{
    const std::string this_topic(topic_prefix_ + "/get/wrench");
    if(node_->count_publishers(this_topic)>1)
        throw std::runtime_error(this_topic + " must be exclusively published and there is more than one publisher connected.");

    geometry_msgs_wrench_stamped_to_dq(msg, force_, torque_);

    if(!enabled_)
    {
        enabled_ = true;
        RCLCPP_INFO_STREAM(node_->get_logger(),"::"+get_class_name()+" enabled.");
    }
}

ForceSensorClient::ForceSensorClient(const std::shared_ptr<Node>& node, const std::string& topic_prefix):
    sas::Object("sas::ForceSensorClient"),
    node_(node),
    enabled_(false),
    topic_prefix_(topic_prefix == "GET_FROM_NODE"? node->get_name() : topic_prefix),
    force_(0),
    torque_(0)
{
    RCLCPP_INFO_STREAM(node_->get_logger(),"::Initializing "+get_class_name()+" with prefix " + topic_prefix_);

    subscriber_wrench_ = node->create_subscription<geometry_msgs::msg::WrenchStamped>(
                topic_prefix_ + "/get/wrench", 1, std::bind(&ForceSensorClient::_callback_wrench, this, _1)
                );
}

bool ForceSensorClient::is_enabled() const
{
    return enabled_;
}

DQ ForceSensorClient::get_force() const
{
    if(is_enabled())
        return force_;
    else
        throw std::runtime_error("::"+get_class_name()+"::get_force()::trying to get force but uninitialized.");
}

DQ ForceSensorClient::get_torque() const
{
    if(is_enabled())
        return torque_;
    else
        throw std::runtime_error("::"+get_class_name()+"::get_torque()::trying to get torque but uninitialized.");
}

std::string ForceSensorClient::get_topic_prefix() const
{
    return topic_prefix_;
}

}

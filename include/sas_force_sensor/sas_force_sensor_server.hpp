#pragma once
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

#include <dqrobotics/DQ.h>

#include <rclcpp/rclcpp.hpp>
#include <geometry_msgs/msg/wrench_stamped.hpp>
#include <sas_core/sas_object.hpp>

using namespace rclcpp;
using namespace DQ_robotics;

namespace sas
{
/**
 * @class ForceSensorServer
 * @brief Server for force/torque sensor readings.
 *
 * ForceSensorServer publishes force/torque readings, obtained from a physical
 * (or simulated) force sensor, as a `geometry_msgs/msg/WrenchStamped` message.
 * Any number of `sas::ForceSensorClient` instances can subscribe to that topic
 * to retrieve the latest reading.
 */
class ForceSensorServer: private sas::Object
{
private:
    std::shared_ptr<Node> node_;

    const std::string topic_prefix_;

    Publisher<geometry_msgs::msg::WrenchStamped>::SharedPtr publisher_wrench_;
public:
    ForceSensorServer() = delete;
    ForceSensorServer(const ForceSensorServer&) = delete;

    /**
     * @brief Construct a new ForceSensorServer.
     *
     * @param node Shared pointer to the rclcpp::Node used for communication.
     * @param topic_prefix Prefix used to compose the ROS topic name (defaults to "GET_FROM_NODE",
     *                      in which case the node name is used).
     */
    ForceSensorServer(const std::shared_ptr<Node>& node, const std::string& topic_prefix="GET_FROM_NODE");

    /**
     * @brief Publish the current force/torque reading.
     *
     * @param force DQ (pure quaternion) representing the sensed force vector.
     * @param torque DQ (pure quaternion) representing the sensed torque vector.
     */
    void send_force_torque(const DQ& force, const DQ& torque) const;

    /**
     * @brief Get the configured topic prefix.
     *
     * @return std::string Topic prefix used by this server.
     */
    std::string get_topic_prefix() const;
};

}

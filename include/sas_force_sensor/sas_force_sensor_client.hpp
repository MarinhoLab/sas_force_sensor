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

#include <atomic>

#include <dqrobotics/DQ.h>

#include <rclcpp/rclcpp.hpp>
#include <geometry_msgs/msg/wrench_stamped.hpp>
#include <sas_core/sas_object.hpp>

using namespace rclcpp;
using namespace DQ_robotics;

namespace sas
{
/**
 * @class ForceSensorClient
 * @brief Client for force/torque sensor readings.
 *
 * ForceSensorClient subscribes to the `geometry_msgs/msg/WrenchStamped` topic
 * published by a `sas::ForceSensorServer` and exposes the latest force and
 * torque readings as dqrobotics `DQ` (pure quaternion) objects.
 */
class ForceSensorClient: private sas::Object
{
private:
    std::shared_ptr<Node> node_;

    std::atomic_bool enabled_;
    const std::string topic_prefix_;

    Subscription<geometry_msgs::msg::WrenchStamped>::SharedPtr subscriber_wrench_;
    DQ force_;
    DQ torque_;

    void _callback_wrench(const geometry_msgs::msg::WrenchStamped& msg);
public:
    ForceSensorClient() = delete;
    ForceSensorClient(const ForceSensorClient&) = delete;

    /**
     * @brief Construct a new ForceSensorClient.
     *
     * @param node Shared pointer to the rclcpp::Node used for communication.
     * @param topic_prefix Prefix used to compose the ROS topic name (defaults to "GET_FROM_NODE",
     *                      in which case the node name is used).
     */
    ForceSensorClient(const std::shared_ptr<Node>& node, const std::string& topic_prefix="GET_FROM_NODE");

    /**
     * @brief Check whether the client has received at least one force/torque reading.
     *
     * @return true if enabled, false otherwise.
     */
    bool is_enabled() const;

    /**
     * @brief Get the last received force reading.
     *
     * @return DQ (pure quaternion) representing the sensed force vector.
     * @throws std::runtime_error if the client is not enabled yet.
     */
    DQ get_force() const;

    /**
     * @brief Get the last received torque reading.
     *
     * @return DQ (pure quaternion) representing the sensed torque vector.
     * @throws std::runtime_error if the client is not enabled yet.
     */
    DQ get_torque() const;

    /**
     * @brief Get the configured topic prefix.
     *
     * @return std::string Topic prefix used by this client.
     */
    std::string get_topic_prefix() const;
};

}

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
#include <cmath>

#include <sas_force_sensor/sas_force_sensor_server.hpp>

namespace
{
const double amplitude = 2.0;
const double frequency_hz = 25.0;
const double tick_rate_hz = 100.0;
const double angular_frequency = 2.0 * M_PI * frequency_hz;
}

class SinusoidalForceSensorNode : public rclcpp::Node
{
public:
    SinusoidalForceSensorNode()
        : Node("sinusoidal_force_sensor")
    {
    }

    void attach_server()
    {
        server_ = std::make_shared<sas::ForceSensorServer>(
            std::shared_ptr<Node>(shared_from_this()), "sinusoidal_force_sensor");
        timer_ = this->create_wall_timer(
            std::chrono::milliseconds(static_cast<int>(1000.0 / tick_rate_hz)),
            std::bind(&SinusoidalForceSensorNode::on_timer, this));

        RCLCPP_INFO(this->get_logger(), "Sinusoidal force sensor node started.");
    }

private:
    void on_timer()
    {
        const double time_s = static_cast<double>(tick_++) / tick_rate_hz;
        const double value = amplitude * std::sin(angular_frequency * time_s);

        force_reading_ = value;
        torque_reading_ = value;

        DQ force(Vector3d(value, 0.0, 0.0));
        DQ torque(Vector3d(0.0, value, 0.0));

        server_->send_force_torque(force, torque);
    }

    std::shared_ptr<sas::ForceSensorServer> server_;
    rclcpp::TimerBase::SharedPtr timer_;
    double force_reading_ = 0.0;
    double torque_reading_ = 0.0;
    size_t tick_ = 0;
};

int main(int argc, char* argv[])
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<SinusoidalForceSensorNode>();
    node->attach_server();
    rclcpp::spin(node);
    return 0;
}

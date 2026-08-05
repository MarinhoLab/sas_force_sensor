# sas_force_sensor

> [!TIP]
> Repository for this module: https://github.com/MarinhoLab/sas_force_sensor. <br/>
> More information about SmartArmStack is available at https://smartarmstack.github.io/.

## Contents

- `include/` — public C++ headers.
- `src/` — library and pybind11 bindings.
- `sas_force_sensor/` — Python package (thin wrapper around the pybind11 module).
- `scripts/` — Python example script.

## Client–Server pair

The package implements a **ForceSensorServer / ForceSensorClient** pair that manages a
single `geometry_msgs/msg/WrenchStamped` topic, `<topic_prefix>/get/wrench`.

- `sas::ForceSensorServer` is used by the process that has access to the physical
  (or simulated) force/torque sensor. It publishes the readings.
- `sas::ForceSensorClient` is used by any other process that needs to consume the
  force/torque readings. It subscribes to the topic.

Both classes take a shared `rclcpp::Node` and a `topic_prefix` string that forms the
namespace for the topic. When `topic_prefix` is `"GET_FROM_NODE"` (the default) the
node name is used automatically.

Force and torque readings are exposed as `dqrobotics::DQ` pure quaternions, which is a
suitable and consistent representation across the SmartArmStack ecosystem.

### Header files

| Class                    | Header                                          |
|--------------------------|--------------------------------------------------|
| `sas::ForceSensorServer` | `sas_force_sensor/sas_force_sensor_server.hpp` |
| `sas::ForceSensorClient` | `sas_force_sensor/sas_force_sensor_client.hpp` |

### Importing in Python

```python
from sas_force_sensor import (
    ForceSensorServer,
    ForceSensorClient
)
```

## Script

Demonstrates `ForceSensorServer` and `ForceSensorClient` in Python.

```bash
ros2 run sas_force_sensor sas_force_sensor_interface_example.py
```

---
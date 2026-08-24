# sas_force_sensor

> [!TIP]
> Repository for this module: https://github.com/MarinhoLab/sas_force_sensor. <br/>
> More information about SmartArmStack is available at https://smartarmstack.github.io/.

## Contents

- `include/` — public C++ headers.
- `src/` — library and pybind11 bindings.
- `sas_force_sensor/` — Python package (thin wrapper around the pybind11 module).
- `scripts/` — Python example script.
- `launch/` — example launch file for the sinusoidal force sensor node.
- `config/` — example parameter configuration file.

## ROS 2 Nodes & Parameters

The package is primarily a library. It also provides one example node.

### Node: `sinusoidal_force_sensor`

| Property | Value |
|---|---|
| **Executable** | `sinusoidal_force_sensor` |
| **ROS node name** | `sinusoidal_force_sensor` (set by the `name` launch argument of `sinusoidal_force_sensor_launch.py`) |
| **Description** | Example node that publishes a sinusoidal force/torque wrench on `<node_name>/get/wrench` via `ForceSensorServer`. |

#### Parameters

The node currently declares **no ROS parameters** — the amplitude, frequency, and tick rate are hardcoded constants in `src/examples/sinusoidal_force_sensor.cpp`.

#### Sample launch

```console
ros2 launch sas_force_sensor sinusoidal_force_sensor_launch.py
```

The launch file loads the (currently empty) parameter block from `config/config.yaml` (override with `config_file:=/path/to/config.yaml`) so the node follows the standard SmartArmStack config-file pattern.

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
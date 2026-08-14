FROM murilomarinho/sas:jazzy
LABEL authors="murilomarinho"
SHELL ["/bin/bash", "-c"]
ENV BASH_ENV="/etc/bash_env"

RUN sudo apt-get update && sudo apt-get upgrade -y
RUN python3 -m pip install --upgrade dqrobotics --break-system-packages
RUN python3 -m pip install pyqtgraph PyQt6 --break-system-packages
# https://github.com/bhowiebkr/laser-level-webcam/issues/28
RUN python3 -m pip install pyqtdarktheme==2.1.0 --ignore-requires-python --break-system-packages
RUN apt-get remove -y ros-jazzy-sas-force-sensor
RUN mkdir -p /root/sas_force_sensor_devel/src/

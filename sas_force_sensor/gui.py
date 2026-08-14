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
from queue import Queue

import numpy as np

from PyQt6.QtCore import QTimer, Qt, QCoreApplication
from PyQt6.QtWidgets import (
    QWidget,
    QApplication,
    QMainWindow,
    QSlider,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
)

import qdarktheme
import pyqtgraph as pg

from sas_force_sensor.shared_memory.client import ForceSensorSharedMemoryClient


class SliderLabelVertical(QWidget):
    def __init__(self, label: str, slider_range: tuple, parent=None):
        super().__init__(parent)

        self.description_label = QLabel()
        self.description_label.setText(label)

        self.value_label = QLabel()
        self.value_label.setText(label)

        self.slider = QSlider(Qt.Orientation.Vertical)
        self.slider.setRange(slider_range[0], slider_range[1])

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.description_label)
        self.layout.addWidget(self.value_label)
        self.layout.addWidget(self.slider)

        self.setLayout(self.layout)

    def set_value(self, value):
        self.slider.setValue(value)

    def set_text(self, text):
        self.value_label.setText(text)


class ForceSensorMainWindow(QMainWindow):
    def __init__(self, shared_memory_client: ForceSensorSharedMemoryClient):
        super().__init__()

        self.setWindowTitle("sas_force_sensor")
        self.setMinimumHeight(400)

        self.shared_memory_client: ForceSensorSharedMemoryClient = shared_memory_client

        self.timer_ = QTimer()
        self.timer_.timeout.connect(self._timer_callback)
        self.timer_.start(1)

        self.central_widget = QWidget()
        self.layout = QHBoxLayout(self)

        self.force_slider = SliderLabelVertical("Force Norm", (-300, 300), self)
        self.torque_slider = SliderLabelVertical("Torque Norm", (-300, 300), self)

        # --- Force plots ---
        self.force_plot_layout = QVBoxLayout()
        self.plot_fx = pg.plot(title="f_x")
        self.plot_fy = pg.plot(title="f_y")
        self.plot_fz = pg.plot(title="f_z")
        self.fx_queue = Queue(maxsize=200)
        self.fy_queue = Queue(maxsize=200)
        self.fz_queue = Queue(maxsize=200)
        self.fx_lims = [0, 0]
        self.fy_lims = [0, 0]
        self.fz_lims = [0, 0]
        self.data_fx = self.plot_fx.plot([])
        self.data_fy = self.plot_fy.plot([])
        self.data_fz = self.plot_fz.plot([])
        self.force_plot_layout.addWidget(self.plot_fx)
        self.force_plot_layout.addWidget(self.plot_fy)
        self.force_plot_layout.addWidget(self.plot_fz)

        # --- Torque plots ---
        self.torque_plot_layout = QVBoxLayout()
        self.plot_tx = pg.plot(title="\\tau_x")
        self.plot_ty = pg.plot(title="\\tau_y")
        self.plot_tz = pg.plot(title="\\tau_z")
        self.tx_queue = Queue(maxsize=200)
        self.ty_queue = Queue(maxsize=200)
        self.tz_queue = Queue(maxsize=200)
        self.tx_lims = [0, 0]
        self.ty_lims = [0, 0]
        self.tz_lims = [0, 0]
        self.data_tx = self.plot_tx.plot([])
        self.data_ty = self.plot_ty.plot([])
        self.data_tz = self.plot_tz.plot([])
        self.torque_plot_layout.addWidget(self.plot_tx)
        self.torque_plot_layout.addWidget(self.plot_ty)
        self.torque_plot_layout.addWidget(self.plot_tz)

        self.layout.addWidget(self.force_slider)
        self.layout.addWidget(self.torque_slider)
        self.layout.addLayout(self.force_plot_layout)
        self.layout.addLayout(self.torque_plot_layout)

        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

    # ------------------------------------------------------------------ helpers
    @staticmethod
    def _update_queue_and_plot(queue, plot, data_item, lims, value, title):
        if queue.full():
            queue.get()
        queue.put(value)
        current_data = np.asarray(queue.queue)
        lims[0] = min(lims[0], np.min(current_data))
        lims[1] = max(lims[1], np.max(current_data))
        data_item.setData(np.linspace(0, 1, queue.qsize()), current_data)
        plot.setYRange(lims[0], lims[1])
        plot.setTitle(title)

    # ------------------------------------------------------------------ callback
    def _timer_callback(self):
        try:
            if self.shared_memory_client.is_open():
                wrench = self.shared_memory_client.get_wrench()

                f = np.array(wrench[0:3])
                t = np.array(wrench[3:6])
                f_norm = np.linalg.norm(f)

                self._update_queue_and_plot(self.fx_queue, self.plot_fx,
                                            self.data_fx, self.fx_lims, f[0], "fx")
                self._update_queue_and_plot(self.fy_queue, self.plot_fy,
                                            self.data_fy, self.fy_lims, f[1], "fy")
                self._update_queue_and_plot(self.fz_queue, self.plot_fz,
                                            self.data_fz, self.fz_lims, f[2], "fz")

                self._update_queue_and_plot(self.tx_queue, self.plot_tx,
                                            self.data_tx, self.tx_lims, t[0], "tx")
                self._update_queue_and_plot(self.ty_queue, self.plot_ty,
                                            self.data_ty, self.ty_lims, t[1], "ty")
                self._update_queue_and_plot(self.tz_queue, self.plot_tz,
                                            self.data_tz, self.tz_lims, t[2], "tz")

                self.force_slider.set_value(int(f_norm))
                self.force_slider.set_text('{:.2f}'.format(f_norm))

                t_norm = np.linalg.norm(t)
                self.torque_slider.set_value(int(t_norm))
                self.torque_slider.set_text('{:.2f}'.format(t_norm))

            if self.shared_memory_client.get_shutdown_flag():
                QCoreApplication.quit()
        except Exception:
            pass


def run(shared_memory_info, lock):
    shared_memory_client = ForceSensorSharedMemoryClient(shared_memory_info, lock)
    try:
        app = QApplication([])
        myapp = ForceSensorMainWindow(shared_memory_client)
        qdarktheme.setup_theme()
        myapp.show()
        app.exec()
    except Exception as e:
        print("sas_force_sensor::gui::Error::" + str(e))
    except KeyboardInterrupt:
        print("sas_force_sensor::gui::Info::Interrupted by user.")

    shared_memory_client.send_shutdown_flag(True)
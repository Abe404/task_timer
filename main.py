"""
Copyright (C) 2022 Abraham George Smith
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


import datetime
from enum import Enum
import sys
import time


from PyQt5 import QtWidgets 
from PyQt5 import QtCore
from PyQt5 import QtGui


class TimerState(Enum):
    IDLE = 1
    TIMING = 2 # timing
    STOPPED = 3 # timing but STOPPED (caused by stop button)


class MainWindow(QtWidgets.QMainWindow):

    def start_timer(self):
        self.prev_update_time = time.time() # updates start from now.
        self.timer_state = TimerState.TIMING
        self.start_time = time.time() # epoch time

    def stop_timer(self):
        self.timer_state = TimerState.STOPPED
        
    def save_timing(self):
        print('saving', self.duration_seconds, 'to spreadsheet with start time end time and organ name')

    def reset_timer(self):
        self.duration_seconds = 0
        self.timer_state = TimerState.IDLE
 
    def add_start_button(self):
        self.start_button = QtWidgets.QPushButton('start', self)
        self.start_button.pressed.connect(self.start_timer)
        self.start_button.setGeometry(10, 70, 200, 60)

    def add_stop_button(self):
        self.stop_button = QtWidgets.QPushButton('stop', self)
        self.stop_button.pressed.connect(self.stop_timer)
        self.stop_button.setGeometry(10, 140, 200, 60)

    def add_reset_button(self):
        self.reset_button = QtWidgets.QPushButton('reset', self)
        self.reset_button.pressed.connect(self.reset_timer)
        self.reset_button.setGeometry(10, 210, 200, 60)
        self.duration_seconds = 0

    def add_save_button(self):
        self.save_button = QtWidgets.QPushButton('save', self)
        self.save_button.pressed.connect(self.save_timing)
        self.save_button.setGeometry(10, 280, 200, 60)

    def show_current_duration(self):
        if self.timer_state == TimerState.TIMING:
            duration_str = str(datetime.timedelta(seconds=self.duration_seconds))
        elif self.timer_state == TimerState.STOPPED:
            duration_str = str(datetime.timedelta(seconds=round(self.duration_seconds, 2)))
        else:
            duration_str = '0:00:00.00'
        self.time_label.setText(duration_str[:10])

    def update_duration(self):
        if self.timer_state == TimerState.TIMING:
            cur_time = time.time()
            time_passed = cur_time - self.prev_update_time
            self.prev_update_time = cur_time
            self.duration_seconds = self.duration_seconds + time_passed
        self.show_current_duration()


    def add_display_timer(self):
        self.display_timer = QtCore.QTimer()
        self.display_timer.start(50) # updates 20 times a second
        self.display_timer.timeout.connect(self.update_duration)

    def create_ui(self):
       self.setWindowTitle("Task timer")
       self.setGeometry(10, 10, 300, 600)
       self.add_start_button()
       self.add_reset_button()
       self.add_stop_button()
       self.add_save_button()
       self.create_time_label()
       self.show_current_duration()
       self.add_display_timer()

    def create_time_label(self):
       self.time_label = QtWidgets.QLabel(self)
       self.time_label.setFont(QtGui.QFont('Arial', 36))
       self.time_label.setGeometry(25, 10, 200, 60)

    def __init__(self):
        super().__init__()
        self.timer_state = TimerState.IDLE
        self.duration_seconds = 0
        self.create_ui()


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())

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

import os
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

        self.stop_button.show()
        self.stop_button.setEnabled(True)
        self.start_button.hide()

    def stop_timer(self):
        self.timer_state = TimerState.STOPPED
        self.stop_button.hide()
        self.start_button.show()
        self.start_button.setEnabled(True)
        self.reset_button.show()
        self.save_button.show()
        self.textbox.show()
        self.notes_label.show()

    def clear_info_label(self):
        self.info_label.setText('')

    def save_timing(self):
        now_str = datetime.datetime.now().isoformat()
        fname = 'spreadsheet.csv'
        if os.path.exists(fname):
            f = open('spreadsheet.csv', 'a')
        else:
            f = open('spreadsheet.csv', 'w')
            print('duration_seconds,task_name,save_time,notes', file=f)
        print(f'{self.duration_seconds},{self.combo.currentText()},'
              f'{now_str},{self.textbox.text()}', file=f)
        #self.info_label.setText(f'Saved timing for {self.combo.currentText()}')
        self.reset()
        #QtCore.QTimer.singleShot(600, self.clear_info_label)

    def reset(self):
        self.duration_seconds = 0
        self.timer_state = TimerState.IDLE
        self.reset_button.hide()
        self.save_button.hide()
        self.textbox.setText('')
        self.textbox.hide()
        self.notes_label.hide()
 
    def add_start_button(self, y):
        self.start_button = QtWidgets.QPushButton('start', self)
        self.start_button.clicked.connect(self.start_timer)
        self.start_button.setGeometry(10, y, 200, 60)

    def add_stop_button(self, y):
        self.stop_button = QtWidgets.QPushButton('stop', self)
        self.stop_button.clicked.connect(self.stop_timer)
        self.stop_button.setGeometry(10, y, 200, 60)
        self.stop_button.hide()
        

    def add_reset_button(self, y):
        self.reset_button = QtWidgets.QPushButton('reset', self)
        self.reset_button.clicked.connect(self.reset)
        self.reset_button.setGeometry(10, y, 200, 60)
        self.duration_seconds = 0
        self.reset_button.hide()

    def add_save_button(self, y):
        self.save_button = QtWidgets.QPushButton('save', self)
        self.save_button.clicked.connect(self.save_timing)
        self.save_button.setGeometry(10, y, 200, 60)
        self.save_button.hide()

    def show_current_duration(self):
        if self.timer_state == TimerState.TIMING:
            duration_str = str(datetime.timedelta(seconds=self.duration_seconds))
        elif self.timer_state == TimerState.STOPPED:
            duration_str = str(datetime.timedelta(seconds=round(self.duration_seconds, 2)))
        else:
            duration_str = '0:00:00.00'
        self.time_label.setText(duration_str[:10])


    def add_info_label(self, y):
       self.info_label = QtWidgets.QLabel(self)
       self.info_label.setFont(QtGui.QFont('Arial', 12))
       self.info_label.setGeometry(25, y, 200, 60)


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

    def add_task_selection(self, y):
        self.combo = QtWidgets.QComboBox(self)
        self.combo.setGeometry(10, y, 200, 60)
        self.combo.addItem("Kindey")
        self.combo.addItem("Bowel bag")
        self.combo.addItem("Spinal cord")

    def add_notes_input(self, y):
        self.notes_label = QtWidgets.QLabel(self)
        self.notes_label.setFont(QtGui.QFont('Arial', 12))
        self.notes_label.setGeometry(15, y, 200, 15 )
        self.notes_label.setText('Notes')
        self.notes_label.hide()

        self.textbox = QtWidgets.QLineEdit(self)
        self.textbox.move(15, y + 20)
        self.textbox.resize(190, 40)
        self.textbox.hide()

    def create_ui(self):
       self.setWindowTitle("Task timer")
       self.setGeometry(10, 10, 220, 430)
       self.add_task_selection(y=10)
       self.add_start_button(y=70)
       self.add_stop_button(y=70)
       self.create_time_label(y=140)
       self.add_reset_button(y=210)
       self.add_notes_input(y=280)
       self.add_save_button(y=350)
       #self.add_info_label(y=325)
       self.show_current_duration()
       self.add_display_timer()

    def create_time_label(self, y):
       self.time_label = QtWidgets.QLabel(self)
       self.time_label.setFont(QtGui.QFont('Arial', 36))
       self.time_label.setGeometry(25, y, 200, 60)

    def __init__(self):
        super().__init__()
        self.timer_state = TimerState.IDLE
        self.duration_seconds = 0
        self.create_ui()

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())


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
from pathlib import Path
from turtle import color

from PyQt5 import QtWidgets 
from PyQt5 import QtCore
from PyQt5 import QtGui
import toml

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
        self.setFixedSize(self.layout.sizeHint())

    def stop_timer(self):
        self.timer_state = TimerState.STOPPED
        self.stop_button.hide()
        self.start_button.show()
        self.start_button.setEnabled(True)
        self.reset_button.show()
        self.save_button.show()
        self.notes_textbox.show()
        self.notes_label.show()
        self.id_textbox.show()
        self.id_label.show()
        self.validate()
        self.setFixedSize(self.layout.sizeHint())


    def clear_info_label(self):
        self.info_label.setText('')

    def save_timing(self):
        now_str = datetime.datetime.now().isoformat()
        if os.path.exists(self.csv_path):
            f = open(self.csv_path, 'a')
        else:
            f = open(self.csv_path, 'w')
            print('duration_seconds,task_name,user_name,save_time,id,notes', file=f)
        print(f'{self.duration_seconds},{self.task_name_combo.currentText()},'
              f'{self.user_name_combo.currentText()},{now_str},'
              f'{self.id_textbox.text()},{self.notes_textbox.text()}', file=f)
        self.reset()

    def reset(self):
        self.duration_seconds = 0
        self.timer_state = TimerState.IDLE
        self.reset_button.hide()
        self.save_button.hide()
        self.notes_textbox.setText('')
        self.notes_textbox.hide()
        self.notes_label.hide()
        self.id_textbox.setText('')
        self.id_textbox.hide()
        self.id_label.hide()
        self.info_label.setText("")
        self.info_label.hide()
        self.setFixedSize(self.layout.sizeHint())
 
    def validate(self):
        if not self.id_textbox.text():
            self.save_button.hide()
            self.info_label.setText("ID is required")
            self.info_label.show()
        elif self.timer_state == TimerState.STOPPED:
            self.save_button.show()
            self.info_label.setText("")
            self.info_label.hide()

        self.setFixedSize(self.layout.sizeHint())


    def add_start_button(self):
        self.start_button = QtWidgets.QPushButton('start')
        self.start_button.clicked.connect(self.start_timer)
        self.layout.addWidget(self.start_button)

    def add_stop_button(self):
        self.stop_button = QtWidgets.QPushButton('stop')
        self.stop_button.clicked.connect(self.stop_timer)
        self.layout.addWidget(self.stop_button)
        self.stop_button.hide()
        
    def add_reset_button(self):
        self.reset_button = QtWidgets.QPushButton('reset')
        self.reset_button.clicked.connect(self.reset)
        self.layout.addWidget(self.reset_button)
        self.duration_seconds = 0
        self.reset_button.hide()

    def add_save_button(self):
        self.save_button = QtWidgets.QPushButton('save')
        self.save_button.clicked.connect(self.save_timing)
        self.layout.addWidget(self.save_button)
        self.save_button.hide()

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

    def add_task_name_combo(self):
        label = QtWidgets.QLabel(self)
        label.setFont(QtGui.QFont('Arial', 12))
        label.setText('Task')
        self.layout.addWidget(label)
        self.task_name_combo = QtWidgets.QComboBox(self)
        for task_name in self.task_names:
            self.task_name_combo.addItem(task_name)
        self.layout.addWidget(self.task_name_combo)

    def add_user_name_combo(self):
        label = QtWidgets.QLabel(self)
        label.setFont(QtGui.QFont('Arial', 12))
        label.setText('User')
        self.layout.addWidget(label)
        self.user_name_combo = QtWidgets.QComboBox()
        for i, user_name in enumerate(self.user_names):
            self.user_name_combo.addItem(user_name)
            if user_name == self.default_user_name:
                self.user_name_combo.setCurrentIndex(i)
        self.layout.addWidget(self.user_name_combo)
            
    def add_id_input(self):
        self.id_label = QtWidgets.QLabel()
        self.id_label.setFont(QtGui.QFont('Arial', 12))
        self.id_label.setText('ID')
        self.layout.addWidget(self.id_label)
        self.id_label.hide()
        
        self.id_textbox = QtWidgets.QLineEdit(self)
        self.id_textbox.resize(190, 60)

        self.id_textbox.textChanged.connect(self.validate)

        self.layout.addWidget(self.id_textbox)
        self.id_textbox.hide()

    def add_notes_input(self):
        self.notes_label = QtWidgets.QLabel()
        self.notes_label.setFont(QtGui.QFont('Arial', 12))
        self.notes_label.setText('Notes')
        self.layout.addWidget(self.notes_label)
        self.notes_label.hide()
        self.notes_textbox = QtWidgets.QLineEdit(self)
        self.notes_textbox.resize(190, 30)
        self.notes_textbox.hide()
        self.layout.addWidget(self.notes_textbox)
        
    def add_info_label(self):
        """ info label is used for displaying message when the ID has not been specified """
        self.info_label = QtWidgets.QLabel()
        self.info_label.setFont(QtGui.QFont('Arial', 12))
        self.info_label.setStyleSheet("color: rgb(255, 0, 0);")
        self.info_label.setText('')
        self.layout.addWidget(self.info_label)

    def create_ui(self):
        self.setWindowTitle("Task timer")
        container = QtWidgets.QWidget()
        container_layout = QtWidgets.QVBoxLayout()
        container.setLayout(container_layout)
        self.layout = container_layout
        self.setCentralWidget(container)
        self.add_user_name_combo()
        self.add_task_name_combo()
        self.add_start_button()
        self.add_stop_button()
        self.create_time_label()
        self.add_reset_button()
        self.add_id_input()
        self.add_notes_input()
        self.add_save_button()
        self.show_current_duration()
        self.add_display_timer()
        self.add_info_label()
        self.setFixedSize(self.layout.sizeHint())

    def create_time_label(self):
       self.time_label = QtWidgets.QLabel()
       self.time_label.setAlignment(QtCore.Qt.AlignCenter)
       self.time_label.setFont(QtGui.QFont('Arial', 28))
       self.layout.addWidget(self.time_label)

    def __init__(self):
        super().__init__()

        settings_path = os.path.join(Path.home(), 'task_timer_settings.toml.txt')
        settings = toml.loads(open(settings_path).read())
        self.user_names = settings['user_names']
        self.task_names = settings['task_names']
        self.default_user_name = settings['default_user_name']
        self.csv_path = settings['csv_path']
        self.timer_state = TimerState.IDLE
        self.duration_seconds = 0
        
        self.setStyleSheet("""
            QPushButton{font-size: 14pt;}
            QComboBox{font-size: 11pt;}
        """)

        self.create_ui()


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())

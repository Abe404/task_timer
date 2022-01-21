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

import sys
from PyQt5 import QtWidgets 

class MainWindow(QtWidgets.QMainWindow):

    def add_start_button(self):
        start_button = QtWidgets.QPushButton('start', self)
 
    def create_ui(self):
       label = QtWidgets.QLabel(self)
       label.setText("task timer")
       label.move(10, 10)
       self.setGeometry(100, 100, 200, 60)
       self.setWindowTitle("Task timer")

    def __init__(self):
        super().__init__()
        self.create_ui()

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())

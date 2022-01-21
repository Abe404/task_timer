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

import sys
from PyQt5 import QtWidgets 

if __name__ == '__main__':
   app = QtWidgets.QApplication(sys.argv)
   widget = QtWidgets.QWidget()
   label = QtWidgets.QLabel(widget)
   label.setText("task timer")
   label.move(10, 10)
   widget.setGeometry(100, 100, 200, 60)
   widget.setWindowTitle("Task timer")
   widget.show()
   sys.exit(app.exec_())

import sys
from PyQt5 import QtWidgets 

if __name__ == '__main__':
   app = QtWidgets.QApplication(sys.argv)
   widget = QtWidgets.QWidget()
   label = QtWidgets.QLabel(widget)
   label.setText("hello")
   label.move(100, 100)
   widget.setGeometry(100,100,400,300)
   widget.setWindowTitle("Task timer")
   widget.show()
   sys.exit(app.exec_())

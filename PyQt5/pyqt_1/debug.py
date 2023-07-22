import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

def window():
   app = QApplication(sys.argv)
   win = QWidget()

   # b1 = QPushButton("Button1")
   # b2 = QPushButton("Button2")
   #
   # hbox = QHBoxLayout(win)
   # hbox.addWidget(b1)
   # hbox.addStretch()
   # hbox.addWidget(b2)

   layout = QHBoxLayout()

   button1 = QPushButton("One")
   button2 = QPushButton("Two")
   button3 = QPushButton("Three")
   button4 = QPushButton("Four")
   button5 = QPushButton("Five")
   # button5.setGeometry(650,495,239,239)

   # left_container = QWidget()
   # left_container.setFixedWidth(130)

   layout.addWidget(button1)
   layout.addStretch()
   layout.addWidget(button2)
   layout.addStretch()
   layout.addWidget(button3)
   layout.addStretch()
   layout.addWidget(button4)
   layout.addStretch()
   layout.addWidget(button5)

   # hbox.addStretch()
   # hbox.addLayout(layout)
   layout.setGeometry(QRect(500,500,500,500))
   win.setLayout(layout)

   win.setWindowTitle("PyQt")
   win.show()
   sys.exit(app.exec_())

if __name__ == '__main__':
   window()

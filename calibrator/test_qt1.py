import sys
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.resize(506, 312)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.hbox = QtWidgets.QHBoxLayout(self.centralwidget)

        self.toolButton = QtWidgets.QToolButton(self.centralwidget)
        # self.toolButton.setGeometry(QtCore.QRect(220, 120, 41, 41))
        self.toolButton1 = QtWidgets.QToolButton(self.centralwidget)
        # self.toolButton1.setGeometry(QtCore.QRect(120, 20, 141, 41))

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButton.sizePolicy().hasHeightForWidth())
        self.toolButton.setSizePolicy(sizePolicy)
        self.toolButton.setMaximumSize(QtCore.QSize(300, 100))
        self.hbox.addWidget(self.toolButton)
        self.hbox.addWidget(self.toolButton1)

        # icon = QtGui.QIcon()
        # icon.addPixmap(QtGui.QPixmap("exiticon.png [exact location of image]"),
        #                QtGui.QIcon.Normal, QtGui.QIcon.Off)
        #
        # # adding icon to the toolbutton
        # self.toolButton.setIcon(icon)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # adding signal and slot
        self.toolButton.clicked.connect(self.exitapp)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

        # For closing the application

    def exitapp(self):
        sys.exit()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
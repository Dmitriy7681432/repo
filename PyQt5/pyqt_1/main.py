# уроки - https://www.youtube.com/watch?v=M4EovcpiuNs&t=2s
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication

Form, Window = uic.loadUiType("test.ui")

app = QApplication([])
window =Window()
form =Form()
form.setupUi(window)
window.show()
app.exec_()
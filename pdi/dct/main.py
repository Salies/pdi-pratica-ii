from sys import argv
from PyQt5.QtWidgets import QApplication
from .gui.mainwindow import MainWindow

app = QApplication(argv)
w = MainWindow()

w.show()
app.exec()
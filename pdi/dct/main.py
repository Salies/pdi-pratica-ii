from sys import argv
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from pdi.dct.gui.mainwindow import MainWindow

app = QApplication(argv)
app.setAttribute(Qt.AA_DisableWindowContextHelpButton)
w = MainWindow()

w.show()
app.exec()
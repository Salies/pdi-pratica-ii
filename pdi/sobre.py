from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout
from PyQt5.QtGui import QIcon

class Sobre(QDialog):
    def __init__ (self, icopath):
        super().__init__()
        labelTxt = '''Este programa é parte dos trabalhos práticos do segundo bimestre 
da disciplina de Processamento Digital de Imagens, 
ministrada na FCT-UNESP em 2022.\n\nAutores:\nCarlos Eduardo Fernandes de Santana\nDaniel Henrique Serezane Pereira'''
        label = QLabel(labelTxt)
        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)
        self.setWindowTitle("Sobre")
        self.setWindowIcon(QIcon(icopath))
        self.exec_()
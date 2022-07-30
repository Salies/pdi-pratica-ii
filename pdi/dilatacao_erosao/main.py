''' 
Este programa é parte dos trabalhos práticos do segundo bimestre 
da disciplina de Processamento Digital de Imagens,
ministrada na FCT-UNESP em 2022.

Autores:
Carlos Eduardo Fernandes de Santana
Daniel Henrique Serezane Pereira

///

Aula 12
Prática
Implemente a operação de dilatação e erosão de imagens binárias compare o resultado da erosão com o método de afinamento de Zhang e Suen
'''

from sys import argv
import numpy as np
from numba import njit
from PIL import Image
from PIL.ImageQt import ImageQt
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QScrollArea, QMenu, QAction, QFileDialog
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from pdi.zhang_suen import zhang_suen

@njit
def dilatar(img):
    # Matriz de dilatação
    masc = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])
    # Cria uma imagem com o mesmo tamanho da original
    img_dil = np.full(img.shape, False)
    for x in range(1, img.shape[0] - 1):
        for y in range(1, img.shape[1] - 1):
            cor = img[x, y]
            # Para cada vizinho do pixel atual
            if cor == True:
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if masc[i + 1, j + 1] == 1:
                            img_dil[x + i, y+ j] = True # Pixel branco
    return img_dil

@njit
def erodir(img):
    # Matriz de erosão
    masc = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])
    # Cria uma imagem com o mesmo tamanho da original
    img_ero = np.full(img.shape, False)
    for x in range(1, img.shape[0] - 1):
        for y in range(1, img.shape[1] - 1):
            cor = img[x, y]
            # Para cada vizinho do pixel atual
            if cor == True:
                remove = False
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if (masc[i + 1, j + 1] == 1) and (img[x + i, y + j] == False):
                            remove = True
                if remove:
                    img_ero[x, y] = False
                else:
                    img_ero[x, y] = True
    return img_ero

class MainWindow(QMainWindow):
    def __init__ (self):
        super().__init__()
        self.setWindowTitle("PDI -- Dilatação e erosão (morfologia)")
        self.setWindowIcon(QIcon('ico/brewmaster.ico'))
        im = Image.open("imagens/teste.bmp").convert("1")
        self.__img = np.array(im)
        de_layout = QVBoxLayout()
        btn_layout = QHBoxLayout()
        btnDil = QPushButton("Dilatar")
        btnDil.clicked.connect(self.faz_dilatar)
        btnEro = QPushButton("Erodir")
        btnEro.clicked.connect(self.faz_erodir)
        btn_layout.addWidget(btnDil)
        btn_layout.addWidget(btnEro)
        self.__mainImgLabel = QLabel()
        self.__mainImgLabel.setFixedSize(400, 300)
        self.__mainImgLabel.setFrameStyle(QFrame.StyledPanel)
        self.__mainImgLabel.setPixmap(QPixmap.fromImage(ImageQt(im)))
        sobreWidget = QLabel("<sobre>")
        sobreWidget.setToolTip('''Este programa é parte dos trabalhos práticos do segundo bimestre 
da disciplina de Processamento Digital de Imagens, 
ministrada na FCT-UNESP em 2022.\n\nAutores:\nCarlos Eduardo Fernandes de Santana\nDaniel Henrique Serezane Pereira''')
        de_layout.addLayout(btn_layout)
        de_layout.addWidget(self.__mainImgLabel)
        de_layout.addWidget(sobreWidget)
        zs_layout = QVBoxLayout()
        zs_dl = QLabel("Imagem afinada por Zhang-Suen:")
        #a.setStyleSheet(''' font-size: 20px; ''')
        zs_dl.setContentsMargins(0, 5, 0, 5)
        zs_layout.addWidget(zs_dl)
        zs_label = QLabel()
        zs_label.setFixedSize(400, 300)
        zs_label.setFrameStyle(QFrame.StyledPanel)
        zs_label.setPixmap(QPixmap.fromImage(ImageQt(Image.fromarray(zhang_suen(self.__img)))))
        zs_layout.addWidget(zs_label)
        zs_layout.addWidget(QLabel(""))
        centralLayout = QHBoxLayout()
        centralLayout.addLayout(de_layout)
        centralLayout.addLayout(zs_layout)
        centralWidget = QWidget()
        centralWidget.setLayout(centralLayout)
        self.setCentralWidget(centralWidget)
    
    def faz_dilatar(self):
        self.__img = dilatar(self.__img)
        self.__mainImgLabel.setPixmap(QPixmap.fromImage(ImageQt(Image.fromarray(self.__img))))
    
    def faz_erodir(self):
        self.__img = erodir(self.__img)
        self.__mainImgLabel.setPixmap(QPixmap.fromImage(ImageQt(Image.fromarray(self.__img))))

app = QApplication(argv)
app.setAttribute(Qt.AA_DisableWindowContextHelpButton)
w = MainWindow()

w.show()
app.exec()
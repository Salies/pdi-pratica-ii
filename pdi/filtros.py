from sys import argv
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QScrollArea, QMenu, QAction, QFileDialog
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from PIL import Image
from PIL.ImageQt import ImageQt
from numpy import array as nparray
from numba import njit
from pdi.sobre import Sobre
from pdi.slithice import filtra_imagem

# Funções filtro
@njit
def filtro_max(vec):
    v_max = vec[0]
    for i in range(1, len(vec)):
        if(vec[i] > v_max):
            v_max = vec[i]
    return v_max

@njit
def filtro_min(vec):
    v_min = vec[0]
    for i in range(1, len(vec)):
        if(vec[i] < v_min):
            v_min = vec[i]
    return v_min

@njit
def filtro_pmedio(vec):
    v_min = vec[0]
    v_max = vec[0]
    for i in range(1, len(vec)):
        if(vec[i] < v_min):
            v_min = vec[i]
        if(vec[i] > v_max):
            v_max = vec[i]
    return (v_max + v_min) // 2

# Interface gráfica
class MainWindow(QMainWindow):
    def __init__ (self):
        super().__init__()
        self.setWindowTitle("PDI -- Filtros")
        self.setWindowIcon(QIcon('ico/enigma.ico'))
        centralWidget = QWidget()
        centralLayout = QHBoxLayout()
        menuArquivo = QMenu("Arquivo", self)
        menuAjuda = QMenu("Ajuda", self)
        sobre_action = QAction("Sobre", self)
        abrir_action = QAction("Abrir", self)
        sobre_action.triggered.connect(lambda: Sobre('ico/enigma.ico'))
        abrir_action.triggered.connect(self.abrir)
        menuAjuda.addAction(sobre_action)
        menuArquivo.addAction(abrir_action)
        scroll1 = QScrollArea()
        scroll2 = QScrollArea()
        scroll1.setFixedSize(516, 516)
        scroll2.setFixedSize(516, 516)
        self.__label1 = QLabel()
        self.__label2 = QLabel()
        scroll1.setWidget(self.__label1)
        scroll2.setWidget(self.__label2)
        opcoesLayout = QVBoxLayout()
        opcoesLayout.setAlignment(Qt.AlignVCenter)
        opcoesLayout.addWidget(QLabel("Filtros:"))
        self.__btnMinimo = QPushButton("Mínimo")
        self.__btnMaximo = QPushButton("Máximo")
        self.__btnPMedio = QPushButton("Ponto médio")
        self.__btnMinimo.clicked.connect(self.filtro_minimo)
        self.__btnMaximo.clicked.connect(self.filtro_maximo)
        self.__btnPMedio.clicked.connect(self.filtro_ponto_medio)
        opcoesLayout.addWidget(self.__btnMinimo)
        opcoesLayout.addWidget(self.__btnMaximo)
        opcoesLayout.addWidget(self.__btnPMedio)
        centralLayout.addWidget(scroll1)
        centralLayout.addLayout(opcoesLayout)
        centralLayout.addWidget(scroll2)
        centralWidget.setLayout(centralLayout)
        self.__btnMinimo.setEnabled(False)
        self.__btnMaximo.setEnabled(False)
        self.__btnPMedio.setEnabled(False)
        menubar = self.menuBar()
        menubar.addMenu(menuArquivo)
        menubar.addMenu(menuAjuda)
        self.setCentralWidget(centralWidget)

    def abrir(self, event):
        pathArquivo = QFileDialog.getOpenFileName(self, "Abrir imagem", "", "Imagens (*.png *.jpg *.bmp *.tif)")[0]
        if not pathArquivo:
            return
        self.__btnMinimo.setEnabled(True)
        self.__btnMaximo.setEnabled(True)
        self.__btnPMedio.setEnabled(True)
        self.__image2 = None
        self.__label2.clear()
        self.__label2.resize(0, 0)
        self.__image1 = Image.open(pathArquivo).convert('L')
        width, height = self.__image1.size
        self.__label1.resize(width, height)
        self.__label1.setPixmap(QPixmap.fromImage(ImageQt(self.__image1)))

    def filtro_maximo(self, event):
        self.__image2 = Image.fromarray(filtra_imagem(nparray(self.__image1), filtro_max, 3, 3)).convert('L')
        width, height = self.__image2.size
        self.__label2.resize(width, height)
        self.__label2.setPixmap(QPixmap.fromImage(ImageQt(self.__image2)))

    def filtro_minimo(self, event):
        self.__image2 = Image.fromarray(filtra_imagem(nparray(self.__image1), filtro_min, 3, 3)).convert('L')
        width, height = self.__image2.size
        self.__label2.resize(width, height)
        self.__label2.setPixmap(QPixmap.fromImage(ImageQt(self.__image2)))

    def filtro_ponto_medio(self, event):
        self.__image2 = Image.fromarray(filtra_imagem(nparray(self.__image1), filtro_pmedio, 3, 3)).convert('L')
        width, height = self.__image2.size
        self.__label2.resize(width, height)
        self.__label2.setPixmap(QPixmap.fromImage(ImageQt(self.__image2)))

app = QApplication(argv)
app.setAttribute(Qt.AA_DisableWindowContextHelpButton)
w = MainWindow()

w.show()
app.exec()
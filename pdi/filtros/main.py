from sys import argv
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QFrame, QScrollArea, QMenu, QAction, QFileDialog, QSizePolicy
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from PIL import Image
from PIL.ImageQt import ImageQt
from pdi.sobre import Sobre

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
        opcoesLayout.addWidget(self.__btnMinimo)
        opcoesLayout.addWidget(self.__btnMaximo)
        opcoesLayout.addWidget(self.__btnPMedio)
        centralLayout.addWidget(scroll1)
        centralLayout.addLayout(opcoesLayout)
        centralLayout.addWidget(scroll2)
        centralWidget.setLayout(centralLayout)
        menubar = self.menuBar()
        menubar.addMenu(menuArquivo)
        menubar.addMenu(menuAjuda)
        self.setCentralWidget(centralWidget)

    def abrir(self, event):
        pathArquivo = QFileDialog.getOpenFileName(self, "Abrir imagem", "", "Imagens (*.png *.jpg *.bmp)")[0]
        if not pathArquivo:
            return
        self.__image1 = Image.open(pathArquivo).convert('L')
        width, height = self.__image1.size
        self.__label1.resize(width, height)
        self.__label1.setPixmap(QPixmap.fromImage(ImageQt(self.__image1)))

app = QApplication(argv)
app.setAttribute(Qt.AA_DisableWindowContextHelpButton)
w = MainWindow()

w.show()
app.exec()
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QFrame, QMenu, QAction, QFileDialog, QApplication
from PyQt5.QtGui import QPixmap
# esse Qt é o namespace do Qt, com algumas propriedades (números, valores) predefinidos
# por exemplo o Qt.AlignVCenter em C++ seria Qt::AlignVCenter
from PyQt5.QtCore import Qt
from PIL import Image
from PIL.ImageQt import ImageQt
from numpy import array as nparray
from ..dct import dct, idct
from ...slithice import normalizar

# Classe principal de interface gráfica
# Como é um programa simples, resolvemos concentrar praticamente todo
# o funcionamento da interface aqui.
class MainWindow(QMainWindow):
    def __init__ (self):
        super().__init__()
        # Criando widgets base
        centralWidget = QWidget()
        centralLayout = QHBoxLayout()
        # Criando menuBar
        menubar = self.menuBar()
        menuArquivo = QMenu("Arquivo", self)
        abrir_action = QAction("Abrir", self)
        abrir_action.triggered.connect(self.abrir)
        menuArquivo.addAction(abrir_action)
        menubar.addMenu(menuArquivo)
        # Criando statusBar
        self.statusBar().showMessage("Abra uma imagem")
        # Criando labels pras images
        self.__label1 = QLabel()
        self.__label2 = QLabel()
        self.__label1.setFixedSize(128, 128)
        self.__label2.setFixedSize(128, 128)
        self.__label1.setFrameStyle(QFrame.StyledPanel)
        self.__label2.setFrameStyle(QFrame.StyledPanel)
        # Criando os botões pra usar DCT/iDCT
        self.__btnDCT = QPushButton("DCT")
        self.__btniDCT = QPushButton("iDCT")
        self.__btnDCT.clicked.connect(self.fazer_dct)
        self.__btniDCT.clicked.connect(self.fazer_idct)
        btnLayout = QVBoxLayout()
        btnLayout.setAlignment(Qt.AlignVCenter)
        btnLayout.addWidget(self.__btnDCT)
        btnLayout.addWidget(self.__btniDCT)
        # Adicionando tudo
        centralLayout.addWidget(self.__label1)
        centralLayout.addLayout(btnLayout)
        centralLayout.addWidget(self.__label2)
        # Setando layouts e outros detalhes da janela
        self.setWindowTitle("PDI -- Transformada Discreta do Cosseno")
        centralWidget.setLayout(centralLayout)
        self.setCentralWidget(centralWidget)

    # Chama a função DCT. É passado o valor C existente no ambiente.
    def abrir(self, event):
        # Essa função retorna uma tupla (pathDoArquivo, tipoDoArquivo)
        # Como no nosso caso o arquivo é sempre uma imagem, pego só o path
        pathArquivo = QFileDialog.getOpenFileName(self, "Abrir imagem", "", "Imagens (*.png *.jpg *.bmp)")[0]
        if not pathArquivo:
            return
        # Usa o pillow (PIL, fork) e não o Qt para representar as imagens
        # O Qt meramente as exibe, após uma conversão.
        # Já redimensiona a imagem e a deixa em escala de cinza.
        # Amo o quão fod@-s3 é o Python, pode só declarar um atributo aqui e beleza!
        self.__image1 = Image.open(pathArquivo).convert('L').resize((128, 128))
        # Exibe no label1
        self.__label1.setPixmap(QPixmap.fromImage(ImageQt(self.__image1)))
    
    def fazer_dct(self, event):
        self.statusBar().showMessage("Calculando DCT. Aguarde...")
        QApplication.processEvents() # força a atualização da statusBar (senão ela atrasa)
        C, dct_vmax, dct_vmin = dct(nparray(self.__image1))

        self.statusBar().showMessage("")
        #print(C)

    def fazer_idct(self, event):
        print("fazer idct")
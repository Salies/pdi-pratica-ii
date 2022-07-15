from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QFrame, QMenu, QAction, QFileDialog, QApplication
from PyQt5.QtGui import QPixmap, QImage
# esse Qt é o namespace do Qt, com algumas propriedades (números, valores) predefinidos
# por exemplo o Qt.AlignVCenter em C++ seria Qt::AlignVCenter
from PyQt5.QtCore import Qt, pyqtSignal
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
        menuOp = QMenu("Operações", self)
        pb_action = QAction("Filtro passa-baixa", self)
        pa_action = QAction("Filtro passa-alta", self)
        pb_action.triggered.connect(self.fazer_passa_baixa)
        pa_action.triggered.connect(self.fazer_passa_alta)
        abrir_action = QAction("Abrir", self)
        abrir_action.triggered.connect(self.abrir)
        menuArquivo.addAction(abrir_action)
        menuOp.addAction(pb_action)
        menuOp.addAction(pa_action)
        menubar.addMenu(menuArquivo)
        menubar.addMenu(menuOp)
        # Criando statusBar
        self.statusBar().showMessage("Abra uma imagem")
        # Criando labels pras images
        self.__label1 = QLabel()
        #self.__label2 = QLabel()
        self.__label2 = LabelComTracking()
        self.__label2.clicouSignal.connect(self.pintar_pixel)
        self.__label1.setFixedSize(130, 130)
        self.__label2.setFixedSize(130, 130)
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
        self.__C, dct_vmax, dct_vmin = dct(nparray(self.__image1))
        self.__image2qt = ImageQt(Image.fromarray(normalizar(self.__C, dct_vmax, dct_vmin)).convert("L"))
        self.__label2.setPixmap(QPixmap.fromImage(self.__image2qt))
        self.statusBar().showMessage("DCT concluído.")

    def fazer_idct(self, event):
        self.statusBar().showMessage("Calculando iDCT. Aguarde...")
        QApplication.processEvents()
        self.__image1 = Image.fromarray(idct(self.__C)).convert('L')
        self.__label1.setPixmap(QPixmap.fromImage(ImageQt(self.__image1)))
        self.statusBar().showMessage("iDCT concluído.")

    def fazer_passa_baixa(self, event):
        print("passa-baixa")

    def fazer_passa_alta(self, event):
        print("passa-alta")

    def pintar_pixel(self, pos):
        print("pintar o pixel", pos)
    
# Label com mouse tracking, para podermos
# pintar a posição onde o usuário clicar
class LabelComTracking(QLabel):
    clicouSignal = pyqtSignal(tuple)
    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)

    #def mouseMoveEvent(self, event):
    #    print("passando por cima")

    def mousePressEvent(self, event):
        self.clicouSignal.emit((event.x(), event.y()))
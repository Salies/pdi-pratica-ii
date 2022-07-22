from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QFrame, QMenu, QAction, QFileDialog, QApplication, QSpinBox, QDialog
from PyQt5.QtGui import QPixmap, QIcon
# esse Qt é o namespace do Qt, com algumas propriedades (números, valores) predefinidos
# por exemplo o Qt.AlignVCenter em C++ seria Qt::AlignVCenter
from PyQt5.QtCore import Qt, pyqtSignal
from PIL import Image
from PIL.ImageQt import ImageQt
from numpy import array as nparray
from pdi.dct.dct import dct, idct, passa_baixa_dct, passa_alta_dct
from pdi.slithice import normalize
from pdi.sobre import Sobre

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
        menuAjuda = QMenu("Ajuda", self)
        sobre_action = QAction("Sobre", self)
        sobre_action.triggered.connect(lambda: Sobre('ico/mirana.ico'))
        menuAjuda.addAction(sobre_action)
        self.__menuOp = QMenu("Operações", self)
        pb_action = QAction("Filtro passa-baixa", self)
        pa_action = QAction("Filtro passa-alta", self)
        pb_action.triggered.connect(self.fazer_passa_baixa)
        pa_action.triggered.connect(self.fazer_passa_alta)
        abrir_action = QAction("Abrir", self)
        abrir_action.triggered.connect(self.abrir)
        menuArquivo.addAction(abrir_action)
        self.__menuOp.addAction(pb_action)
        self.__menuOp.addAction(pa_action)
        menubar.addMenu(menuArquivo)
        menubar.addMenu(self.__menuOp)
        menubar.addMenu(menuAjuda)
        self.__menuOp.setEnabled(False)
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
        # Desativando botões para impedir operações com lixo
        self.__btnDCT.setEnabled(False)
        self.__btniDCT.setEnabled(False)
        # Define esse atributo pra poder recusar a operação de inserir ruído
        self.setPodeInversa(False)
        # Setando layouts e outros detalhes da janela
        self.setWindowTitle("PDI -- Transformada Discreta do Cosseno")
        self.setWindowIcon(QIcon('ico/mirana.ico'))
        centralWidget.setLayout(centralLayout)
        self.setCentralWidget(centralWidget)

    # Chama a função DCT. É passado o valor C existente no ambiente.
    def abrir(self, event):
        # Essa função retorna uma tupla (pathDoArquivo, tipoDoArquivo)
        # Como no nosso caso o arquivo é sempre uma imagem, pego só o path
        pathArquivo = QFileDialog.getOpenFileName(self, "Abrir imagem", "", "Imagens (*.png *.jpg *.bmp *.tif)")[0]
        if not pathArquivo:
            return
        # Limpa o painel 2
        # Trava o DCT para não ser realizado com lixo
        # Limpa self.__image2qt pra não pintar lixo
        self.__label2.clear()
        self.__btnDCT.setEnabled(True)
        self.setPodeInversa(False)
        self.__menuOp.setEnabled(True)
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
        # Salva o DCT e o max como atributos -- o DCT pra passar quando o usuário pedir
        # e o máx pra usar como ruído (garante que o ruído vai ser perceptível quando fizer a inversa)
        self.__C, self.__dct_vmax, dct_vmin = dct(nparray(self.__image1))
        self.__image2qt = ImageQt(Image.fromarray(normalize(self.__C, self.__dct_vmax, dct_vmin)).convert("L"))
        self.__label2.setPixmap(QPixmap.fromImage(self.__image2qt))
        # Ativa o botão de inversa e mostra a mensagem de conclusão
        self.setPodeInversa(True)
        self.statusBar().showMessage("DCT concluído.")

    def fazer_idct(self, event):
        self.statusBar().showMessage("Calculando iDCT. Aguarde...")
        QApplication.processEvents()
        self.__image1 = Image.fromarray(idct(self.__C)).convert('L')
        self.__label1.setPixmap(QPixmap.fromImage(ImageQt(self.__image1)))
        self.statusBar().showMessage("iDCT concluído.")

    def fazer_passa_baixa(self, event):
        self.setPodeInversa(False)
        valDialog = FiltroDialog()
        valDialog.corteSignal.connect(self.aplica_passa_baixa)
        valDialog.exec_()

    def fazer_passa_alta(self, event):
        self.setPodeInversa(False)
        valDialog = FiltroDialog()
        valDialog.corteSignal.connect(self.aplica_passa_alta)
        valDialog.exec_()

    def aplica_passa_baixa(self, corte):
        self.aplica_filtro(passa_baixa_dct, corte)

    def aplica_passa_alta(self, corte):
        self.aplica_filtro(passa_alta_dct, corte)

    def aplica_filtro(self, funcao, corte):
        self.statusBar().showMessage("Calculando DCT. Aguarde...")
        QApplication.processEvents()
        C = dct(nparray(self.__image1))[0]
        self.statusBar().showMessage("Aplicando filtro e iDCT. Aguarde...")
        QApplication.processEvents()
        res = idct(funcao(C, corte))
        self.__image2qt = ImageQt(Image.fromarray(res).convert("L"))
        self.__label2.setPixmap(QPixmap.fromImage(self.__image2qt))
        self.statusBar().showMessage("Filtragem concluída.")

    def pintar_pixel(self, pos):
        if not self.__podeInversa:
            return
        # coloca o ruído na matriz real do DCT
        # divido por 5 porque senão o ruído fica MUITO forte
        # x e y vem invertido, inverter aqui
        self.__C[pos[1], pos[0]] = self.__dct_vmax / 5
        # mostar o ruído pro usuário (coloca na QImage e atualiza o pixmap da label)
        # aqui não precisa inverter
        self.__image2qt.setPixel(pos[0], pos[1], 255)
        self.__label2.setPixmap(QPixmap.fromImage(self.__image2qt))
        #print(self.__image2qt.format()) # tem que retornar Indexed8

    def setPodeInversa(self, pode):
        self.__podeInversa = pode
        self.__btniDCT.setEnabled(pode)
    
# Label com mouse tracking, para podermos
# pintar a posição onde o usuário clicar
class LabelComTracking(QLabel):
    clicouSignal = pyqtSignal(tuple)
    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)

    def mousePressEvent(self, event):
        self.clicouSignal.emit((event.x(), event.y()))

# Os dialogs do PyQt são kek, tivemos que fazer o nosso
class FiltroDialog(QDialog):
    corteSignal = pyqtSignal(int)
    def __init__(self):
        super().__init__(None, Qt.WindowSystemMenuHint | Qt.WindowTitleHint)
        self.setWindowTitle("Corte")
        layout = QVBoxLayout()
        okBtn = QPushButton("OK")
        okBtn.clicked.connect(self.aplica)
        self.__spBox = QSpinBox()
        self.__spBox.setMinimum(0)
        self.__spBox.setMaximum(255)
        layout.addWidget(self.__spBox)
        layout.addWidget(okBtn)
        self.setLayout(layout)

    def aplica(self):
        self.close()
        self.corteSignal.emit(self.__spBox.value())

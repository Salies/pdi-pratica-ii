from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QFrame
# esse Qt é o namespace do Qt, com algumas propriedades (números, valores) predefinidos
# por exemplo o Qt.AlignVCenter em C++ seria Qt::AlignVCenter
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__ (self):
        super().__init__()

        # Criando widgets base
        centralWidget = QWidget()
        centralLayout = QHBoxLayout()
        # Criando menuBar
        menubar = self.menuBar()
        # Criando statusBar
        self.statusBar().showMessage("Abra uma imagem")
        # Criando labels pras images
        self.__label1 = QLabel("img1")
        self.__label2 = QLabel("img2")
        self.__label1.setFixedSize(128, 128)
        self.__label2.setFixedSize(128, 128)
        self.__label1.setFrameStyle(QFrame.Box)
        self.__label2.setFrameStyle(QFrame.Box)
        self.__btnDCT = QPushButton("DCT")
        self.__btniDCT = QPushButton("iDCT")
        # Criando os botões pra usar DCT/iDCT
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
''' 
Este programa é parte dos trabalhos práticos do segundo bimestre 
da disciplina de Processamento Digital de Imagens,
ministrada na FCT-UNESP em 2022.

Autores:
Carlos Eduardo Fernandes de Santana
Daniel Henrique Serezane Pereira

///

Aula 10.3
Prática - Implementar o método de OTSU, para usá-lo na limiarização e binarização, já implementados
'''

from PIL import Image
import numpy as np
from numba import njit
from pdi.slithice import gerar_histograma, binarizacao, limiarizacao
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog, QPushButton, QHBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

# Otsu
# Código baseado em uma versão recente do Gonzalez (2020, ISBN 9780982085417)
# pág. 656-657
@njit
def otsu(img, l):
    p = gerar_histograma(img, 256) / img.size
    o_max = -np.inf
    k_ast = 0
    # Para cada tom k possíel
    for k in range(l):
        P1 = 0
        for i in range(k + 1):
            P1 += p[i]
        mg = 0
        for i in range(l):
            mg += i * p[i]
        mk = 0
        for i in range(k + 1):
            mk += i * p[i]
        if P1 == 1 or P1 == 0:
            continue
        o = (((mg * P1) - mk) ** 2) / (P1 * (1 - P1))
        if(o > o_max):
            o_max = o
            k_ast = k
    return k_ast

# Interface gráfica simples
# Seletor de operação
class Seletor(QDialog):
    def __init__ (self, callback_lim, callback_bin):
        super().__init__()
        self.__callback_lim = callback_lim
        self.__callback_bin = callback_bin
        self.setWindowTitle("Selecione uma operação")
        self.setWindowIcon(QIcon('ico/ember.ico'))
        limBtn = QPushButton("Limiarização")
        binBtn = QPushButton("Binarização")
        limBtn.clicked.connect(self.clim)
        binBtn.clicked.connect(self.cbin)
        l = QHBoxLayout()
        l.addWidget(limBtn)
        l.addWidget(binBtn)
        self.setLayout(l)

    def cbin(self):
        self.close()
        self.__callback_bin()

    def clim(self):
        self.close()
        self.__callback_lim()

def main():
    _ = QApplication([])
    _.setAttribute(Qt.AA_DisableWindowContextHelpButton)

    pathArquivo = QFileDialog.getOpenFileName(None, "Abrir imagem", "", "Imagens (*.png *.jpg *.bmp *.tif)")[0]
    if not pathArquivo:
        return
    
    im = Image.open(pathArquivo).convert('L')
    img = np.array(im)
    limiar = otsu(img, 256)

    call_lim = lambda: Image.fromarray(limiarizacao(img, limiar)).convert('L').show()
    call_bin = lambda: Image.fromarray(binarizacao(img, limiar)).convert('1').show()

    s = Seletor(call_lim, call_bin)
    s.exec_()


if __name__ == "__main__":
    main()
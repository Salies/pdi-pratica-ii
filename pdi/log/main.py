''' 
Este programa é parte dos trabalhos práticos do segundo bimestre 
da disciplina de Processamento Digital de Imagens,
ministrada na FCT-UNESP em 2022.

Autores:
Carlos Eduardo Fernandes de Santana
Daniel Henrique Serezane Pereira

///

Aula 10.1
Prática:
1) Implementar o Laplaciano e o Laplaciano da Gaussiana (LoG) exibindo os dois resultados lado a lado
2) Normalizar ou Equalizar as imagens resultantes, para uma boa visualização
'''

from PIL import Image, ImageDraw, ImageFont
import numpy as np
from pdi.slithice import conv, normalize
from PyQt5.QtWidgets import QApplication, QFileDialog

def main():
    _ = QApplication([]) # O meu nome é gambiarra!
    pathArquivo = QFileDialog.getOpenFileName(None, "Abrir imagem", "", "Imagens (*.png *.jpg *.bmp *.tif)")[0]
    if not pathArquivo:
        return

    im = Image.open(pathArquivo).convert("L")

    l = np.array([
        [0, -1, 0],
        [-1, 4, -1],
        [0, -1, 0]
    ])

    lg = np.array([
        [0, 0, -1, 0, 0],
        [0, -1, -2, -1, 0],
        [-1, -2, 16, -2, -1],
        [0, -1, -2, -1, 0],
        [0, 0, -1, 0, 0]
    ])

    im_l = conv(np.array(im), l)
    im_l_n = normalize(im_l, np.max(im_l), np.min(im_l))

    im_lg = conv(np.array(im), lg)
    im_lg_n = normalize(im_lg, np.max(im_lg), np.min(im_lg))

    # Croppando a laplaciana, porque ela tem 1px a mais de cada lado do que a LoG
    # dado os tamanhos dos filtros
    im_l_n = im_l_n[1:-1, 1:-1]
    
    # Adicionando texto
    im_l_n = Image.fromarray(im_l_n)
    im_lg_n = Image.fromarray(im_lg_n)
    font = ImageFont.truetype("ttf/NotoSansMono-Bold.ttf", size=14)
    ImageDraw.Draw(im_l_n).text((0, 0), 'Laplaciano', 255, font=font)
    ImageDraw.Draw(im_lg_n).text((0, 0), 'Laplaciano da Gaussiana (LoG)', 255, font=font)

    # Juntando as duas imagens e exibindo
    Image.fromarray(np.hstack((np.array(im_l_n),np.array(im_lg_n)))).show()

if __name__ == "__main__":
    main()
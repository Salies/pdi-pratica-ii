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
import numpy as np
from numba import njit
from PIL import Image

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

im = Image.open("imagens/teste.bmp").convert("1")
dil = erodir(np.array(im))
print(dil)
Image.fromarray(dil).show()
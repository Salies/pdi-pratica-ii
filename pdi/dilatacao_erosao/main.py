''' 
Este programa é parte dos trabalhos práticos do segundo bimestre 
da disciplina de Processamento Digital de Imagens,
ministrada na FCT-UNESP em 2022.

Autores:
Carlos Eduardo Fernandes de Santana
Daniel Henrique Serezane Pereira

///

Aula 12
Prática - Implemente a operação de dilatação e erosão de imagens binárias
'''
import numpy as np

def dilatar(img):
    # Matriz de dilatação
    masc = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])
    # Cria uma imagem com o mesmo tamanho da original
    img_dil = np.zeros(img.shape, dtype=np.uint8)
    # Para cada pixel da imagem original
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            img_dil[i, j] = 0 # Pixel preto
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            cor = img_dil[i, j]
            # Para cada vizinho do pixel atual
            if cor > 0:
                for ii in range(-1, 1):
                    for jj in range(-1, 1):
                        if masc[ii+1, jj+1] == 1:
                            img_dil[i + ii, j + jj] = 1 # Pixel branco
    return img_dil

def erodir(img):
    # Matriz de erosão
    masc = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])
    # Cria uma imagem com o mesmo tamanho da original
    img_ero = np.zeros(img.shape, dtype=np.uint8)
    # Para cada pixel da imagem original
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            img_ero[i, j] = 0 # Pixel preto
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            cor = img_ero[i, j]
            # Para cada vizinho do pixel atual
            if cor > 0:
                remove = False
                for ii in range(-1, 1):
                    for jj in range(-1, 1):
                        if masc[ii+1, jj+1] == 1 and img_ero[i + ii, j + jj] == 0:
                            remove = True
                if remove:
                    img_ero[i, j] = 0
                else:
                    img_ero[i, j] = 1
    return img_ero
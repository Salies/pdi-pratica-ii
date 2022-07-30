''' 
Este programa é parte dos trabalhos práticos do segundo bimestre 
da disciplina de Processamento Digital de Imagens,
ministrada na FCT-UNESP em 2022.

Autores:
Carlos Eduardo Fernandes de Santana
Daniel Henrique Serezane Pereira

///

Aula 11
Trabalho Prático
Implementar o afinamento de objetos, para a obtenção de Esqueletos de imagens binárias usando o algoritmo de Zhang e Suen. 
Usar a imagem teste.bmp para demonstrar observe que esta imagem tem objeto branco e fundo preto.
O algoritmo deve ser aplicado apenas nos pontos de borda, entretanto, pode ser aplicado em todos os pontos  da imagem, gerando um processamento maior 
o resultado obtido com este algoritmo será comparado com o resultado obtido pela operação de erosão, visto na próxima aula
'''

import numpy as np
from numba import njit

@njit
def vizinhos(i, j, img):
    return [
            img[i - 1, j], # p[2] -- 0
            img[i - 1, j + 1], # p[3] -- 1
            img[i, j + 1], # p[4] -- 2
            img[i + 1, j + 1], # p[5] -- 3
            img[i + 1, j], # p[6] -- 4
            img[i + 1, j - 1], # p[7] -- 5
            img[i, j - 1], # p[8] -- 6
            img[i - 1, j - 1] # p[9] -- 7
    ]

@njit
def S(p):
    aux = np.append(p, p[0]) # coloca o p2 no final
    s = 0
    for k in range(len(aux) - 1):
        if (aux[k], aux[k + 1]) == (False, True):
            s += 1
    return s

# TODO (não necessário): limpar o código (loops -> funções)
@njit
def zhang_suen(img):
    out = img.copy()
    mar_p1 = [(0, 0)] # pixels marcados para remoção, passo 1 -- não há do while em Python
    mar_p2 = [(0, 0)] # tem que deixar assim (elemento dummy tupla), senão o numba não jita
    # loopa enquanto houverem pixels marcados em cada um dos passos
    while len(mar_p1) != 0 or len(mar_p2) != 0:
        # Inicializa o array de marcados -- cada ponto é uma tupla de coordenadas
        mar_p1 = mar_p2 = []
        # Passo 1
        # Ignora pixels na borda da imagem
        for i in range(1, img.shape[0] - 1):
            for j in range(1, img.shape[1] - 1):
                if(out[i, j] == False): # pixels pretos não podem ser de borda
                    continue
                p = vizinhos(i, j, out)
                if(sum(p) == 8): # se tem 8 vizinhos brancos não é pixel de borda
                    continue
                # Se batarem as condições, marcar para eliminação
                if ((2 <= sum(p) <= 6) and (S(p) == 1) and (p[0] * p[2] * p[4] == 0) and (p[2] * p[4] * p[6] == 0)):
                    mar_p1.append((i, j))
        # Elimina os pixels
        for i, j in mar_p1:
            out[i, j] = False
        # Passo 2 -- mesma coisa, só mudam os vizinhos das condições c) e d) (TODO)
        for i in range(1, img.shape[0] - 1):
            for j in range(1, img.shape[1] - 1):
                if(out[i, j] == False):
                    continue
                p = vizinhos(i, j, out)
                if(sum(p) == 8):
                    continue
                if ((2 <= sum(p) <= 6) and (S(p) == 1) and (p[0] * p[2] * p[6] == 0) and (p[0] * p[4] * p[6] == 0)):
                    mar_p2.append((i, j))
        for i, j in mar_p2:
            out[i, j] = False
    return out
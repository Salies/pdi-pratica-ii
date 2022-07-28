from PIL import Image
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

# Não vou jitar porque esse truque do Python é muito conveniente
# e buga de eu jitar
@njit
def S(p):
    aux = np.append(p, p[0]) # coloca o p2 no final
    s = 0
    for k in range(len(aux) - 1):
        if (aux[k], aux[k + 1]) == (False, True):
            s += 1
    return s

@njit
def zhang_suen(img):
    out = img.copy()
    mar_p1 = [(0, 0)] # pixels marcados para remoção, passo 1 -- não há do while em Python
    mar_p2 = [(0, 0)] # tem que deixar assim (elemento dummy tupla), senão o numba não jita
    # loopa enquanto houverem pixels marcados em cada um dos passos
    while len(mar_p1) != 0 or len(mar_p2) != 0:
        # Passo 1
        mar_p1 = []
        # Ignora pixels na borda da imagem
        for i in range(1, img.shape[0] - 1):
            for j in range(1, img.shape[1] - 1):
                if(out[i, j] == False): # pixels pretos não podem ser de borda
                    continue
                p = p2, p3, p4, p6, p6, p7, p8, p9 = vizinhos(i, j, out)
                if(sum(p) == 8): # se tem 8 vizinhos brancos não é pixel de borda
                    continue
                # Se batarem as condições, marcar para eliminação
                if (2 <= sum(p) <= 6 and S(p) == 1 and p2 * p4 * p6 == 0 and p4 * p6 * p8 == 0):
                    mar_p1.append((i, j))
        # Elimina os pixels
        for i, j in mar_p1:
            out[i, j] = False
        # Passo 2
        mar_p2 = []
        for i in range(1, img.shape[0] - 1):
            for j in range(1, img.shape[1] - 1):
                if(out[i, j] == False):
                    continue
                p = p2, p3, p4, p6, p6, p7, p8, p9 = vizinhos(i, j, out)
                if(sum(p) == 8):
                    continue
                if (2 <= sum(p) <= 6 and S(p) == 1 and p2 * p4 * p8 == 0 and p2 * p6 * p8 == 0):
                    mar_p2.append((i, j))
        for i, j in mar_p2:
            out[i, j] = False
    return out

    
# Abrindo como imagem binária
# na pillow:
#   False   :   pixel preto
#   True    :   pixel branco
im = Image.open("imagens/teste.bmp").convert('1')
#a = vizinhos(1, 1, np.array(im))
#print(a)
#print(a.dtype)
#b = np.array([False, True, False, True, False, False, True, True, False])
#print(S(b))
'''o = Image.fromarray(zhang_suen(np.array(im)))
o.show()'''
Image.fromarray(zhang_suen(np.array(im))).show()
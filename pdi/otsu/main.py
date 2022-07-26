from PIL import Image
import numpy as np
from numba import njit
from pdi.slithice import gerar_histograma, binarizacao

# Código baseado em uma versão recente do Gonzalez
# (salvo em Drive pessoal, não distribuído no repo por questões de direitos autorais)
@njit
def otsu(img, l):
    n = img.shape[0] * img.shape[1]
    p = gerar_histograma(img, 256) / n
    o_max = -np.inf
    k_ast = 0
    # Para cada tom k possíel
    for k in range(l):
        P1 = 0
        for i in range(k):
            P1 += p[i]
        mg = 0
        for i in range(l):
            mg += i * p[i]
        mk = 0
        for i in range(k):
            mk += i * p[i]
        if P1 == 1 or P1 == 0:
            continue
        o = (((mg * P1) - mk) ** 2) / (P1 * (1 - P1))
        if(o > o_max):
            o_max = o
            k_ast = k
    return k_ast

im = Image.open("imagens/Image_processing_pre_otsus_algorithm.jpg").convert('L')
img = np.array(im)
limiar = otsu(img, 256)
print(limiar)
#print(limiar)
Image.fromarray(binarizacao(img, limiar)).show()

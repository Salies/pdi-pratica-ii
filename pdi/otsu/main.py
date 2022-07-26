from PIL import Image
import numpy as np
from numba import njit
from pdi.slithice import gerar_histograma, binarizacao

@njit
def otsu(img, l):
    n = img.shape[0] * img.shape[1]
    p = gerar_histograma(img, 256) / n
    o = np.empty(l)
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
            o[k] = 0
            continue
        o[k] = (((mg * P1) - mk) ** 2) / (P1 * (1 - P1))
    return np.argmax(o) # pega o que maximiza a variância

im = Image.open("imagens/Image_processing_pre_otsus_algorithm.jpg").convert('L')
img = np.array(im)
limiar = otsu(img, 256)
#print(limiar)
Image.fromarray(binarizacao(img, limiar)).show()

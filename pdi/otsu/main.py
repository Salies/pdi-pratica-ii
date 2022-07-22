from PIL import Image
import numpy as np
from numba import njit
from pdi.slithice import gerar_histograma, limiarizacao, binarizacao

@njit
def otsu(img, l):
    n = img.shape[0] * img.shape[1]
    eta = np.zeros(l)
    for t in range(l):
        a = limiarizacao(img, t)
        p = gerar_histograma(a, l)
        # p agora diz quanto de cada tom há na imagem
        # Basta então dividir pela quantidade total de pixels
        p /= n
        u_T = 0
        for i in range(l):
            u_T += i * p[i]
        sigma2_T = 0
        for i in range(l):
            sigma2_T += ((i - u_T) ** 2) * p[i]
        omega_0 = 0
        for i in range(t + 1):
            omega_0 += p[i]
        omega_1 = 1 - omega_0
        u_t = 0
        for i in range(t + 1):
            u_t = i * p[i]
        u_1 = (u_T - u_t) / (1 - omega_0)
        u_0 = u_t / omega_0
        sigma2_B = omega_0 * omega_1 * ((u_1 * u_0) ** 2)
        eta[t] = sigma2_B / sigma2_T
    return np.argmin(eta)

im = Image.open("imagens/Image_processing_pre_otsus_algorithm.jpg")
img = np.array(im)
limiar = otsu(img, 256)
print(limiar)
Image.fromarray(binarizacao(img, limiar)).show()

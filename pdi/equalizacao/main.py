from PIL import Image, ImageChops
import numpy as np
from numba import njit
from pdi.slithice import rgb_para_hsl, hsl_para_rgb, eq_histograma_img

@njit
def equalizar_img_por_l(img):
    l_array = np.empty(img.shape[:2], dtype=np.uint8)
    img_hsl = np.empty(img.shape)
    width, height = img.shape[:2]
    aux = np.empty(3)
    # Convertendo pra HSL
    for i in range(width):
        for j in range(height):
            r, g, b = img[i][j]
            #h, s, l
            aux[0], aux[1], aux[2] = rgb_para_hsl(r, g, b)
            # Infelizmente tem que arredondar o l pra poder equalizar depois
            # O resto deixo igual, para tentar manter a precisão
            l_array[i][j] = np.rint(aux[2])
            img_hsl[i][j] = aux

    # Equalizando
    l_eq = eq_histograma_img(l_array, 241)

    # Voltando pra RGB
    img_eq = np.empty(img.shape)
    for i in range(width):
        for j in range(height):
            h, s, l = img_hsl[i][j]
            l = l_eq[i][j]
            # r, g, b
            aux[0], aux[1], aux[2] = hsl_para_rgb(h, s, l)
            img_eq[i][j] = aux

    return img_eq
   

im = Image.open("imagens/Fig0638(a)(lenna_RGB).tif").convert("RGB")
im_eq = Image.fromarray(equalizar_img_por_l(np.array(im)).astype(np.uint8))

im.show()
im_eq.show()


from PIL import Image, ImageChops
import numpy as np
from pdi.slithice import rgb_para_hsl, hsl_para_rgb, eq_histograma_img

# Fig0638(a)(lenna_RGB).tif
img = Image.open("imagens/Fig0638(a)(lenna_RGB).tif").convert("RGB")
img_array = np.array(img)
l_array = np.empty(img_array.shape[:2], dtype=np.uint8)
img_hsl = np.empty(img_array.shape)
width, height = img_array.shape[:2]
for i in range(width):
    for j in range(height):
        r, g, b = img_array[i][j]
        # Infelizmente tem que arredondar pra poder equalizar depois
        h, s, l = np.rint(rgb_para_hsl(r, g, b))
        l_array[i][j] = l
        img_hsl[i][j] = np.array([h, s, l])

l_eq = eq_histograma_img(l_array, 241)

img_teste = np.empty(img_array.shape)
for i in range(width):
    for j in range(height):
        h, s, l = img_hsl[i][j]
        l = l_eq[i][j]
        r, g, b = hsl_para_rgb(h, s, l)
        img_teste[i][j] = np.array([r, g, b])

iii = Image.fromarray((img_teste).astype(np.uint8))
img.show()
iii.show()


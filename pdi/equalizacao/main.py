from PIL import Image, ImageChops
import numpy as np
from pdi.slithice import rgb_para_hsl, hsl_para_rgb

# Fig0638(a)(lenna_RGB).tif
img = Image.open("imagens/Fig0638(a)(lenna_RGB).tif").convert("RGB")
img_array = np.array(img)
img_hsl = np.empty(img_array.shape)
width, height = img_array.shape[:2]
for i in range(width):
    for j in range(height):
        r, g, b = img_array[i][j]
        h, s, l = rgb_para_hsl(r, g, b)
        img_hsl[i][j] = np.array([h, s, l])

img_teste = np.empty(img_array.shape)
for i in range(width):
    for j in range(height):
        h, s, l = img_hsl[i][j]
        r, g, b = hsl_para_rgb(h, s, l)
        img_teste[i][j] = np.array([r, g, b])

print(img_teste.shape)
iii = Image.fromarray((img_teste).astype(np.uint8))
aaa = ImageChops.subtract(img, iii)
print(np.linalg.norm(np.array(aaa)))
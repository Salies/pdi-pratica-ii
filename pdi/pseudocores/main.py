from PIL import Image
from numpy import array as nparray, empty



# Abrindo imagem e representando como matriz
# Já fazemos a conversão de escala de cinza para RGB
# (a imagem de mantém cinza, mas cara tom agora está em RGB e não em apenas um uchar)
img = nparray(Image.open("imagens/Fig0622(a)(tropical_rain_grayscale.tif").convert('RGB'))
#print(img)

width, height = img.shape[:2]

# Loopando e aplicando pseudocores
subs = empty(3)
for i in range(width):
    for j in range(height):
        cor = img[i, j][0]
        if(cor < 64):
            subs[0] = 0
            subs[1] = 0
            subs[2] = cor * 4
        elif(cor >= 64 and cor < 128):
            subs[0] = 0
            subs[1] = (cor - 64) * 4
            subs[2] = 255
        elif(cor >= 128 and cor < 192):
            subs[0] = 0
            subs[1] = 255
            subs[2] = 255 - ((cor - 128) * 4)
        elif(cor >= 192):
            subs[0] = (cor - 192) * 4
            subs[1] = 255
            subs[2] = 0
        img[i, j] = subs

img = Image.fromarray(img)
img.show() 
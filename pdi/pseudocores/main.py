from PIL import Image
from numpy import array as nparray, empty
from numba import njit

@njit
def colorizar(img):
    width, height = img.shape[:2]

    # Loopando e aplicando pseudocores
    subs = empty(3)
    for i in range(width):
        for j in range(height):
            tom = img[i, j][0]
            if(tom < 64):
                subs[0] = 0
                subs[1] = 0
                subs[2] = tom * 4
            elif(tom >= 64 and tom < 128):
                subs[0] = 0
                subs[1] = (tom - 64) * 4
                subs[2] = 255
            elif(tom >= 128 and tom < 192):
                subs[0] = 0
                subs[1] = 255
                subs[2] = 255 - ((tom - 128) * 4)
            elif(tom >= 192):
                subs[0] = (tom - 192) * 4
                subs[1] = 255
                subs[2] = 0
            img[i, j] = subs

# Abrindo imagem e representando como matriz
# Já fazemos a conversão de escala de cinza para RGB
# (a imagem mantém-se cinza, mas cada tom agora está em uma cor RGB)
img = nparray(Image.open("imagens/Fig0622(a)(tropical_rain_grayscale.tif").convert('RGB'))

colorizar(img)

# Remontando e exibindo a imagem após a colorização
img = Image.fromarray(img)
img.show() 
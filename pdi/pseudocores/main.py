''' 
Este programa é parte dos trabalhos práticos do segundo bimestre 
da disciplina de Processamento Digital de Imagens,
ministrada na FCT-UNESP em 2022.

Autores:
Carlos Eduardo Fernandes de Santana
Daniel Henrique Serezane Pereira

///

Aula 10.1
Prática:
1) Implementar o Laplaciano e o Laplaciano da Gaussiana (LoG) exibindo os dois resultados lado a lado
2) Normalizar ou Equalizar as imagens resultantes, para uma boa visualização
'''

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
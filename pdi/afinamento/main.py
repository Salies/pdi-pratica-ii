from PIL import Image
import numpy as np

'''
for (int k = -1; k <= 1; k++) {
    for (int l = -1; l <= 1; l++) {
        if (0 <= i + k && i + k < height && 0 <= j + l && j + l < width) {
            array_size++;
        }
    }
}
'''

# Retorna a posição dos vizinhos de um pixel
def get_vizinhos(i, j, w, h):
    v = []
    for k in range (-1, 2):
        for l in range(-1, 2):
            if((k, l) != (0, 0) and 0 <= i + k and i + k < h and 0 <= j + l and j + l < w):
                v.append((i + k, j + l))
    return v

# Abrindo como imagem binária
# na pillow:
#   False   :   pixel preto
#   True    :   pixel branco
#im = Image.open("imagens/teste.bmp").convert('1')
#print(np.array(im))

a = get_vizinhos(4, 4, 5, 5)
print(a)
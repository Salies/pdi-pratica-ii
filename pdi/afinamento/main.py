from PIL import Image
import numpy as np
from numba import njit

'''
for (int k = -1; k <= 1; k++) {
    for (int l = -1; l <= 1; l++) {
        if (0 <= i + k && i + k < height && 0 <= j + l && j + l < width) {
            array_size++;
        }
    }
}
'''

@njit
def zhang_suen(img):
    out = img.copy()
    # Não tem do while em Python =/
    a = 0
    while True:
        if(a > 1000): break
        print("it", a)

        mar = np.zeros(img.shape, dtype=np.uint8)
        # Ignorando as bordas da imagem
        for i in range(1, img.shape[0] - 1):
            for j in range(1, img.shape[1] - 1):
                if(img[i, j] == 0):
                    continue
                p = [
                    img[i - 1, j], # p[2] -- 0
                    img[i - 1, j + 1], # p[3] -- 1
                    img[i, j + 1], # p[4] -- 2
                    img[i + 1, j + 1], # p[5] -- 3
                    img[i + 1, j], # p[6] -- 4
                    img[i + 1, j - 1], # p[7] -- 5
                    img[i, j - 1], # p[8] -- 6
                    img[i - 1, j - 1] # p[9] -- 7
                ]
                N = sum(p)
                # Se N = 8 e img[i, j] = 1, não é pixel de borda
                if(N == 8):
                    continue
                # "pontuação" do algoritmo -- se atingir 4, é marcado pra eliminação
                # TODO: decompor em funções
                score = 0
                if(N >= 2 and N <= 6):
                    score += 1
                S = 0
                for k in range(-1, 6): # tem que dar a volta
                    if(p[k + 1] != p[k]):
                        S += 1
                if(S == 1):
                    score += 1
                if(p[0] * p[2] * p[4] == 0):
                    score += 1
                if(p[2] * p[4] * p[6] == 0):
                    score += 1
                if(score == 4):
                    mar[i, j] = 255
        out -= mar
        mar = np.zeros(img.shape, dtype=np.uint8)
        for i in range(1, img.shape[0] - 1):
            for j in range(1, img.shape[1] - 1):
                p = [
                    out[i - 1, j], # p[2] -- 0
                    out[i - 1, j + 1], # p[3] -- 1
                    out[i, j + 1], # p[4] -- 2
                    out[i + 1, j + 1], # p[5] -- 3
                    out[i + 1, j], # p[6] -- 4
                    out[i + 1, j - 1], # p[7] -- 5
                    out[i, j - 1], # p[8] -- 6
                    out[i - 1, j - 1] # p[9] -- 7
                ]
                # Se N = 8 e img[i, j] = 1, não é pixel de borda
                if(N == 8 and img[i, j] == 255):
                    continue
                # "pontuação" do algoritmo -- se atingir 4, é marcado pra eliminação
                # TODO: decompor em funções
                score = 0
                if(N >= 2 and N <= 6):
                    score += 1
                S = 0
                for k in range(-1, 6): # tem que dar a volta
                    if(p[k + 1] != p[k]):
                        S += 1
                if(S == 1):
                    score += 1
                if(p[0] * p[2] * p[6] == 0):
                    score += 1
                if(p[0] * p[4] * p[6] == 0):
                    score += 1
                if(score == 4):
                    mar[i, j] = 255
        out -= mar
        # Não há mais pixels eliminados
        print(mar)
        if(np.sum(mar) == 0):
            break
        a += 1
    return out
    
# Abrindo como imagem binária
# na pillow:
#   False   :   pixel preto
#   True    :   pixel branco
im = Image.open("imagens/teste.bmp").convert('L')
o = Image.fromarray(zhang_suen(np.array(im)))
o.show()
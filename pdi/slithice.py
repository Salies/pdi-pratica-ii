'''
    Slithice - Biblioteca para processamento de imagens em Python

    Um port de algumas funções da versão original da biblioteca,
    escrita em C++ para Qt. Esta versão é baseada em arrays da
    biblioteca numpy, e utiliza o numba para acelerar os cáclulos.
    Os comentários agora estão em Português, mas os nomes de funções
    e variáveis permanecem em Inglês, para maior legibilidade do código,
    visto que todas as instruções da linguagem de programação e suas
    respectivas bibliotecas também são em Inglês.

    Copyright (C) 2022 Daniel Serezane

    Slithice is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Slithice is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Slithice.  If not, see <https://www.gnu.org/licenses/>
'''

import numpy as np
from numba import njit

@njit
def normalize(img, v_max, v_min):
    if (v_max == v_min):
        return

    out = np.empty(img.shape)
    for i, j in np.ndindex(img.shape):
        out[i, j] = np.round(((img[i, j] - v_min)*( 255 / (v_max-v_min))))
    
    return out

'''
void slithice::convolution(const QImage& in, float* kernel, int k_width, int k_height, QImage& out) {
    out = in.copy(); // keep corners

    const int img_width = in.width(), img_height = in.height(),
        k_center_j = k_width >> 1, k_center_i = k_height >> 1;
    int offsetJ = 0, offsetI = 0, lim_j = 0, lim_i = 0, acc_color;
    uchar* bitsB;

    for (int j = k_center_j; j < img_height - k_center_j; j++) {
        bitsB = out.scanLine(j);
        for (int i = k_center_i; i < img_width - k_center_i; i++) {
            acc_color = 0;
            for (int mj = 0; mj < k_height; mj++) {
                // The convolution kernel is mirrored.
                offsetJ = k_height - mj - 1;
                lim_j = j + k_center_i - offsetJ;
                const uchar *bits = in.constScanLine(lim_j);
                for (int mi = 0; mi < k_width; mi++) {
                    offsetI = k_width - mi - 1;
                    lim_i = i + k_center_j - offsetI;
                    if (lim_j >= 0 && lim_j < img_height && lim_i >= 0 && lim_i < img_width) {
                        acc_color += bits[lim_i] * kernel[(k_width * offsetJ) + offsetI];
                    }
                }
            }
            bitsB[i] = acc_color;
        }
    }
}
'''

# Aplica um filtro qualquer a uma imagem.
# O parâmetro filter é uma função. Adaptado do código original da mediana:
# https://github.com/Salies/slithice/blob/main/slithice.cpp#L220
@njit
def filter(img, filter, f_width, f_height):
    out = img.copy() # copia-se e subistui para manters os cantos originais da imagem

    (img_width, img_height) = img.shape
    f_center_j = f_width >> 1
    f_center_i = f_height >> 1
    vec_f = np.empty(f_width * f_height) # vetor acumulador de pixels para o filtro

    for j in range(f_center_j, img_height - k_center_j):
        for i in range(j_center_i, img_width - j_center_i):
            pos = 0 # posição atual do vetor acumulador de pixels do filtro
            for mj in range(f_height):
                # Não sei se aqui isso faz muita diferença ou se só na convolução que faz,
                # mas vou deixar mesmo assim
                offsetJ = f_height - mj - 1
                lim_j = j + f_center_i - offsetJ
                for mi in range(f_width):
                    offsetI = f_width - mi - 1
                    lim_i = i + f_center_j - offsetI
                    if(lim_j >= 0 and lim_j < f_height and lim_i >= 0 and lim_i < img_height):
                        vec_f[pos] = img[lim_i][lim_j]
                        pos += 1
            out[i][j] = filtro(vec_f) # define o pixel como o resultado da filtragem, seja lá qual ela for
    
    return out

# Convolução genérica
# Adaptado da função original:
# https://github.com/Salies/slithice/blob/main/slithice.cpp#L132
@njit
def convolution(img, kernel, k_width, k_height, v_max = -(np.inf), v_min = np.inf):
    out = img.copy() # copia-se e subistui para manters os cantos originais da imagem

    (img_width, img_height) = img.shape
    k_center_j = k_width >> 1
    k_center_i = k_height >> 1

    for j in range(k_center_j, img_height - k_center_j):
        for i in range(j_center_i, img_width - j_center_i):
            acc_color = 0
            for mj in range(k_height):
                offsetJ = k_height - mj - 1
                lim_j = j + k_center_i - offsetJ
                for mi in range(k_width):
                    offsetI = k_width - mi - 1
                    lim_i = i + k_center_j - offsetI
                    if(lim_j >= 0 and lim_j < k_height and lim_i >= 0 and lim_i < img_height):
                        acc_color += img[lim_i][lim_j] * kernel[offsetI][offsetJ]
            out[i][j] = acc_color
            if(acc_color < v_min):
                v_min = acc_color
            if(acc_color > v_max):
                v_max = acc_color
    
    return out, v_max, v_min # retorna o máximo e mínimo, pra normalizar depois
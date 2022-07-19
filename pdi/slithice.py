'''
    Slithice - Biblioteca para processamento de imagens em Python

    Um port de algumas funções da versão original da biblioteca,
    escrita em C++ para Qt. Esta versão é baseada em arrays da
    biblioteca numpy, e utiliza o numba para acelerar os cáclulos.
    Os comentários agora estão em Português. Alguns nomes foram mantidos
    em Inglês para maior coesão com a linguagem.

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

# Aplica um filtro qualquer a uma imagem.
# O parâmetro filter é uma função. Adaptado do código original da mediana:
# https://github.com/Salies/slithice/blob/main/slithice.cpp#L220
@njit
def filter_image(img, filter, f_width, f_height):
    out = img.copy() # copia-se e subistui para manters os cantos originais da imagem

    (img_width, img_height) = img.shape
    print
    f_center_j = f_width >> 1
    f_center_i = f_height >> 1
    vec_f = np.zeros(f_width * f_height) # vetor acumulador de pixels para o filtro

    for j in range(f_center_j, img_height - f_center_j):
        for i in range(f_center_i, img_width - f_center_i):
            pos = 0 # posição atual do vetor acumulador de pixels do filtro
            for mj in range(f_height):
                # Não sei se aqui isso faz muita diferença ou se só na convolução que faz,
                # mas vou deixar mesmo assim
                offsetJ = f_height - mj - 1
                lim_j = j + f_center_i - offsetJ
                for mi in range(f_width):
                    offsetI = f_width - mi - 1
                    lim_i = i + f_center_j - offsetI
                    if(lim_j >= 0 and lim_j < img_height and lim_i >= 0 and lim_i < img_width):
                        vec_f[pos] = img[lim_i][lim_j]
                        pos += 1
            out[i][j] = filter(vec_f) # define o pixel como o resultado da filtragem, seja lá qual ela for
    
    return out

# Convolução genérica
# Adaptado da função original:
# https://github.com/Salies/slithice/blob/main/slithice.cpp#L132
@njit
def conv(img, kernel, k_width, k_height, v_max = -(np.inf), v_min = np.inf):
    out = img.copy() # copia-se e subistui para manters os cantos originais da imagem

    (img_width, img_height) = img.shape
    k_center_j = k_width >> 1
    k_center_i = k_height >> 1

    for j in range(k_center_j, img_height - k_center_j):
        for i in range(k_center_i, img_width - k_center_i):
            acc_color = 0
            for mj in range(k_height):
                offsetJ = k_height - mj - 1
                lim_j = j + k_center_i - offsetJ
                for mi in range(k_width):
                    offsetI = k_width - mi - 1
                    lim_i = i + k_center_j - offsetI
                    if(lim_j >= 0 and lim_j < img_height and lim_i >= 0 and lim_i < img_width):
                        acc_color += img[lim_i][lim_j] * kernel[offsetI][offsetJ]
            out[i][j] = acc_color
            if(acc_color < v_min):
                v_min = acc_color
            if(acc_color > v_max):
                v_max = acc_color
    
    return out, v_max, v_min # retorna o máximo e mínimo, pra normalizar depois
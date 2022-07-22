'''
    Slithice - Biblioteca para processamento de imagens em Python

    Um port de algumas funções da versão original da biblioteca,
    escrita em C++ para Qt. Esta versão é baseada em arrays da
    biblioteca numpy, e utiliza o numba para acelerar os cáclulos.
    Os comentários agora estão em Português. Alguns nomes foram mantidos
    em Inglês para maior coesão com a linguagem, ou porquê foram simplesmente
    mantidos da versão original da biblioteca, em C++.

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
        out[i, j] = np.round(((img[i, j] - v_min) * ( 255 / (v_max - v_min))))
    
    return out

# Função filtro simplificada, baseada na convolução (abaixo)
@njit
def filtra_imagem(img, filtro, fil_w, fil_h):
    img_w, img_h = img.shape

    out_w = img_w - fil_w + 1
    out_h = img_h - fil_h + 1

    out = np.empty((out_w, out_h))

    for i in range(out_w):
        for j in range(out_h):
            out[i][j] = filtro(img[i:i + fil_w, j:j + fil_h].flatten())
    
    return out

# Função convolução simplificada, usando o potencial da linguagem Python
# Não mantém as bordas da imagem original, como na Slithice C++
# Ao invés disso, retorna uma imagem com as bordas cortadas
@njit
def conv(img, kernel):
    img_w, img_h = img.shape
    ker_w, ker_h = kernel.shape

    # Ao invés de definir o tamanho das bordas,
    # já define o tamanho da imagem de saída
    out_w = img_w - ker_w + 1
    out_h = img_h - ker_h + 1

    out = np.empty((out_w, out_h))

    for i in range(out_w):
        for j in range(out_h):
            out[i][j] = np.sum(img[i:i + ker_w, j:j + ker_h] * kernel)

    return out

@njit
def gerar_histograma(img, n_tons):
    h = np.zeros(n_tons)

    for i, j in np.ndindex(img.shape):
        h[img[i, j]] += 1

    return h

@njit
def eq_histograma_img(img, n_tons):
    out = img.copy()
    h = gerar_histograma(img, n_tons)

    width, height = img.shape
    freq_acc = 0
    lut = np.empty(n_tons)
    escala = (n_tons - 1) / (width * height)

    for i in range(n_tons):
        freq_acc += h[i]
        lut[i] = max(0,  (freq_acc * escala) - 1)

    h = np.zeros(n_tons)
    for i, j in np.ndindex(img.shape):
        out[i, j] = lut[out[i, j]]
        h[out[i, j]] += 1

    return out

# Igualzinho na biblioteca original em C++
# Mas essa aqui eu não arredondo, pra ter mais precisão
# (na outra precisava arredondar pois precisava mostrar)
# (fiz um teste e o HSL voltou perfeito, com 0.0 diferença entre as imagens)
@njit
def rgb_para_hsl(r, g, b):
    rr = r / 255.0
    gg = g / 255.0
    bb = b / 255.0
    cmax = max([ rr, gg, bb ])
    cmin = min([ rr, gg, bb ])
    ll = (cmax + cmin) / 2.0
    if (cmax == cmin):
        h = s = 0
    # Calcula H e S
    else:
        delta = cmax - cmin;
        # S está na escala de 0...1, converter p/ 240
        s = (delta / (1.0 - np.abs((2 * ll) - 1.0))) * 240
        if (cmax == rr):
            hh = ((gg - bb) / delta) + (6.0 if gg < bb else 0.0) # (gg < bb ? 6.0 : 0.0)
        elif (cmax == gg):
            hh = ((bb - rr) / delta) + 2.0
        elif (cmax == bb):
            hh = ((rr - gg) / delta) + 4.0

        if (hh < 0.0):
            hh += 360.0
        hh *= 60.0
        # 0 <= h < 360 => 0 <= h < 240
        hh = (hh * 2.0) / 3.0
        h = hh
    # Calcula L
    l = ll * 240.0

    return h, s, l

@njit
def hsl_f(n, h, s, l):
    k = np.fmod((n + (h / 30.0)), 12.0)
    return np.round((l - (s * min(l, 1.0 - l)) * max(-1.0, min([ k - 3.0, 9.0 - k, 1.0 ]))) * 255.0)

@njit
def hsl_para_rgb(h, s, l):
    ll = l / 240.0
    # Imagem sem saturação (cinza)
    if (s == 0):
        r = g = b = np.round(ll * 255.0)
        return r, g, b

    hh = (h / 2.0) * 3.0
    ss = s / 240.0

    r = hsl_f(0, hh, ss, ll)
    g = hsl_f(8, hh, ss, ll)
    b = hsl_f(4, hh, ss, ll)

    return r, g, b

@njit
def limiarizacao(img, limiar):
    out = img.copy()
    for i, j in np.ndindex(img.shape):
        if (img[i, j] < limiar):
            out[i, j] = 0
    return out

# Binarização: agora com o poder do numpy!
# Faz uma imagem preta, e só pinta de branco os
# pontos que forem >= ao limiar de binarização.
@njit
def binarizacao(img, limiar):
    out = np.zeros(img.shape)
    for i, j in np.ndindex(img.shape):
        if (img[i, j] >= limiar):
            out[i, j] = 255
    return out
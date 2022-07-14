'''
    Slithice - Biblioteca para processamento de imagens em Python

    Um port de algumas funções da versão original da biblioteca,
    escrita em C++ para Qt. Esta versão é baseada em arrays da
    biblioteca numpy, e utiliza o numba para acelerar os cáclulos.
    Os comentários agora, assim como os nomes de funções, estão em
    Português.

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
from numba import jit

@jit
def normalizar(img, v_max, v_min):
    if (v_max == v_min):
        return

    out = np.empty(img.shape)
    for i, j in np.ndindex(img.shape):
        out[i, j] = np.round(((img[i, j] - v_min)*( 255 / (v_max-v_min))))
    
    return out
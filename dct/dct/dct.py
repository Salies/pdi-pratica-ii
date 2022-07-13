import numpy as np
from numba import jit

@jit
def alpha(u, N):
    if(u == 0):
        return np.sqrt(1.0 / N)
    return np.sqrt(2.0 / N)

@jit
def dct(img):
    N = img.shape[0]
    C = np.empty((N, N))
    maxval = -np.inf
    minval = np.inf
    for u in range(N):
        for v in range(N):
            sigma = 0.0
            for x in range(N):
                for y in range(N):
                    sigma += img[x][y] * np.cos((((2 * x) + 1) * u * np.pi) / (2 * N)) * np.cos((((2 * y) + 1) * v * np.pi) / (2 * N))
            C[u][v] = alpha(u, N) * alpha(v, N) * sigma
            if(C[u][v] > maxval):
                maxval = C[u][v]
            if(C[u][v] < minval):
                minval = C[u][v]
    return C, maxval, minval

@jit
def idct(C):
    N = C.shape[0]
    f = np.empty((N, N))
    for x in range(N):
        for y in range(N):
            sigma = 0.0
            for u in range(N):
                for v in range(N):
                    sigma += alpha(u, N) * alpha(v, N) * C[u][v] * np.cos((((2 * x) + 1) * u * np.pi) / (2 * N)) * np.cos((((2 * y) + 1) * v * np.pi) / (2 * N))
            f[x][y] = np.round(sigma)
    return f
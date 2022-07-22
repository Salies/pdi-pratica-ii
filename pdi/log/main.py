from PIL import Image
import numpy as np
from pdi.slithice import conv

im = Image.open("imagens/Fig0638(a)(lenna_RGB).tif").convert("L")

laplace = [
    [0, -1, 0],
    [-1, 4, -1],
    [0, -1, 0]
]

laplace = np.array(laplace)

teste = conv(np.array(im), laplace)
print(teste.shape)

testen = np.divide(teste, 4)

Image.fromarray(testen).show()

from PIL import Image
import numpy as np
import random

im = Image.open("FigP0438(a).tif")
img = np.array(im)
f = img.flatten()
pos = random.sample(range(0, f.size), int(f.size * 0.05)) # 5% de ruído
for p in pos:
    f[p] = 0
img = Image.fromarray(f.reshape(img.shape)).convert("L")
img.save("FigP0438(a)-pepper.tif")
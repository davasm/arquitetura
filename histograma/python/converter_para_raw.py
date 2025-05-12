from PIL import Image
import numpy as np


img = Image.open('imagem.jpg').convert('L')  # 'L' = grayscale


img = img.resize((176, 144))

with open('img_raw.y', 'wb') as f:
    f.write(img.tobytes())
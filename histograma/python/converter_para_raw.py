from PIL import Image
import numpy as np

# Abra a imagem
img = Image.open('imagem.jpg').convert('L')  # 'L' = grayscale

# Redimensiona para 176x144
img = img.resize((176, 144))

# Salva como RAW (apenas os bytes dos pixels)
with open('img_raw.y', 'wb') as f:
    f.write(img.tobytes())
from PIL import Image
import numpy as np

with open('Imagem_PB_equalizada_assembly.raw', 'rb') as f:
    data = f.read()

altura = 120
largura = 176

if len(data) != altura * largura:
    raise ValueError(f"Tamanho do arquivo ({len(data)}) não bate com {altura}x{largura} ({altura*largura})")

img_array = np.frombuffer(data, dtype=np.uint8).reshape((altura, largura))
img = Image.fromarray(img_array, mode='L')
img.save('Imagem_PB_equalizada_assembly.jpg')
print("Imagem salva como Imagem_PB_equalizada_assembly.jpg")
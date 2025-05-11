from PIL import Image
import numpy as np

with open('Equalizada.raw', 'rb') as f:
    data = f.read()

altura = 144
largura = 176

data = data[:altura * largura]

if len(data) != altura * largura:
    raise ValueError(f"Tamanho do arquivo ({len(data)}) não bate com {altura}x{largura} ({altura*largura})")

img_array = np.frombuffer(data, dtype=np.uint8).reshape((altura, largura))
img = Image.fromarray(img_array, mode='L')
img.save('Imagem_PB_equalizada_assembly.jpg')
print("Imagem salva como Imagem_PB_equalizada_assembly.jpg")
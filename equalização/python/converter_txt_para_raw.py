import re
import random

largura = 176
altura = 120
total_pixels = largura * altura

pixels = []
with open('ocorrencias_altonivel_equalizado.txt', encoding='utf-8') as f:
    for linha in f:
        m = re.match(r'Pixel (\d+) - ocorrencia (\d+)', linha)
        if m:
            valor = int(m.group(1))
            ocorrencias = int(m.group(2))
            pixels.extend([valor] * ocorrencias)

if len(pixels) != total_pixels:
    raise ValueError(f"Número de pixels ({len(pixels)}) diferente do esperado ({total_pixels})")

random.shuffle(pixels)  # opcional

with open('imagem_reconstruida_alto_nivel.raw', 'wb') as f:
    f.write(bytearray(pixels))

print("imagem_reconstruida.raw gerada com sucesso!")
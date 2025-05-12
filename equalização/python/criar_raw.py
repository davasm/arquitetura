# Converte um arquivo de histograma (formato "Pixel X - Ocorrencia Y") em uma imagem .raw

import re
import random


largura = 176
altura = 144
total_pixels = largura * altura


histograma = [0] * 256
with open('out_PB_riscv.txt', encoding='utf-8') as f:
    for linha in f:
        m = re.match(r'Pixel (\d+) - Ocorrencia (\d+)', linha)
        if m:
            valor = int(m.group(1))
            ocorrencias = int(m.group(2))
            histograma[valor] = ocorrencias


pixels = []
for valor, ocorrencias in enumerate(histograma):
    pixels.extend([valor] * ocorrencias)


random.shuffle(pixels)


if len(pixels) != total_pixels:
    raise ValueError(f"Número de pixels ({len(pixels)}) diferente do esperado ({total_pixels})")

with open('imagem_reconstruida.raw', 'wb') as f:
    f.write(bytearray(pixels))

print("imagem_reconstruida.raw gerada com sucesso!")
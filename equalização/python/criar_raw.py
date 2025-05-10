# Converte um arquivo de histograma (formato "Pixel X - Ocorrencia Y") em uma imagem .raw

import re
import random

# Parâmetros da imagem (ajuste conforme necessário)
largura = 176
altura = 144
total_pixels = largura * altura

# Lê o histograma do arquivo
histograma = [0] * 256
with open('out_PB_riscv.txt', encoding='utf-8') as f:
    for linha in f:
        m = re.match(r'Pixel (\d+) - Ocorrencia (\d+)', linha)
        if m:
            valor = int(m.group(1))
            ocorrencias = int(m.group(2))
            histograma[valor] = ocorrencias

# Gera a lista de pixels a partir do histograma
pixels = []
for valor, ocorrencias in enumerate(histograma):
    pixels.extend([valor] * ocorrencias)

# Embaralha os pixels para simular uma distribuição realista (opcional)
random.shuffle(pixels)

# Garante que o número de pixels está correto
if len(pixels) != total_pixels:
    raise ValueError(f"Número de pixels ({len(pixels)}) diferente do esperado ({total_pixels})")

# Salva como arquivo .raw (binário puro, 8 bits por pixel)
with open('imagem_reconstruida.raw', 'wb') as f:
    f.write(bytearray(pixels))

print("imagem_reconstruida.raw gerada com sucesso!")
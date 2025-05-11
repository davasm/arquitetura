from collections import Counter
from PIL import Image

# Abre a imagem JPG e converte para tons de cinza
img = Image.open('Imagem_PB.jpg').convert('L')
pixels = list(img.getdata())

# Conta as ocorrências de cada valor de pixel (0 a 255)
contagem = Counter(pixels)

# Salva o histograma em um arquivo txt
with open('histograma_imagem_alto_nivel.txt', 'w', encoding='utf-8') as f:
    for valor in range(256):
        f.write(f"Pixel {valor} - ocorrencia {contagem.get(valor, 0)}\n")

print("Histograma salvo em histograma_imagem.txt")
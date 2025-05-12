from collections import Counter
from PIL import Image


img = Image.open('Imagem_PB.jpg').convert('L')
pixels = list(img.getdata())


contagem = Counter(pixels)


with open('histograma_imagem_alto_nivel.txt', 'w', encoding='utf-8') as f:
    for valor in range(256):
        f.write(f"Pixel {valor} - ocorrencia {contagem.get(valor, 0)}\n")

print("Histograma salvo em histograma_imagem.txt")
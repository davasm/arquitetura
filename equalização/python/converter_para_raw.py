from PIL import Image
img = Image.open('Imagem_PB.jpg').convert('L')
with open('Imagem_PB.raw', 'wb') as f:
    f.write(img.tobytes())
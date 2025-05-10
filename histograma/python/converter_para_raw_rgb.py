from PIL import Image

# Altere o nome da imagem se necessário
img = Image.open('imagem.jpg').convert('RGB').resize((176, 144))

# Salva o RAW RGB (cada pixel = 3 bytes: R, G, B)
with open('img_rgb.raw', 'wb') as f:
    f.write(img.tobytes())
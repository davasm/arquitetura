from PIL import Image


img = Image.open('imagem.jpg').convert('RGB').resize((176, 144))


with open('img_rgb.raw', 'wb') as f:
    f.write(img.tobytes())
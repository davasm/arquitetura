from PIL import Image

# Abra a imagem original (ajuste o nome se necessário)
img = Image.open('imagem.jpg')

# Converta para tons de cinza
img_pb = img.convert('L')

# Salve a nova imagem em tons de cinza
img_pb.save('Imagem_PB.jpg')
print("Imagem convertida para tons de cinza e salva como Imagem_PB.jpg")
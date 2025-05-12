from PIL import Image


img = Image.open('imagem.jpg')

img_pb = img.convert('L')


img_pb.save('Imagem_PB.jpg')
print("Imagem convertida para tons de cinza e salva como Imagem_PB.jpg")
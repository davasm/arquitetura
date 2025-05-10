from PIL import Image
import numpy as np

img = Image.open('Imagem_PB.jpg').convert('L')
pixels = np.array(img)
hist, _ = np.histogram(pixels.flatten(), bins=256, range=[0,256])
cdf = hist.cumsum()
cdf_min = cdf[cdf > 0][0]
cdf_normalized = ((cdf - cdf_min) * 255) / (cdf[-1] - cdf_min)
cdf_normalized = cdf_normalized.astype('uint8')
img_eq = cdf_normalized[pixels]
Image.fromarray(img_eq).save('Imagem_PB_equalizada_altonivel.jpg')
print("Imagem equalizada salva como Imagem_PB_equalizada_altonivel.jpg")

# Gerar arquivo de histograma
with open('histograma_altonivel.txt', 'w') as f:
    for i, count in enumerate(hist):
        f.write(f"Pixel {i} - ocorencia {count}\n")
print("Histograma salvo em histograma_altonivel.txt")
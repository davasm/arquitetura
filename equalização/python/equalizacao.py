# equalizador_altonivel.py
from PIL import Image
import numpy as np

def equalizar_histograma(array):
    # Calcular histograma e CDF
    hist, bins = np.histogram(array.flatten(), 256, [0, 256])
    cdf = hist.cumsum()
    
    # Normalizar CDF
    cdf_normalized = (cdf - cdf.min()) * 255 / (cdf.max() - cdf.min())
    
    # Aplicar mapeamento
    equalized = np.interp(array.flatten(), bins[:-1], cdf_normalized)
    return equalized.reshape(array.shape).astype('uint8')

def main():
    # Carregar imagem em tons de cinza
    gray_img = Image.open("Imagem_PB.jpg")
    gray_array = np.array(gray_img)
    
    # Equalizar
    equalized = equalizar_histograma(gray_array)
    
    # Salvar resultados
    Image.fromarray(equalized).save("Imagem_PB_equalizada_altonivel.jpg")
    salvar_ocorrencias(equalized, "histograma_altonivel_equalizado.txt")

def salvar_ocorrencias(array, arquivo):
    hist, _ = np.histogram(array, bins=256, range=(0, 256))
    with open(arquivo, "w") as f:
        for i in range(256):
            f.write(f"Pixel {i} - ocorrencia {hist[i]}\n")

if __name__ == "__main__":
    main()
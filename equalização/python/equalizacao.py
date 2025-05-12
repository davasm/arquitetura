import cv2
import numpy as np


img_pb = cv2.imread("Imagem_PB.jpg", cv2.IMREAD_GRAYSCALE)
if img_pb is None:
    raise FileNotFoundError("Não encontrou Imagem_PB.jpg")


img_eq = cv2.equalizeHist(img_pb)


cv2.imwrite("Imagem_PB_equalizada_altonivel.jpg", img_eq)


hist_eq, _ = np.histogram(img_eq, bins=256, range=(0, 256))

with open("histograma_altonivel_equalizada.txt", "w") as f:
    for valor, contagem in enumerate(hist_eq):
        f.write(f"Pixel {valor} - Ocorrencia {contagem}\n")

print("Processamento concluído:")
print("- Imagem equalizada em Imagem_PB_equalizada_altonivel.jpg")
print("- Histograma salvo em histograma_altonivel_equalizada.txt")

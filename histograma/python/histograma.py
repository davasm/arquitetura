

import os
import sys
from PIL import Image
import numpy as np
import pandas as pd
import plotly.express as px

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(BASE_DIR, 'imagem.jpg')
RESULT_DIR = os.path.join(BASE_DIR, 'result_python')
os.makedirs(RESULT_DIR, exist_ok=True)


def calcula_histograma_rgb(img):
    r_hist = [0]*256
    g_hist = [0]*256
    b_hist = [0]*256
    for r, g, b in img.getdata():
        r_hist[r] += 1
        g_hist[g] += 1
        b_hist[b] += 1
    return r_hist, g_hist, b_hist


def equalizar_rgb(img):
    canais_eq = []
    arr = np.array(img)
    for ch in range(3):
        canal = arr[..., ch].flatten()
        counts = np.bincount(canal, minlength=256)
        total = canal.size
        cdf = np.cumsum(counts)
        lut = np.floor((cdf - cdf.min())/(total - cdf.min()) * 255).astype(np.uint8)
        canal_eq = lut[arr[..., ch]]
        canais_eq.append(canal_eq.reshape(arr.shape[0], arr.shape[1]))
    merged = np.stack(canais_eq, axis=2)
    return Image.fromarray(merged)


def salva_histogramas(hist_list, prefix):
    canais = ['red', 'green', 'blue']
    for hist, canal in zip(hist_list, canais):
        filename = os.path.join(RESULT_DIR, f"{prefix}_{canal}.txt")
        with open(filename, 'w') as f:
            for i, cnt in enumerate(hist):
                f.write(f"Pixel {i} - Ocorrencia {cnt}\n")


def plota_histograma_interativo(img):
    pixels = list(img.getdata())
    dados = []
    for r, g, b in pixels:
        dados.append((r, 'Vermelho'))
        dados.append((g, 'Verde'))
        dados.append((b, 'Azul'))
    df = pd.DataFrame(dados, columns=['Intensidade', 'Canal'])
    fig = px.histogram(
        df,
        x='Intensidade',
        color='Canal',
        nbins=256,
        title='Histograma RGB por Canal',
        color_discrete_map={
            'Vermelho': 'rgba(255, 102, 102, 0.6)',
            'Verde':    'rgba(144, 238, 144, 0.6)',
            'Azul':     'rgba(173, 216, 230, 0.6)',
        }
    )
    fig.show()


def main():
    if not os.path.isfile(IMAGE_PATH):
        print(f"Arquivo não encontrado: {IMAGE_PATH}", file=sys.stderr)
        sys.exit(1)


    img = Image.open(IMAGE_PATH).convert('RGB')

    r_hist, g_hist, b_hist = calcula_histograma_rgb(img)
    salva_histogramas([r_hist, g_hist, b_hist], 'histograma_original')
    print(f"Histogramas originais salvos em {RESULT_DIR}")

    plota_histograma_interativo(img)

    img_eq = equalizar_rgb(img)
    out_img_path = os.path.join(RESULT_DIR, 'imagem_equalizada_altonivel.jpg')
    img_eq.save(out_img_path)
    print(f"Imagem equalizada salva em {out_img_path}")

    rh_eq, gh_eq, bh_eq = calcula_histograma_rgb(img_eq)
    salva_histogramas([rh_eq, gh_eq, bh_eq], 'histograma_equalizado')
    print(f"Histogramas equalizados salvos em {RESULT_DIR}")

if __name__ == '__main__':
    main()

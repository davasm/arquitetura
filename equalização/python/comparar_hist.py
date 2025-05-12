import matplotlib.pyplot as plt
import os

def read_histogram(file_path):
    hist = []
    with open(file_path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            hist.append(int(parts[-1]))
    return hist

files = {
    "Python Original":          "histograma_imagem_alto_nivel.txt",
    "Assembly Original":        "histograma_assembly.txt",
    "Python Equalizado":        "histograma_altonivel_equalizado.txt",
    "Assembly Equalizado":      "histograma_equalizada_assembly.txt",
}


for label, fname in files.items():
    path = fname  
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Não encontrei '{fname}' no diretório atual")
    files[label] = path


hists = {label: read_histogram(path) for label, path in files.items()}

plt.figure()
plt.plot(hists["Python Original"], label="Python Original")
plt.plot(hists["Assembly Original"], label="Assembly Original")
plt.title("Comparação do Histograma Original")
plt.xlabel("Valor de Pixel")
plt.ylabel("Ocorrência")
plt.legend()
plt.tight_layout()
plt.show()

plt.figure()
plt.plot(hists["Python Equalizado"], label="Python Equalizado")
plt.plot(hists["Assembly Equalizado"], label="Assembly Equalizado")
plt.title("Comparação do Histograma Equalizado")
plt.xlabel("Valor de Pixel")
plt.ylabel("Ocorrência")
plt.legend()
plt.tight_layout()
plt.show()

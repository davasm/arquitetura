# Exemplo de comparação de histogramas, ignorando linhas inválidas

with open('histograma_altonivel_equalizado.txt', encoding='utf-8') as f1, open('histograma_equalizada_assembly.txt', encoding='utf-8') as f2:
    histo1 = []
    histo2 = []
    for line in f1:
        partes = line.strip().split()
        if partes and partes[-1].isdigit():
            histo1.append(int(partes[-1]))
    for line in f2:
        partes = line.strip().split()
        if partes and partes[-1].isdigit():
            histo2.append(int(partes[-1]))

# Exemplo de comparação: diferença absoluta total
if len(histo1) == len(histo2):
    diff = sum(abs(a - b) for a, b in zip(histo1, histo2))
    print(f'Diferença absoluta total: {diff}')
else:
    print('Os histogramas têm tamanhos diferentes!')
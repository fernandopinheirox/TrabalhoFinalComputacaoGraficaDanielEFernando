import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import random

# Variáveis de recorte e memória da última polilinha/polígono desenhado
x_min, y_min, x_max, y_max = -10, -10, 10, 10
ultimos_pontos = []  # Variável global para armazenar as últimas coordenadas desenhadas
pixels_preenchidos = set()  # Conjunto para armazenar os pixels preenchidos

# Função para desenhar a grade e a polilinha/polígono
def desenhar_grade(pontos, aplicar_recorte=False):
    global ultimos_pontos
    ultimos_pontos = pontos if not aplicar_recorte else recortar_polilinha(pontos)  # Armazena os pontos desenhados
    plt.clf()
    plt.xlim(-22, 22)
    plt.ylim(-22, 22)

    # Desenhar a grade
    for x in range(-22, 23):
        plt.axvline(x, color='gray', linestyle='--', linewidth=0.5)
    for y in range(-22, 23):
        plt.axhline(y, color='gray', linestyle='--', linewidth=0.5)

    # Desenhar a polilinha ou polígono
    desenhar_polilinha(ultimos_pontos)

    plt.grid(True)
    plt.axhline(0, color='black', linewidth=1)  # Eixo X
    plt.axvline(0, color='black', linewidth=1)  # Eixo Y
    plt.show()

# Função para desenhar a polilinha usando Bresenham
def desenhar_polilinha(pontos):
    for i in range(len(pontos) - 1):
        x1, y1 = pontos[i]
        x2, y2 = pontos[i + 1]
        bresenham(x1, y1, x2, y2)

# Algoritmo de Bresenham para desenhar quadrados
def bresenham(x1, y1, x2, y2):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    while True:
        plt.gca().add_patch(plt.Rectangle((x1, y1), 1, 1, color='blue', alpha=0.5))
        if x1 == x2 and y1 == y2:
            break
        err2 = err * 2
        if err2 > -dy:
            err -= dy
            x1 += sx
        if err2 < dx:
            err += dx
            y1 += sy

# Função para obter dados do usuário
def obter_dados(aplicar_recorte=False):
    global x_min, y_min, x_max, y_max
    try:
        # Obtém os pontos de entrada como uma lista de pares (x, y)
        pontos_str = entry_pontos.get().split(';')
        pontos = []
        
        # Pega os valores de recorte
        x_min = int(entry_xmin.get())
        y_min = int(entry_ymin.get())
        x_max = int(entry_xmax.get())
        y_max = int(entry_ymax.get())
        
        for ponto_str in pontos_str:
            x, y = map(int, ponto_str.split(','))
            if not (-22 <= x <= 22 and -22 <= y <= 22):
                messagebox.showerror("Erro", "Os pontos devem estar entre -22 e 22.")
                return
            pontos.append((x, y))
        
        desenhar_grade(pontos, aplicar_recorte=aplicar_recorte)
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira valores válidos no formato 'x1,y1;x2,y2;...'. Ex: '0,0;5,5;-2,-3'")

# Algoritmo de recorte de polilinha (usando Cohen-Sutherland)
INSIDE = 0
LEFT = 1
RIGHT = 2
BOTTOM = 4
TOP = 8

def compute_outcode(x, y):
    code = INSIDE
    if x < x_min:
        code |= LEFT
    elif x > x_max:
        code |= RIGHT
    if y < y_min:
        code |= BOTTOM
    elif y > y_max:
        code |= TOP
    return code

def cohen_sutherland_clip(x1, y1, x2, y2):
    outcode1 = compute_outcode(x1, y1)
    outcode2 = compute_outcode(x2, y2)
    accept = False
    pontos_visiveis = []  # Lista para guardar os pontos visíveis

    while True:
        if outcode1 == 0 and outcode2 == 0:
            accept = True
            pontos_visiveis.extend([(x1, y1), (x2, y2)])
            break
        elif (outcode1 & outcode2) != 0:
            break
        else:
            x, y = 0, 0
            outcode_out = outcode1 if outcode1 != 0 else outcode2

            if outcode_out & TOP:
                x = x1 + (x2 - x1) * (y_max - y1) / (y2 - y1)
                y = y_max
            elif outcode_out & BOTTOM:
                x = x1 + (x2 - x1) * (y_min - y1) / (y2 - y1)
                y = y_min
            elif outcode_out & RIGHT:
                y = y1 + (y2 - y1) * (x_max - x1) / (x2 - x1)
                x = x_max
            elif outcode_out & LEFT:
                y = y1 + (y2 - y1) * (x_min - x1) / (x2 - x1)
                x = x_min

            if outcode_out == outcode1:
                x1, y1 = x, y
                outcode1 = compute_outcode(x1, y1)
            else:
                x2, y2 = x, y
                outcode2 = compute_outcode(x2, y2)

            pontos_visiveis.append((int(x), int(y)))

    return pontos_visiveis if accept else None

def recortar_polilinha(pontos):
    pontos_recortados = []
    for i in range(len(pontos) - 1):
        ponto_inicial = pontos[i]
        ponto_final = pontos[i + 1]
        linha_recortada = cohen_sutherland_clip(*ponto_inicial, *ponto_final)
        if linha_recortada:
            pontos_recortados.extend(linha_recortada)
    return pontos_recortados

# Função para verificar se um ponto está dentro do polígono
def ponto_em_poligono(ponto, poligono):
    x, y = ponto
    n = len(poligono)
    dentro = False

    for i in range(n):
        x1, y1 = poligono[i]
        x2, y2 = poligono[(i + 1) % n]

        if (y1 > y) != (y2 > y) and (x < (x2 - x1) * (y - y1) / (y2 - y1) + x1):
            dentro = not dentro

    return dentro

# Função para preencher a área (recursivo)
def preencher_area():
    if not ultimos_pontos:
        messagebox.showerror("Erro", "Por favor, insira uma polilinha primeiro.")
        return

    # Escolher um ponto aleatório dentro do polígono
    while True:
        x_rand = random.randint(-22, 22)
        y_rand = random.randint(-22, 22)
        if ponto_em_poligono((x_rand, y_rand), ultimos_pontos):
            flood_fill(x_rand, y_rand)
            break

def flood_fill(x, y):
    if not (-22 <= x <= 22 and -22 <= y <= 22):
        return
    if (x, y) in pixels_preenchidos:
        return

    # Verifica se o pixel está dentro da polilinha/polígono
    if not ponto_em_poligono((x, y), ultimos_pontos):
        return

    pixels_preenchidos.add((x, y))
    plt.gca().add_patch(plt.Rectangle((x, y), 1, 1, color='green', alpha=0.5))

    # Preenchimento recursivo
    flood_fill(x + 1, y)
    flood_fill(x - 1, y)
    flood_fill(x, y + 1)
    flood_fill(x, y - 1)

# Função para preencher por varredura (Scanline Fill)
def preencher_area_varredura():
    if not ultimos_pontos:
        messagebox.showerror("Erro", "Por favor, insira uma polilinha primeiro.")
        return

    # Obter a faixa de y dos pontos do polígono
    ys = [y for _, y in ultimos_pontos]
    y_min = int(min(ys))
    y_max = int(max(ys))

    for y in range(y_min, y_max + 1):
        interseccoes = []
        for i in range(len(ultimos_pontos)):
            x1, y1 = ultimos_pontos[i]
            x2, y2 = ultimos_pontos[(i + 1) % len(ultimos_pontos)]

            # Verifica se a linha horizontal intersecta a aresta do polígono
            if (y1 <= y < y2) or (y2 <= y < y1):
                x = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
                interseccoes.append(x)

        # Ordena as interseções
        interseccoes.sort()

        # Preenche entre os pares de interseções
        for i in range(0, len(interseccoes), 2):
            if i + 1 < len(interseccoes):
                x1 = int(interseccoes[i])
                x2 = int(interseccoes[i + 1])
                for x in range(x1, x2):
                    plt.gca().add_patch(plt.Rectangle((x, y), 1, 1, color='green', alpha=0.5))

def adicionar_ponto_aleatorio():
    if not ultimos_pontos:
        messagebox.showerror("Erro", "Por favor, insira uma polilinha primeiro.")
        return

    while True:
        x_rand = random.randint(-22, 22)
        y_rand = random.randint(-22, 22)
        if ponto_em_poligono((x_rand, y_rand), ultimos_pontos):
            plt.gca().add_patch(plt.Rectangle((x_rand, y_rand), 1, 1, color='red', alpha=0.5))
            plt.draw()
            break

# Criar a interface
root = tk.Tk()
root.title("Desenho de Polilinha com Recorte e Preenchimento")

# Label e entrada para os pontos
tk.Label(root, text="Insira os pontos no formato (x,y) separados por ';':").pack()

frame_pontos = tk.Frame(root)
frame_pontos.pack(pady=5)

entry_pontos = tk.Entry(frame_pontos, width=50)
entry_pontos.pack(side=tk.LEFT, padx=5)

# Labels e entradas para os limites de recorte
tk.Label(root, text="Limites de Recorte (x_min, y_min, x_max, y_max):").pack(pady=(10, 0))
frame_recorte = tk.Frame(root)
frame_recorte.pack(pady=5)

entry_xmin = tk.Entry(frame_recorte, width=5)
entry_xmin.insert(0, "-10")
entry_xmin.pack(side=tk.LEFT, padx=5)

entry_ymin = tk.Entry(frame_recorte, width=5)
entry_ymin.insert(0, "-10")
entry_ymin.pack(side=tk.LEFT, padx=5)

entry_xmax = tk.Entry(frame_recorte, width=5)
entry_xmax.insert(0, "10")
entry_xmax.pack(side=tk.LEFT, padx=5)

entry_ymax = tk.Entry(frame_recorte, width=5)
entry_ymax.insert(0, "10")
entry_ymax.pack(side=tk.LEFT, padx=5)

# Botões para desenhar com e sem recorte
botao_sem_recorte = tk.Button(root, text="Desenhar Polilinha", command=lambda: obter_dados(aplicar_recorte=False))
botao_sem_recorte.pack(pady=10)

botao_com_recorte = tk.Button(root, text="Desenhar com Recorte", command=lambda: obter_dados(aplicar_recorte=True))
botao_com_recorte.pack(pady=10)

botao_preencher = tk.Button(root, text="Preencher Recursivo", command=preencher_area)
botao_preencher.pack(pady=10)

botao_varredura = tk.Button(root, text="Preencher por Varredura", command=preencher_area_varredura)
botao_varredura.pack(pady=10)

# Botão para adicionar um ponto aleatório
botao_aleatorio = tk.Button(root, text="Ponto Aleatório", command=adicionar_ponto_aleatorio)
botao_aleatorio.pack(pady=10)

# Iniciar a interface
root.mainloop()

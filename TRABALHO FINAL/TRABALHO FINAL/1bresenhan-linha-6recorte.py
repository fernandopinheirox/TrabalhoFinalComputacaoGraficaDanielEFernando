import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

# Variáveis de recorte, inicialmente com valores padrão
x_min, y_min, x_max, y_max = -5, -5, 5, 5

# Algoritmo de Cohen-Sutherland para recorte de linhas
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

    while True:
        if outcode1 == 0 and outcode2 == 0:
            accept = True
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

    if accept:
        return (int(x1), int(y1), int(x2), int(y2))
    else:
        return None

# Função para desenhar a grade e preencher os quadrados
def desenhar_grade(x1, y1, x2, y2, aplicar_recorte=False):
    plt.clf()
    plt.xlim(-22, 22)
    plt.ylim(-22, 22)

    # Desenhar a grade
    for x in range(-22, 23):
        plt.axvline(x, color='gray', linestyle='--', linewidth=0.5)
    for y in range(-22, 23):
        plt.axhline(y, color='gray', linestyle='--', linewidth=0.5)

    # Aplica o recorte de linha e desenha somente a parte visível
    if aplicar_recorte:
        pontos_recortados = cohen_sutherland_clip(x1, y1, x2, y2)
        if pontos_recortados:
            bresenham(*pontos_recortados)
    else:
        bresenham(x1, y1, x2, y2)

    plt.grid(True)
    plt.axhline(0, color='black', linewidth=1)
    plt.axvline(0, color='black', linewidth=1)
    plt.show()

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

# Função para obter dados do usuário e desenhar a linha
def obter_dados(aplicar_recorte=False):
    global x_min, y_min, x_max, y_max
    try:
        x1 = int(entry_x1.get())
        y1 = int(entry_y1.get())
        x2 = int(entry_x2.get())
        y2 = int(entry_y2.get())
        
        # Obter limites de recorte definidos pelo usuário
        x_min = int(entry_xmin.get())
        y_min = int(entry_ymin.get())
        x_max = int(entry_xmax.get())
        y_max = int(entry_ymax.get())
        
        # Verifica se os pontos estão dentro da grade
        if not (-22 <= x1 <= 22 and -22 <= y1 <= 22 and -22 <= x2 <= 22 and -22 <= y2 <= 22):
            messagebox.showerror("Erro", "Os pontos devem estar entre -22 e 22.")
            return
        
        desenhar_grade(x1, y1, x2, y2, aplicar_recorte=aplicar_recorte)
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira valores inteiros válidos.")

# Criar a interface
root = tk.Tk()
root.title("Desenho de Grade com Recorte")

# Labels e entradas para os pontos da linha
tk.Label(root, text="Ponto Inicial (x1, y1):").pack()
frame_inicial = tk.Frame(root)
frame_inicial.pack(pady=5)

entry_x1 = tk.Entry(frame_inicial, width=5)
entry_x1.pack(side=tk.LEFT, padx=5)
entry_y1 = tk.Entry(frame_inicial, width=5)
entry_y1.pack(side=tk.LEFT, padx=5)

tk.Label(root, text="Ponto Final (x2, y2):").pack(pady=(10, 0))
frame_final = tk.Frame(root)
frame_final.pack(pady=5)

entry_x2 = tk.Entry(frame_final, width=5)
entry_x2.pack(side=tk.LEFT, padx=5)
entry_y2 = tk.Entry(frame_final, width=5)
entry_y2.pack(side=tk.LEFT, padx=5)

# Labels e entradas para os limites de recorte
tk.Label(root, text="Limites de Recorte (x_min, y_min, x_max, y_max):").pack(pady=(10, 0))
frame_recorte = tk.Frame(root)
frame_recorte.pack(pady=5)

entry_xmin = tk.Entry(frame_recorte, width=5)
entry_xmin.insert(0, "-5")
entry_xmin.pack(side=tk.LEFT, padx=5)

entry_ymin = tk.Entry(frame_recorte, width=5)
entry_ymin.insert(0, "-5")
entry_ymin.pack(side=tk.LEFT, padx=5)

entry_xmax = tk.Entry(frame_recorte, width=5)
entry_xmax.insert(0, "5")
entry_xmax.pack(side=tk.LEFT, padx=5)

entry_ymax = tk.Entry(frame_recorte, width=5)
entry_ymax.insert(0, "5")
entry_ymax.pack(side=tk.LEFT, padx=5)

# Botões para desenhar com e sem recorte
botao_sem_recorte = tk.Button(root, text="Desenhar Reta Bresenham", command=lambda: obter_dados(aplicar_recorte=False))
botao_sem_recorte.pack(pady=10)

botao_com_recorte = tk.Button(root, text="Desenhar com Recorte", command=lambda: obter_dados(aplicar_recorte=True))
botao_com_recorte.pack(pady=10)

# Iniciar a interface
root.mainloop()

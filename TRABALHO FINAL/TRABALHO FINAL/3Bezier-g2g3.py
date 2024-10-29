import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np

# Função para desenhar a grade e preencher os quadrados
def desenhar_grade(x0, y0, x1, y1, xc1, yc1, xc2=None, yc2=None):
    plt.clf()  # Limpa o gráfico anterior
    plt.xlim(-22, 22)
    plt.ylim(-22, 22)

    # Desenhar a grade
    for x in range(-22, 23):
        plt.axvline(x, color='gray', linestyle='--', linewidth=0.5)
    for y in range(-22, 23):
        plt.axhline(y, color='gray', linestyle='--', linewidth=0.5)

    # Preencher a curva de Bézier com base nos dados
    desenhar_bezier(x0, y0, x1, y1, xc1, yc1, xc2, yc2)

    plt.grid(True)
    plt.axhline(0, color='black', linewidth=1)  # Eixo X
    plt.axvline(0, color='black', linewidth=1)  # Eixo Y
    plt.show()

# Função para desenhar uma curva de Bézier usando Bresenham
def desenhar_bezier(x0, y0, x1, y1, xc1, yc1, xc2=None, yc2=None):
    pontos = calcular_bezier(x0, y0, x1, y1, xc1, yc1, xc2, yc2)

    for i in range(len(pontos) - 1):
        bresenham(pontos[i][0], pontos[i][1], pontos[i + 1][0], pontos[i + 1][1])

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

# Função para calcular os pontos de uma curva de Bézier
def calcular_bezier(x0, y0, x1, y1, xc1, yc1, xc2=None, yc2=None):
    pontos = []
    t_values = np.linspace(0, 1, 100)  # Dividindo t em 100 pontos para suavidade

    if xc2 is None and yc2 is None:  # Bézier de grau 2
        for t in t_values:
            x = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * xc1 + t ** 2 * x1
            y = (1 - t) ** 2 * y0 + 2 * (1 - t) * t * yc1 + t ** 2 * y1
            pontos.append((int(round(x)), int(round(y))))  # Arredondar para valores inteiros
    else:  # Bézier de grau 3
        for t in t_values:
            x = (1 - t) ** 3 * x0 + 3 * (1 - t) ** 2 * t * xc1 + 3 * (1 - t) * t ** 2 * xc2 + t ** 3 * x1
            y = (1 - t) ** 3 * y0 + 3 * (1 - t) ** 2 * t * yc1 + 3 * (1 - t) * t ** 2 * yc2 + t ** 3 * y1
            pontos.append((int(round(x)), int(round(y))))  # Arredondar para valores inteiros

    return pontos

# Função para obter dados do usuário
def obter_dados():
    try:
        x0 = int(entry_x0.get())
        y0 = int(entry_y0.get())
        x1 = int(entry_x1.get())
        y1 = int(entry_y1.get())
        xc1 = int(entry_xc1.get())
        yc1 = int(entry_yc1.get())
        
        if var_grau.get() == 1:  # Grau 2
            xc2 = yc2 = None
        else:  # Grau 3
            xc2 = int(entry_xc2.get())
            yc2 = int(entry_yc2.get())

        # Verifica se os pontos estão dentro da grade
        if not (-25 < x0 < 25 and -25 < y0 < 25 and -25 < x1 < 25 and -25 < y1 < 25 and
                -25 < xc1 < 25 and -25 < yc1 < 25 and (xc2 is None or (-25 < xc2 < 25)) and (yc2 is None or (-25 < yc2 < 25))):
            messagebox.showerror("Erro", "Os pontos devem estar entre -25 e 25.")
            return

        desenhar_grade(x0, y0, x1, y1, xc1, yc1, xc2, yc2)
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira valores inteiros válidos.")

# Criar a interface
root = tk.Tk()
root.title("Curva de Bézier com Bresenham")

# Labels e entradas para os pontos
tk.Label(root, text="Ponto Inicial (x0, y0):").pack()

frame_inicial = tk.Frame(root)
frame_inicial.pack(pady=5)

entry_x0 = tk.Entry(frame_inicial, width=5)  # Diminuindo o tamanho do campo
entry_x0.pack(side=tk.LEFT, padx=5)
entry_y0 = tk.Entry(frame_inicial, width=5)  # Diminuindo o tamanho do campo
entry_y0.pack(side=tk.LEFT, padx=5)

tk.Label(root, text="Ponto de Controle 1 (xc1, yc1):").pack(pady=(10, 0))

frame_controle1 = tk.Frame(root)
frame_controle1.pack(pady=5)

entry_xc1 = tk.Entry(frame_controle1, width=5)  # Diminuindo o tamanho do campo
entry_xc1.pack(side=tk.LEFT, padx=5)
entry_yc1 = tk.Entry(frame_controle1, width=5)  # Diminuindo o tamanho do campo
entry_yc1.pack(side=tk.LEFT, padx=5)

# Adicionar um segundo ponto de controle para Bézier de grau 3
tk.Label(root, text="Ponto de Controle 2 (xc2, yc2):").pack(pady=(10, 0))

frame_controle2 = tk.Frame(root)
frame_controle2.pack(pady=5)

entry_xc2 = tk.Entry(frame_controle2, width=5)  # Diminuindo o tamanho do campo
entry_xc2.pack(side=tk.LEFT, padx=5)
entry_yc2 = tk.Entry(frame_controle2, width=5)  # Diminuindo o tamanho do campo
entry_yc2.pack(side=tk.LEFT, padx=5)

tk.Label(root, text="Ponto Final (x1, y1):").pack(pady=(10, 0))

frame_final = tk.Frame(root)
frame_final.pack(pady=5)

entry_x1 = tk.Entry(frame_final, width=5)  # Diminuindo o tamanho do campo
entry_x1.pack(side=tk.LEFT, padx=5)
entry_y1 = tk.Entry(frame_final, width=5)  # Diminuindo o tamanho do campo
entry_y1.pack(side=tk.LEFT, padx=5)

# Opções de grau da curva
var_grau = tk.IntVar(value=1)  # 1 para grau 2, 2 para grau 3

frame_grau = tk.Frame(root)
frame_grau.pack(pady=10)

tk.Radiobutton(frame_grau, text="Grau 2", variable=var_grau, value=1).pack(side=tk.LEFT)
tk.Radiobutton(frame_grau, text="Grau 3", variable=var_grau, value=2).pack(side=tk.LEFT)

# Botão para desenhar
botao = tk.Button(root, text="Desenhar Curva Bézier", command=obter_dados)
botao.pack(pady=20)

# Inicializa a visibilidade do segundo ponto de controle
def atualizar_visibilidade():
    if var_grau.get() == 1:
        entry_xc2.pack_forget()
        entry_yc2.pack_forget()
    else:
        entry_xc2.pack(side=tk.LEFT, padx=5)
        entry_yc2.pack(side=tk.LEFT, padx=5)

var_grau.trace("w", lambda *args: atualizar_visibilidade())
atualizar_visibilidade()

# Iniciar a interface
root.mainloop()

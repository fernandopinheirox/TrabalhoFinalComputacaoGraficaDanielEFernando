import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np

# Função para desenhar a grade
def desenhar_grade(xc, yc, raio, a=None, b=None):
    plt.clf()  # Limpa o gráfico anterior
    plt.xlim(-22, 22)
    plt.ylim(-22, 22)

    # Desenhar a grade
    for x in range(-22, 23):
        plt.axvline(x, color='gray', linestyle='--', linewidth=0.5)
    for y in range(-22, 23):
        plt.axhline(y, color='gray', linestyle='--', linewidth=0.5)

    # Desenhar círculo ou elipse
    if a is None or b is None:  # Desenhar círculo
        bresenham_circulo(xc, yc, raio)
    else:  # Desenhar elipse
        bresenham_elipse(xc, yc, a, b)

    plt.grid(True)
    plt.axhline(0, color='black', linewidth=1)  # Eixo X
    plt.axvline(0, color='black', linewidth=1)  # Eixo Y
    plt.show()

# Algoritmo de Bresenham para desenhar círculo
def bresenham_circulo(xc, yc, raio):
    x = 0
    y = raio
    d = 3 - 2 * raio
    plotar_circulo(xc, yc, x, y)

    while y >= x:
        x += 1
        if d > 0:
            y -= 1
            d = d + 4 * (x - y) + 10
        else:
            d = d + 4 * x + 6
        plotar_circulo(xc, yc, x, y)

# Função para plotar os pontos do círculo em todas as 8 regiões
def plotar_circulo(xc, yc, x, y):
    plt.gca().add_patch(plt.Rectangle((xc + x, yc + y), 1, 1, color='blue', alpha=0.5))
    plt.gca().add_patch(plt.Rectangle((xc - x, yc + y), 1, 1, color='blue', alpha=0.5))
    plt.gca().add_patch(plt.Rectangle((xc + x, yc - y), 1, 1, color='blue', alpha=0.5))
    plt.gca().add_patch(plt.Rectangle((xc - x, yc - y), 1, 1, color='blue', alpha=0.5))
    plt.gca().add_patch(plt.Rectangle((xc + y, yc + x), 1, 1, color='blue', alpha=0.5))
    plt.gca().add_patch(plt.Rectangle((xc - y, yc + x), 1, 1, color='blue', alpha=0.5))
    plt.gca().add_patch(plt.Rectangle((xc + y, yc - x), 1, 1, color='blue', alpha=0.5))
    plt.gca().add_patch(plt.Rectangle((xc - y, yc - x), 1, 1, color='blue', alpha=0.5))

# Algoritmo de Bresenham para desenhar elipse
def bresenham_elipse(xc, yc, a, b):
    x = 0
    y = b
    d1 = b * b - a * a * b + 0.25 * a * a
    plotar_elipse(xc, yc, x, y)

    while b * b * x < a * a * y:
        x += 1
        if d1 < 0:
            d1 += 2 * b * b * x + b * b
        else:
            y -= 1
            d1 += 2 * b * b * x - 2 * a * a * y + b * b
        plotar_elipse(xc, yc, x, y)

    d2 = b * b * (x + 0.5) * (x + 0.5) + a * a * (y - 1) * (y - 1) - a * a * b * b
    while y > 0:
        y -= 1
        if d2 > 0:
            d2 += -2 * a * a * y + a * a
        else:
            x += 1
            d2 += 2 * b * b * x - 2 * a * a * y + a * a
        plotar_elipse(xc, yc, x, y)

# Função para plotar os pontos da elipse em todas as 4 quadrantes
def plotar_elipse(xc, yc, x, y):
    plt.gca().add_patch(plt.Rectangle((xc + x, yc + y), 1, 1, color='red', alpha=0.5))
    plt.gca().add_patch(plt.Rectangle((xc - x, yc + y), 1, 1, color='red', alpha=0.5))
    plt.gca().add_patch(plt.Rectangle((xc + x, yc - y), 1, 1, color='red', alpha=0.5))
    plt.gca().add_patch(plt.Rectangle((xc - x, yc - y), 1, 1, color='red', alpha=0.5))

# Função para obter dados do usuário
def obter_dados_circulo():
    try:
        xc = int(entry_xc.get())
        yc = int(entry_yc.get())
        raio = int(entry_raio.get())
        
        # Verifica se o centro da circunferência está dentro da grade
        if not (-22 <= xc <= 22 and -22 <= yc <= 22):
            messagebox.showerror("Erro", "O centro da circunferência deve estar entre -22 e 22.")
            return
        if raio <= 0 or raio > 22:
            messagebox.showerror("Erro", "O raio deve ser maior que 0 e menor ou igual a 22.")
            return

        desenhar_grade(xc, yc, raio)
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira valores inteiros válidos.")

def obter_dados_elipse():
    try:
        xc = int(entry_xc.get())
        yc = int(entry_yc.get())
        a = int(entry_raio_a.get())
        b = int(entry_raio_b.get())
        
        # Verifica se o centro da elipse está dentro da grade
        if not (-22 <= xc <= 22 and -22 <= yc <= 22):
            messagebox.showerror("Erro", "O centro da elipse deve estar entre -22 e 22.")
            return
        if a <= 0 or a > 22 or b <= 0 or b > 22:
            messagebox.showerror("Erro", "Os raios devem ser maiores que 0 e menores ou iguais a 22.")
            return

        desenhar_grade(xc, yc, None, a, b)
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira valores inteiros válidos.")

# Criar a interface
root = tk.Tk()
root.title("Desenho de Círculo e Elipse")

# Labels e entradas para o centro da circunferência e o raio
tk.Label(root, text="Centro (xc, yc):").pack()

frame_centro = tk.Frame(root)
frame_centro.pack(pady=5)

entry_xc = tk.Entry(frame_centro, width=5)
entry_xc.pack(side=tk.LEFT, padx=5)
entry_yc = tk.Entry(frame_centro, width=5)
entry_yc.pack(side=tk.LEFT, padx=5)

# Raio para o círculo
tk.Label(root, text="Raio do Círculo:").pack(pady=(10, 0))

frame_raio = tk.Frame(root)
frame_raio.pack(pady=5)

entry_raio = tk.Entry(frame_raio, width=5)
entry_raio.pack(side=tk.LEFT, padx=5)

# Botão para desenhar o círculo
botao_circulo = tk.Button(root, text="Desenhar Círculo", command=obter_dados_circulo)
botao_circulo.pack(pady=10)

# Labels e entradas para os raios da elipse
tk.Label(root, text="Raio Horizontal (a):").pack(pady=(10, 0))

entry_raio_a = tk.Entry(root, width=5)
entry_raio_a.pack(pady=5)

tk.Label(root, text="Raio Vertical (b):").pack(pady=(10, 0))

entry_raio_b = tk.Entry(root, width=5)
entry_raio_b.pack(pady=5)

# Botão para desenhar a elipse
botao_elipse = tk.Button(root, text="Desenhar Elipse", command=obter_dados_elipse)
botao_elipse.pack(pady=20)

# Iniciar a interface
root.mainloop()

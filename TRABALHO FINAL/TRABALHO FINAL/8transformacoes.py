import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import math

# Função para desenhar a grade e as linhas do polígono
def desenhar_grade(polygon):
    plt.clf()  # Limpa o gráfico anterior
    plt.xlim(-12, 12)
    plt.ylim(-12, 12)
    
    # Desenhar a grade
    for x in range(-12, 13):
        plt.axvline(x, color='gray', linestyle='--', linewidth=0.5)
    for y in range(-12, 13):
        plt.axhline(y, color='gray', linestyle='--', linewidth=0.5)

    # Traçar linhas usando o algoritmo de Bresenham
    for i in range(len(polygon)):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % len(polygon)]  # Conectar último vértice ao primeiro
        bresenham(x1, y1, x2, y2)

    plt.grid(True)
    plt.axhline(0, color='black', linewidth=1)  # Eixo X
    plt.axvline(0, color='black', linewidth=1)  # Eixo Y
    plt.show()

# Algoritmo de Bresenham para desenhar as linhas
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

# Função de rotação de um ponto em torno de um pivô
def rotacionar_ponto(ponto, angulo, pivox, pivoy):
    angulo_rad = math.radians(angulo)
    x, y = ponto
    x_rot = pivox + (x - pivox) * math.cos(angulo_rad) - (y - pivoy) * math.sin(angulo_rad)
    y_rot = pivoy + (x - pivox) * math.sin(angulo_rad) + (y - pivoy) * math.cos(angulo_rad)
    return (round(x_rot), round(y_rot))

# Função de translação
def transladar(polygon, dx, dy):
    return [(x + dx, y + dy) for x, y in polygon]

# Função de escala
def escalar(polygon, sx, sy, fixox, fixoy):
    return [(fixox + (x - fixox) * sx, fixoy + (y - fixoy) * sy) for x, y in polygon]

# Função para obter dados do usuário e realizar a rotação
def obter_dados_transformacoes():
    try:
        # Pegar os pontos do polígono
        pontos_poligono = []
        for i in range(num_vertices):
            x = int(entry_pontos[i][0].get())
            y = int(entry_pontos[i][1].get())
            pontos_poligono.append((x, y))

        # Escolher a transformação
        if var_transf.get() == "Rotação":
            angulo = float(entry_angulo.get())
            pivox = int(entry_pivox.get())
            pivoy = int(entry_pivoy.get())
            # Rotacionar os pontos
            poligono_rotacionado = [rotacionar_ponto(p, angulo, pivox, pivoy) for p in pontos_poligono]
            desenhar_grade(poligono_rotacionado)

        elif var_transf.get() == "Translação":
            dx = int(entry_dx.get())
            dy = int(entry_dy.get())
            # Transladar os pontos
            poligono_transladado = transladar(pontos_poligono, dx, dy)
            desenhar_grade(poligono_transladado)

        elif var_transf.get() == "Escala":
            sx = float(entry_sx.get())
            sy = float(entry_sy.get())
            fixox = int(entry_fixox.get())
            fixoy = int(entry_fixoy.get())
            # Escalar os pontos
            poligono_escalado = escalar(pontos_poligono, sx, sy, fixox, fixoy)
            desenhar_grade(poligono_escalado)
    
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira valores válidos.")

# Função para criar entradas de pontos dinamicamente
def criar_entradas_pontos():
    global num_vertices, entry_pontos
    num_vertices = int(entry_num_vertices.get())
    entry_pontos = []
    
    # Limpa entradas existentes
    for widget in frame_pontos.winfo_children():
        widget.destroy()

    # Cria novas entradas
    for i in range(num_vertices):
        frame = tk.Frame(frame_pontos)
        frame.pack(pady=5)
        entry_x = tk.Entry(frame, width=5)
        entry_x.pack(side=tk.LEFT, padx=5)
        entry_y = tk.Entry(frame, width=5)
        entry_y.pack(side=tk.LEFT, padx=5)
        entry_pontos.append((entry_x, entry_y))

# Criar a interface
root = tk.Tk()
root.title("Transformações Geométricas")

# Número de vértices
tk.Label(root, text="Número de Vértices:").pack(pady=(10, 0))
entry_num_vertices = tk.Entry(root, width=5)
entry_num_vertices.pack(pady=5)
botao_definir = tk.Button(root, text="Definir Vértices", command=criar_entradas_pontos)
botao_definir.pack(pady=5)

# Labels e entradas para os pontos do polígono
tk.Label(root, text="Pontos do Polígono (x, y):").pack(pady=(10, 0))

frame_pontos = tk.Frame(root)
frame_pontos.pack(pady=5)

# Opções de transformação
var_transf = tk.StringVar(value="Rotação")

frame_opcoes = tk.Frame(root)
frame_opcoes.pack(pady=10)

tk.Radiobutton(frame_opcoes, text="Rotação", variable=var_transf, value="Rotação").pack(anchor=tk.W)
tk.Radiobutton(frame_opcoes, text="Translação", variable=var_transf, value="Translação").pack(anchor=tk.W)
tk.Radiobutton(frame_opcoes, text="Escala", variable=var_transf, value="Escala").pack(anchor=tk.W)

# Parâmetros para rotação
frame_rotacao = tk.Frame(root)
frame_rotacao.pack(pady=5)

tk.Label(frame_rotacao, text="Ângulo de Rotação:").pack(side=tk.LEFT, padx=5)
entry_angulo = tk.Entry(frame_rotacao, width=5)
entry_angulo.pack(side=tk.LEFT)

tk.Label(frame_rotacao, text="Pivô (x, y):").pack(side=tk.LEFT, padx=5)
entry_pivox = tk.Entry(frame_rotacao, width=5)
entry_pivox.pack(side=tk.LEFT)
entry_pivoy = tk.Entry(frame_rotacao, width=5)
entry_pivoy.pack(side=tk.LEFT)

# Parâmetros para translação
frame_translacao = tk.Frame(root)
frame_translacao.pack(pady=5)

tk.Label(frame_translacao, text="Deslocamento (dx, dy):").pack(side=tk.LEFT, padx=5)
entry_dx = tk.Entry(frame_translacao, width=5)
entry_dx.pack(side=tk.LEFT)
entry_dy = tk.Entry(frame_translacao, width=5)
entry_dy.pack(side=tk.LEFT)

# Parâmetros para escala
frame_escala = tk.Frame(root)
frame_escala.pack(pady=5)

tk.Label(frame_escala, text="Fator de Escala (sx, sy):").pack(side=tk.LEFT, padx=5)
entry_sx = tk.Entry(frame_escala, width=5)
entry_sx.pack(side=tk.LEFT)
entry_sy = tk.Entry(frame_escala, width=5)
entry_sy.pack(side=tk.LEFT)

tk.Label(frame_escala, text="Ponto Fixo (x, y):").pack(side=tk.LEFT, padx=5)
entry_fixox = tk.Entry(frame_escala, width=5)
entry_fixox.pack(side=tk.LEFT)
entry_fixoy = tk.Entry(frame_escala, width=5)
entry_fixoy.pack(side=tk.LEFT)

# Botão para aplicar a transformação
botao = tk.Button(root, text="Aplicar Transformação", command=obter_dados_transformacoes)
botao.pack(pady=20)

# Iniciar a interface
root.mainloop()

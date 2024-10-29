import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox

# Funções para gerar os sólidos
def cube_vertices():
    return np.array([[1, 1, 1], [-1, 1, 1], [-1, -1, 1], [1, -1, 1],
                     [1, 1, -1], [-1, 1, -1], [-1, -1, -1], [1, -1, -1]])

def pyramid_vertices():
    return np.array([[0, 1, 0], [-1, 0, -1], [1, 0, -1], [1, 0, 1], [-1, 0, 1]])

def parallelepiped_vertices():
    return np.array([[1, 1, 1], [-1, 1, 1], [-1, -1, 1], [1, -1, 1],
                     [1, 1, -1], [-1, 1, -1], [-1, -1, -1], [1, -1, -1]])

def prism_vertices():
    return np.array([[1, 1, 1], [-1, 1, 1], [-1, -1, 1], 
                     [0, 1, -1], [1, 1, -1], [-1, 1, -1]])

def tetrahedron_vertices():
    return np.array([[0, 1, 0], [-1, -1, -1], [1, -1, -1], [0, -1, 1]])

# Funções de projeção
def orthogonal_projection(vertices):
    return vertices[:, :2]

def oblique_projection(vertices):
    angle = np.pi / 4  # 45 degrees
    return np.array([
        vertices[:, 0] + vertices[:, 2] * np.cos(angle),
        vertices[:, 1] + vertices[:, 2] * np.sin(angle)
    ]).T[:, :2]

def perspective_projection(vertices, d=2):
    return np.array([
        (d * vertices[:, 0]) / (d + vertices[:, 2]),
        (d * vertices[:, 1]) / (d + vertices[:, 2])
    ]).T

# Algoritmo de Bresenham para desenhar linhas
def bresenham(x1, y1, x2, y2):
    points = []
    dx = x2 - x1
    dy = y2 - y1
    sx = 1 if dx > 0 else -1
    sy = 1 if dy > 0 else -1
    dx = abs(dx)
    dy = abs(dy)
    
    if dx > dy:
        err = dx / 2.0
        while x1 != x2:
            points.append((x1, y1))
            err -= dy
            if err < 0:
                y1 += sy
                err += dx
            x1 += sx
    else:
        err = dy / 2.0
        while y1 != y2:
            points.append((x1, y1))
            err -= dx
            if err < 0:
                x1 += sx
                err += dy
            y1 += sy
    points.append((x2, y2))
    return points

# Função para plotar o gráfico
def plot_shape(vertices, edges, title):
    plt.figure()
    for edge in edges:
        x1, y1 = vertices[edge[0]]
        x2, y2 = vertices[edge[1]]
        line_points = bresenham(int(x1 * 10), int(y1 * 10), int(x2 * 10), int(y2 * 10))
        for point in line_points:
            plt.plot(point[0] / 10, point[1] / 10, 'ko', markersize=1)

    plt.xlim(-22, 22)
    plt.ylim(-22, 22)
    plt.axhline(0, color='gray', lw=0.5)
    plt.axvline(0, color='gray', lw=0.5)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    
    plt.title(title)
    plt.axis('equal')
    plt.show()

# Função principal chamada pelos botões
def generate_shape():
    selected_shapes = [shape for shape, var in zip(shapes, shape_vars) if var.get()]
    if not selected_shapes:
        messagebox.showerror("Erro", "Nenhuma forma selecionada!")
        return
    
    for shape in selected_shapes:
        if shape == "Cubo":
            vertices = cube_vertices()
            edges = [(0, 1), (1, 2), (2, 3), (3, 0),
                     (4, 5), (5, 6), (6, 7), (7, 4),
                     (0, 4), (1, 5), (2, 6), (3, 7)]
        elif shape == "Pirâmide":
            vertices = pyramid_vertices()
            edges = [(0, 1), (0, 2), (0, 3), (0, 4),
                     (1, 2), (2, 3), (3, 4), (4, 1)]
        elif shape == "Paralelepípedo":
            vertices = parallelepiped_vertices()
            edges = [(0, 1), (1, 2), (2, 3), (3, 0),
                     (4, 5), (5, 6), (6, 7), (7, 4),
                     (0, 4), (1, 5), (2, 6), (3, 7)]
        elif shape == "Prisma":
            vertices = prism_vertices()
            edges = [(0, 1), (1, 2), (2, 0), (0, 3), (1, 3), (2, 3)]
        elif shape == "Tetraedro":
            vertices = tetrahedron_vertices()
            edges = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]

        # Chamar as projeções
        return vertices, edges

def generate_projection(projection_type):
    vertices, edges = generate_shape()
    if projection_type == "Ortogonal":
        proj = orthogonal_projection(vertices)
    elif projection_type == "Oblíqua":
        proj = oblique_projection(vertices)
    elif projection_type == "Perspectiva":
        proj = perspective_projection(vertices)
    else:
        messagebox.showerror("Erro", "Tipo de projeção não reconhecido!")
        return
    
    plot_shape(proj, edges, f"{projection_type} - {', '.join(shapes)}")

# Configuração da interface gráfica
root = tk.Tk()
root.title("Projeções de Sólidos")

shapes = ["Cubo", "Pirâmide", "Paralelepípedo", "Prisma", "Tetraedro"]
shape_vars = [tk.IntVar() for _ in shapes]

# Frame para caixas de seleção
for shape, var in zip(shapes, shape_vars):
    tk.Checkbutton(root, text=shape, variable=var).pack(anchor='w')

# Botões para projeção
button_orthogonal = tk.Button(root, text="Projeção Ortogonal", command=lambda: generate_projection("Ortogonal"))
button_orthogonal.pack(pady=5)

button_oblique = tk.Button(root, text="Projeção Oblíqua", command=lambda: generate_projection("Oblíqua"))
button_oblique.pack(pady=5)

button_perspective = tk.Button(root, text="Projeção Perspectiva", command=lambda: generate_projection("Perspectiva"))
button_perspective.pack(pady=5)

root.mainloop()

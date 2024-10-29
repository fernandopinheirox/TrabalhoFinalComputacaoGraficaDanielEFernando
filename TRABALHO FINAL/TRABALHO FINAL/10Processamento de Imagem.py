import tkinter as tk
from tkinter import filedialog, messagebox, Label, Button, Canvas, OptionMenu, StringVar
from PIL import Image, ImageTk
import cv2
import numpy as np


class EdgeDetectionApp:
    def __init__(self, master):
        self.master = master
        master.title("Detecção de Bordas")

        self.label = Label(master, text="Selecione uma imagem e escolha um método de detecção de bordas.")
        self.label.pack()

        self.canvas = Canvas(master, width=600, height=400)
        self.canvas.pack()

        self.load_button = Button(master, text="Carregar Imagem", command=self.load_image)
        self.load_button.pack()

        self.method_var = StringVar(master)
        self.method_var.set("Sobel")  # Valor padrão
        self.method_menu = OptionMenu(master, self.method_var, "Sobel", "Prewitt", "Canny")
        self.method_menu.pack()

        self.detect_button = Button(master, text="Aplicar Detecção de Bordas", command=self.detect_edges)
        self.detect_button.pack()

        self.image = None
        self.photo = None

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = cv2.imread(file_path)
            self.display_image(self.image)

    def detect_edges(self):
        if self.image is not None:
            method = self.method_var.get()
            if method == "Sobel":
                edges = self.sobel_edge_detection(self.image)
            elif method == "Prewitt":
                edges = self.prewitt_edge_detection(self.image)
            elif method == "Canny":
                edges = cv2.Canny(self.image, 100, 200)
            self.display_image(edges)

    def sobel_edge_detection(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        sobel_edges = cv2.magnitude(sobel_x, sobel_y)
        return np.uint8(sobel_edges)

    def prewitt_edge_detection(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        kernel_x = np.array([[1, 0, -1],
                             [1, 0, -1],
                             [1, 0, -1]])
        kernel_y = np.array([[1, 1, 1],
                             [0, 0, 0],
                             [-1, -1, -1]])
        prewitt_x = cv2.filter2D(gray, -1, kernel_x)
        prewitt_y = cv2.filter2D(gray, -1, kernel_y)
        prewitt_edges = cv2.magnitude(prewitt_x, prewitt_y)
        return np.uint8(prewitt_edges)

    def display_image(self, img):
        if len(img.shape) == 2:  # Se a imagem for em escala de cinza
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        else:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        img = Image.fromarray(img)
        self.photo = ImageTk.PhotoImage(img)

        self.canvas.create_image(0, 0, image=self.photo, anchor='nw')
        self.canvas.config(width=img.width(), height=img.height())


class NoiseReductionApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Redução de Ruído em Imagens")

        self.label = Label(master, text="Escolha uma imagem para reduzir o ruído:")
        self.label.pack()

        self.canvas = Canvas(master, width=400, height=400)
        self.canvas.pack()

        self.load_button = Button(master, text="Carregar Imagem", command=self.load_image)
        self.load_button.pack()

        self.mean_button = Button(master, text="Redução de Ruído - Média", command=self.reduce_noise_mean)
        self.mean_button.pack()

        self.median_button = Button(master, text="Redução de Ruído - Mediana", command=self.reduce_noise_median)
        self.median_button.pack()

        self.gaussian_button = Button(master, text="Redução de Ruído - Gaussiana", command=self.reduce_noise_gaussian)
        self.gaussian_button.pack()

        self.image = None
        self.image_path = ""

    def load_image(self):
        self.image_path = filedialog.askopenfilename()
        if self.image_path:
            self.image = cv2.imread(self.image_path)
            self.display_image(self.image)

    def display_image(self, img):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_tk = ImageTk.PhotoImage(img_pil)
        self.canvas.create_image(0, 0, anchor='nw', image=img_tk)
        self.canvas.image = img_tk

    def reduce_noise_mean(self):
        if self.image is not None:
            result = cv2.blur(self.image, (5, 5))
            self.display_image(result)

    def reduce_noise_median(self):
        if self.image is not None:
            result = cv2.medianBlur(self.image, 5)
            self.display_image(result)

    def reduce_noise_gaussian(self):
        if self.image is not None:
            result = cv2.GaussianBlur(self.image, (5, 5), 0)
            self.display_image(result)


class ImageApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Visualizador de Imagens")

        self.frame_image = tk.Frame(self.master)
        self.frame_image.pack(side=tk.LEFT, padx=10, pady=10)

        self.frame_controls = tk.Frame(self.master)
        self.frame_controls.pack(side=tk.RIGHT, padx=10, pady=10)

        self.label_image = tk.Label(self.frame_image)
        self.label_image.pack()

        self.btn_load = tk.Button(self.frame_controls, text="Carregar Imagem", command=self.load_image)
        self.btn_load.pack(pady=10)

        self.btn_gaussian = tk.Button(self.frame_controls, text="Aplicar Filtro Gaussiano", command=self.apply_gaussian)
        self.btn_gaussian.pack(pady=10)

        self.btn_mean = tk.Button(self.frame_controls, text="Aplicar Filtro de Média", command=self.apply_mean)
        self.btn_mean.pack(pady=10)

        self.btn_median = tk.Button(self.frame_controls, text="Aplicar Filtro de Mediana", command=self.apply_median)
        self.btn_median.pack(pady=10)

        self.var_display = tk.StringVar(value="RGB")
        self.radio_rgb = tk.Radiobutton(self.frame_controls, text="RGB", variable=self.var_display, value="RGB", command=self.update_image)
        self.radio_gray = tk.Radiobutton(self.frame_controls, text="Cinza", variable=self.var_display, value="Gray", command=self.update_image)
        self.radio_binary = tk.Radiobutton(self.frame_controls, text="Binário", variable=self.var_display, value="Binary", command=self.update_image)

        self.radio_rgb.pack(anchor=tk.W)
        self.radio_gray.pack(anchor=tk.W)
        self.radio_binary.pack(anchor=tk.W)

        self.image = None
        self.image_path = ""

    def load_image(self):
        self.image_path = filedialog.askopenfilename()
        if self.image_path:
            self.image = cv2.imread(self.image_path)
            self.update_image()

    def apply_gaussian(self):
        if self.image is not None:
            self.image = cv2.GaussianBlur(self.image, (5, 5), 0)
            self.update_image()
        else:
            messagebox.showwarning("Aviso", "Carregue uma imagem primeiro.")

    def apply_mean(self):
        if self.image is not None:
            self.image = cv2.blur(self.image, (5, 5))
            self.update_image()
        else:
            messagebox.showwarning("Aviso", "Carregue uma imagem primeiro.")

    def apply_median(self):
        if self.image is not None:
            self.image = cv2.medianBlur(self.image, 5)
            self.update_image()
        else:
            messagebox.showwarning("Aviso", "Carregue uma imagem primeiro.")

    def update_image(self):
        if self.image is not None:
            if self.var_display.get() == "Gray":
                processed_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            elif self.var_display.get() == "Binary":
                gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
                _, processed_image = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY)
            else:
                processed_image = self.image

            processed_image = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(processed_image)
            img = ImageTk.PhotoImage(img)

            self.label_image.config(image=img)
            self.label

def start_edge_detection():
    edge_window = tk.Toplevel(root)
    EdgeDetectionApp(edge_window)

def start_noise_reduction():
    noise_window = tk.Toplevel(root)
    NoiseReductionApp(noise_window)

def start_image_viewer():
    viewer_window = tk.Toplevel(root)
    ImageApp(viewer_window)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Aplicativo de Processamento de Imagem")

    label = tk.Label(root, text="Escolha uma funcionalidade:")
    label.pack(pady=10)

    btn_edge_detection = tk.Button(root, text="Detecção de Bordas", command=start_edge_detection)
    btn_edge_detection.pack(pady=5)

    btn_noise_reduction = tk.Button(root, text="Redução de Ruído", command=start_noise_reduction)
    btn_noise_reduction.pack(pady=5)

    btn_image_viewer = tk.Button(root, text="Visualizador de Imagem", command=start_image_viewer)
    btn_image_viewer.pack(pady=5)

    root.mainloop()

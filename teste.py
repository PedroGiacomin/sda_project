import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import time

class RealTimeGraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gráficos de Tendência em Tempo Real")

        # Configuração do layout em grade
        self.frame = ttk.Frame(root)
        self.frame.grid(row=0, column=0, sticky="nsew")

        # Criação das figuras e subplots
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1)
        self.fig.tight_layout(pad=3.0)

        # Canvas para o primeiro gráfico
        self.canvas1 = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas1.get_tk_widget().grid(row=0, column=0, rowspan=2, columnspan=2, sticky="nsew")

        # Canvas para o segundo gráfico (usando a mesma figura)
        self.canvas2 = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas2.get_tk_widget().grid(row=2, column=0, rowspan=1, columnspan=2, sticky="nsew")

        # Dados dos gráficos
        self.x_data = []
        self.y1_data = []
        self.y2_data = []

        # Animações para os gráficos
        self.ani1 = FuncAnimation(self.fig, self.update_plot1, interval=1000)
        self.ani2 = FuncAnimation(self.fig, self.update_plot2, interval=1000)

        # Configuração das linhas e colunas do grid
        for i in range(3):
            self.frame.rowconfigure(i, weight=1)
        for i in range(2):
            self.frame.columnconfigure(i, weight=1)

    def update_plot1(self, frame):
        self.x_data.append(time.time())
        self.y1_data.append(random.randint(0, 100))

        # Limita os dados aos últimos 20 pontos
        self.x_data = self.x_data[-20:]
        self.y1_data = self.y1_data[-20:]

        self.ax1.clear()
        self.ax1.plot(self.x_data, self.y1_data, marker='o', color='b')
        self.ax1.set_title('Gráfico 1')

        # Formata o eixo x para mostrar o tempo de forma legível
        self.ax1.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: time.strftime('%H:%M:%S', time.localtime(x))))
        self.fig.autofmt_xdate()

    def update_plot2(self, frame):
        self.x_data.append(time.time())
        self.y2_data.append(random.randint(0, 100))

        # Limita os dados aos últimos 20 pontos
        self.x_data = self.x_data[-20:]
        self.y2_data = self.y2_data[-20:]

        self.ax2.clear()
        self.ax2.plot(self.x_data, self.y2_data, marker='o', color='r')
        self.ax2.set_title('Gráfico 2')

        # Formata o eixo x para mostrar o tempo de forma legível
        self.ax2.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: time.strftime('%H:%M:%S', time.localtime(x))))
        self.fig.autofmt_xdate()

if __name__ == "__main__":
    root = tk.Tk()
    app = RealTimeGraphApp(root)
    root.mainloop()
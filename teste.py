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
        self.root.title("Gráfico de Tendência em Tempo Real")
        
        self.frame = ttk.Frame(root)
        self.frame.pack(fill=tk.BOTH, expand=1)
        
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

        self.x_data = []
        self.y_data = []
        
        self.ani = FuncAnimation(self.fig, self.update_plot, interval=1000)
        
    def update_plot(self, frame):
        self.x_data.append(time.time())
        self.y_data.append(random.randint(0, 100))
        
        # Limita o gráfico aos últimos 20 pontos
        self.x_data = self.x_data[-20:]
        self.y_data = self.y_data[-20:]
        
        self.ax.clear()
        self.ax.plot(self.x_data, self.y_data, marker='o', color='b')
        
        # Formata o eixo x para mostrar o tempo de forma legível
        self.ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: time.strftime('%H:%M:%S', time.localtime(x))))
        
        self.fig.autofmt_xdate()

main_win = tk.Tk()
main_win.title("IHM - Autoforno")
chart1 = RealTimeGraphApp(main_win)




main_win.mainloop()
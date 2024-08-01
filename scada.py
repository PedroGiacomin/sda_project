import socket
import threading as th
import time
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

PORT = 1919
HOST = 'localhost'

TAXA_SHOW = 3
TAXA_AQ = 2 # em segundos
T_SP = 10.0
T = 0.0
Q = 0.0

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
        global T
        self.x_data.append(time.time())
        self.y_data.append(T)
        
        # Limita o gráfico aos últimos 20 pontos
        self.x_data = self.x_data[-20:]
        self.y_data = self.y_data[-20:]
        
        self.ax.clear()
        self.ax.plot(self.x_data, self.y_data, marker='o', color='b')
        
        # Formata o eixo x para mostrar o tempo de forma legível
        self.ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: time.strftime('%H:%M:%S', time.localtime(x))))
        
        self.fig.autofmt_xdate()


# O clienteTCP envia apenas um set_point float
def start_client_tcp():
    global Q, T, T_SP

    # Inicializa o arquivo txt
    with open('historiador.txt', 'w') as file:
        file.write("")

    # Cria um socket TCP/IP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Define o endereço e a porta do servidor
    server_address = (HOST, PORT)
    print(f"Conectando ao servidor em {server_address[0]} na porta {server_address[1]}")
    
    # Conecta ao servidor
    client_socket.connect(server_address)
    

    try:
        while True:
            # Envia dados a cada TAXA_AQ segundos
            time.sleep(TAXA_AQ)
            tsp_mutex.acquire()
            message = str(T_SP)
            tsp_mutex.release()

            client_socket.sendall(message.encode())
            
            # Aguarda resposta
            data = client_socket.recv(64).decode()[1:-1] # recebe como string sem os parenteses tira os parenteses
            print(data)
            data_treated = tuple(map(float, data.split(', ')))

            # Escreve no arquivo txt
            hora_atual = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())
            
            tq_mutex.acquire()
            T = data_treated[0]
            Q = data_treated[1]
            with open('historiador.txt', 'a') as file:
                file.write(f"{hora_atual} \t T: {T} \t Q: {Q}\n")
            tq_mutex.release()
    except (socket.error, Exception) as e:
        print(f"Conexão encerrada: {e}")


if __name__ == "__main__":
    tsp_mutex = th.Lock()
    tq_mutex = th.Lock()

    tcp_thread = th.Thread(target=start_client_tcp)
    tcp_thread.start()

    # # Plota interface
    # tq_mutex.acquire()
    # T_aux = T
    # Q_aux = Q
    # tq_mutex.release()
    
    # root = tk.Tk()
    # app = RealTimeGraphApp(root)
    # root.mainloop()

    tcp_thread.join()

    print("Programa SCADA encerrado.")

    

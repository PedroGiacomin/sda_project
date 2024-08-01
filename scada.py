import socket
import threading as th
import time
import matplotlib.pyplot as plt
import signal


PORT = 1919
HOST = 'localhost'

TAXA_SHOW = 2
TAXA_AQ = 2 # em segundos
T_SP = 250.0
T = 0.0
Q = 0.0

# Evento para sinalizar término das threads
stop_event = th.Event()

# Thread para plotar o gráfico da temperatura em tempo real
def get_TSP_thread():
    global T_SP
    while not stop_event.is_set():
        setpoint = input("Insira o Set Point de temperatura: ")
        tsp_mutex.acquire()
        T_SP = setpoint
        tsp_mutex.release()


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
        while not stop_event.is_set():
            # Envia dados a cada TAXA_AQ segundos
            time.sleep(TAXA_AQ)
            tsp_mutex.acquire()
            message = str(T_SP)
            tsp_mutex.release()

            client_socket.sendall(message.encode())
            
            # Aguarda resposta
            data = client_socket.recv(64).decode()[1:-1] # recebe como string sem os parenteses tira os parenteses
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
    print(" ----------------- PROGRAMA SCADA -----------------")
    
    tsp_mutex = th.Lock()
    tq_mutex = th.Lock()

    tcp_thread = th.Thread(target=start_client_tcp)
    tcp_thread.start()

    time.sleep(1)
    get_TSP_thread = th.Thread(target=get_TSP_thread)
    get_TSP_thread.start()

    plt.ion()
    temperaturas = []
    setpoints = []

    while not stop_event.is_set():
        # le valor
        tq_mutex.acquire()
        temperatura = T
        tq_mutex.release()

        tsp_mutex.acquire()
        setpoint = T_SP
        tsp_mutex.release()

        temperaturas.append(temperatura)
        setpoints.append(float(setpoint))

        plt.figure(1)
        plt.clf()
        plt.plot(temperaturas[-200:], 'b*-')
        plt.plot(setpoints[-200:], 'r-')
        plt.title('Temperatura do alto forno')

        plt.gcf().autofmt_xdate()  # Rota os labels do eixo X para ficarem na diagonal
        
        plt.show()
        plt.pause(TAXA_AQ)

    tcp_thread.join()
    get_TSP_thread.join()

    print("Programa SCADA encerrado.")

    

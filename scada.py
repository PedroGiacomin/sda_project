import socket
import threading as th
import time

PORT = 1919
HOST = 'localhost'

TAXA_SHOW = 3
TAXA_AQ = 2 # em segundos
T_SP = 10.0
T = 11.0
Q = 9.1

# O clienteTCP envia apenas um set_point float
def start_client_tcp():
    global Q, T, T_SP
    # Cria um socket TCP/IP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Define o endereço e a porta do servidor
    server_address = (HOST, PORT)
    print(f"Conectando ao servidor em {server_address[0]} na porta {server_address[1]}")
    
    # Conecta ao servidor
    client_socket.connect(server_address)
    
    while True:
        # Envia dados a cada TAXA_AQ segundos
        time.sleep(TAXA_AQ)
        tsp_mutex.acquire()
        message = str(T_SP)
        tsp_mutex.release()

        client_socket.sendall(message.encode())
        
        # # Aguarda a resposta
        # amount_received = 0
        # amount_expected = len(str(T,Q))
        
        # while amount_received < amount_expected:
        data = client_socket.recv(32)
        #amount_received += len(data)
        tq_mutex.acquire()
        T = tuple(data.decode())[0]
        Q = tuple(data.decode())[1]
        tq_mutex.release()
        # print(f"Recebido: {data.decode()}")

if __name__ == "__main__":
    tsp_mutex = th.Lock()
    tq_mutex = th.Lock()

    tcp_thread = th.Thread(target=start_client_tcp)
    tcp_thread.start()

    while True:
        time.sleep(TAXA_SHOW)
        tq_mutex.acquire()
        print(f"T: {T}\t\tQ: {Q}")
        tq_mutex.release()

    

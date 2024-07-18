import socket
import time 
import threading as th

# Variaveis pelas quais as threads trocam informacoes
T_SP = 0
T = 2.1
Q = 8.3

# Thread ClientOPC
def start_client_opc():
    while not stop_event.is_set():
        #print("Running")
        time.sleep(2)
    
    print("Finalizando thread ClienteOPC...")

# Thread ServerTCP
def start_server_tcp():
    global Q, T, T_SP
    # Cria um socket TCP/IP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Define o endereço e a porta do servidor e faz bind
    server_address = ('localhost', 1919)
    server_socket.bind(server_address)
    
    # Habilita o servidor para aceitar conexões
    server_socket.listen(1)
    print(f"Servidor ouvindo em {server_address[0]} na porta {server_address[1]}")
    
    # Aguarda conexoes
    while True:
        print("Aguardando conexão...")

        # Aceita a conexão
        connection, client_address = server_socket.accept()
        try:
            print(f"Conexão estabelecida com {client_address}")

            while True:
                # Recebe os dados de T_SP e guarda na variavel
                data = connection.recv(32)
                tsp_mutex.acquire()
                T_SP = data.decode()
                tsp_mutex.release()
                
                tq_mutex.acquire()
                message = str((T, Q))
                tq_mutex.release()

                if data:
                    # Envia os dados de volta para o cliente
                    connection.sendall(message.encode())
                else:
                    print("Nenhum dado recebido, encerrando a conexão")
                    break
        finally:
            # Fecha a conexão
            connection.close()
    
        print("Finalizando thread ServerTCP...")

if __name__ == "__main__":
    
    # Declarando objetos
    stop_event = th.Event()
    tsp_mutex = th.Lock()
    tq_mutex = th.Lock()

    # Inicialização das threads
    tcp_thread = th.Thread(target=start_server_tcp)
    opc_thread = th.Thread(target=start_client_opc)
    tcp_thread.start()
    opc_thread.start()

    while True:
        time.sleep(3)
        tsp_mutex.acquire()
        print(f"SetPoint: {T_SP}")
        tsp_mutex.release()
    # Aguarda comando para encerrar o programa
    # tecla = input()
    # print(tecla)
    # while tecla != 'q':
    #     tecla = input()
    #     print(tecla)
    
    print("Encerrando programa...")

    stop_event.set()
    stop_event.set()

    tcp_thread.join()
    opc_thread.join()

    print("Programa encerrado...")

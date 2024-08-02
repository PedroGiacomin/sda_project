from opcua import Client
import socket
import time 
import selectors as sel
import threading as th
import signal
import config

PORT = 1919
HOST = 'localhost'
HOST_OPC = config.SERVER_ADDRESS
TAXA_SCADA = 1

# Variaveis trocadas
T_SP = 0
T = 0.0
Q = 0.0

# Funcao Callback para aceitar conexao do cliente TCP
def accept(sock):
    conn, addr = sock.accept()  # Aceita a conexão
    print(f"Conexão aceita de {addr}")
    conn.setblocking(False)
    selec.register(conn, sel.EVENT_READ, readTCP)

# Funcao Callback para ler dados do socket TCP
def readTCP(conn):
    global Q, T, T_SP
    try:
        # Recebe T_SP do SCADA e retorna T,Q
        data = conn.recv(64)  
        tsp_mutex.acquire()
        T_SP = data.decode()
        tsp_mutex.release()
        
        tq_mutex.acquire()
        message = str((T, Q))
        tq_mutex.release()

        if data:
            # print(f"Recebido: {data.decode()}")
            conn.sendall(message.encode()) 
        else:
            print("Conexão fechada pelo cliente")
            selec.unregister(conn)
            conn.close()

    except Exception as e:
        print(f"Erro ao ler dados: {e}")
        selec.unregister(conn)
        conn.close()

# Thread ClientOPC
def start_client_opc():
    global T, Q, T_SP
    # Seta o cliente OPC
    client = Client(HOST_OPC)
    client.connect()

    # Obtém as variáveis do servidor
    T_aux = client.get_node(config.T_CONFIG)
    Q_aux = client.get_node(config.Q_CONFIG)
    TSP_aux = client.get_node(config.TSP_CONFIG)

    # Atualiza os dados de T e Q a cada 1s para o SCADA
    while not stop_event.is_set():
        tq_mutex.acquire()
        T = T_aux.get_value()
        Q = Q_aux.get_value()
        tq_mutex.release()

        tsp_mutex.acquire()
        TSP_aux.set_value(T_SP)
        tsp_mutex.release()
        
        time.sleep(TAXA_SCADA)
    
    print("Finalizando thread ClienteOPC...")

# Thread ServerTCP
def start_server_tcp():
    server_address = (HOST, PORT)

    # Cria um socket TCP/IP nao bloqueante e configura na porta certa
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setblocking(False)
    server_socket.bind(server_address)
    server_socket.listen(1)
    print(f"Servidor ouvindo em {server_address[0]} na porta {server_address[1]}...")
    
    # Habilita o servidor para aceitar conexões
    selec.register(server_socket, sel.EVENT_READ, accept)
    print("Aguardando conexão...")
    
    # Aguarda conexoes
    while not stop_event.is_set():
        events = selec.select(timeout=1)
        for key, mask in events:
            callback = key.data
            callback(key.fileobj)
    
    print("Finalizando thread ServerTCP...")

if __name__ == "__main__":
    print(" ----------------- PROGRAMA CLP -----------------")

    # Declarando objetos
    stop_event = th.Event()
    selec = sel.DefaultSelector()
    tsp_mutex = th.Lock()
    tq_mutex = th.Lock()

    # Inicialização das threads
    tcp_thread = th.Thread(target=start_server_tcp)
    opc_thread = th.Thread(target=start_client_opc)
    opc_thread.start()
    tcp_thread.start()
    
    tcp_thread.join()
    opc_thread.join()

    print("Programa encerrado.")

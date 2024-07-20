import socket
import time 
import selectors as sel
import threading as th
import subprocess as subp

PORT = 1919
HOST = 'localhost'

# Variaveis trocadas
T_SP = 0
T = 2.1
Q = 8.3

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
        data = conn.recv(32)  
        tsp_mutex.acquire()
        T_SP = data.decode()
        tsp_mutex.release()
        
        tq_mutex.acquire()
        message = str((T, Q))
        tq_mutex.release()

        if data:
            print(f"Recebido: {data.decode()}")
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
    while not stop_event.is_set():
        #print("Running")
        time.sleep(2)
    
    print("Finalizando thread ClienteOPC...")

# Thread ServerTCP
def start_server_tcp():
    global Q, T, T_SP
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
    
    # Declarando objetos
    stop_event = th.Event()
    selec = sel.DefaultSelector()
    tsp_mutex = th.Lock()
    tq_mutex = th.Lock()
    tecla_input = ''

    # Inicialização das threads
    tcp_thread = th.Thread(target=start_server_tcp)
    opc_thread = th.Thread(target=start_client_opc)
    tcp_thread.start()
    opc_thread.start()

    # Aguarda comando para encerrar o programa
    try:
        while tecla_input != 'q': 
            tecla_input = input()
    except KeyboardInterrupt:
        print("Encerrando programa...")
        stop_event.set()
    
    tcp_thread.join()
    opc_thread.join()

    print("Programa encerrado.")

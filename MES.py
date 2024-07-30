from opcua import Client
import time
import config
import threading

# Evento para sinalizar término das threads
stop_event = threading.Event()

# Cria o client
client = Client(config.SERVER_ADDRESS)
client.connect()

# Obtém as variáveis do servidor
T = client.get_node(config.T_CONFIG)
Q = client.get_node(config.Q_CONFIG)
start_time = time.time() - 60

def thread_main():

    while not stop_event.is_set():
        global start_time
        # lê os valores do servidor 
        if time.time() - start_time >= 60:
            valueT = T.get_value()
            valueQ = Q.get_value()
            
            hora_atual = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())
                    
            # Salva os dados coletados no arquivo
            with open('mes.txt', 'a') as file:
                file.write(f"{hora_atual} \t T: {valueT} \t Q: {valueQ}\n")
            start_time = time.time()
        time.sleep(1)

def thread_verificar_tecla():

    while not stop_event.is_set():
        tecla_input = input("Pressione qualquer tecla para encerrar: ")
        stop_event.set()


t1 = threading.Thread(target=thread_main)
t2 = threading.Thread(target=thread_verificar_tecla)

t1.start()
t2.start()

t2.join()
t1.join()

client.disconnect()
print("Programa MES encerrado.")


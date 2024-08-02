from opcua import Client
import time
import config
import threading
import signal

start_time = time.time() - 60

# Evento para sinalizar término das threads
stop_event = threading.Event()

def thread_main():
    with open('mes.txt', 'w') as file:
        file.write("")

    try:
        while True:
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
    except KeyboardInterrupt:
        stop_event.set()

if __name__ == "__main__":
    print(" ----------------- PROGRAMA MES -----------------")
    # Cria o client
    client = Client(config.SERVER_ADDRESS)
    client.connect()

    # Obtém as variáveis do servidor
    T = client.get_node(config.T_CONFIG)
    Q = client.get_node(config.Q_CONFIG)

    t1 = threading.Thread(target=thread_main)
    t1.start()

    t1.join()

    client.disconnect()
    print("Programa MES encerrado.")


from opcua import Client
import time
import threading
import keyboard
from opcua.ua import AttributeIds
import matplotlib.pyplot as plt
# import seaborn as sns
# sns.set()

# Cria o client
client = Client("opc.tcp://ULTRON:53530/OPCUA/SimulationServer")
client.connect()

# Obtém as variáveis do servidor
T = client.get_node("ns=3;i=1008")
Q = client.get_node("ns=3;i=1009")

fim = False


dados_coletados = []
start_time = time.time()


def thread_main():
    global dados_coletados, start_time

    while not fim:
        # lê os valores do servidor 
        valueT = T.get_value()
        valueQ = Q.get_value()
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        
        # Adiciona os dados coletados na lista
        dados_coletados.append(f"{timestamp}, T: {valueT}, Q: {valueQ}")
        
        # Verifica se 1 minuto se passou
        if time.time() - start_time >= 60:
            # Define o nome do arquivo com base no intervalo de tempo
            data_inicio = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(start_time))
            data_fim = time.strftime('%Y-%m-%d_%H-%M-%S')
            nome_arquivo = f"mes_{data_inicio}_{data_fim}.txt"
            
            # Salva os dados coletados no arquivo
            with open(nome_arquivo, 'w') as file:
                file.write('\n'.join(dados_coletados))
            
            # Limpa a lista de dados coletados e reinicia o tempo de início
            dados_coletados = []
            start_time = time.time()

def thread_verificar_tecla():
    global fim
    while True:
        if keyboard.is_pressed('f'):
            fim = True
            print("Encerrando programa MES...")
            break
        time.sleep(0.1)


# Criar e iniciar as threads
t1 = threading.Thread(target=thread_main)
t2 = threading.Thread(target=thread_verificar_tecla)
t1.start()
t2.start()

# Esperar as threads terminarem
t1.join()
t2.join()

client.disconnect()

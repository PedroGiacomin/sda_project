import numpy as np
import matplotlib.pyplot as plt
import threading
import time
import seaborn as sns
import keyboard  # Biblioteca para capturar eventos de teclado
from opcua import Client

sns.set()

# Parâmetros do forno
C_m = 1000  # Capacidade térmica (J/K)
T_amb = 25  # Temperatura ambiente (°C)
R = 50      # Resistência térmica (K/W)

# Parâmetros de controle
T_ref = 250  # Temperatura de referência (°C)
K_p = 50     # Ganho proporcional do controlador
K_i = 1    # Ganho integrativo do controlador
K_d = 10     # Ganho derivativo do controlador
Ts = 0.5     # Intervalo de amostragem

# Variáveis globais para comunicação entre threads
temperatura_atual = T_amb
fluxo_calor_atual = 5000  # Valor inicial do fluxo de calor
integral_erro = 0         # Integral do erro para o controlador PI
erro_anterior = 0         # Erro anterior para o componente derivativo
tempo = []
temperaturas = []

# Variável para sinalizar término das threads
fim = False

# Cria o client
client = Client("opc.tcp://DESKTOP-M6O8D4H:53530/OPCUA/SimulationServer")
client.connect()

T = client.get_node("ns=3;i=1008")
Q = client.get_node("ns=3;i=1009")

def derivada_temperatura(T, Q):
    dTdt = (Q / C_m) - ((T - T_amb) / R)
    return dTdt

def runge_kutta(T, Q, dt):
    k1 = derivada_temperatura(T, Q)
    k2 = derivada_temperatura(T + 0.5 * k1 * dt, Q)
    k3 = derivada_temperatura(T + 0.5 * k2 * dt, Q)
    k4 = derivada_temperatura(T + k3 * dt, Q)
    T_next = T + (k1 + 2*k2 + 2*k3 + k4) * (dt / 6.0)
    return T_next

def simular_alto_forno(T_inicial, tempo_total, dt, fluxo_calor):
    num_pontos = int(tempo_total/dt) + 1
    tempo = np.linspace(0, tempo_total, num_pontos)
    temperatura = np.zeros(num_pontos)
    # Condição inicial
    temperatura[0] = T_inicial
    # Simulação
    for i in range(1, num_pontos):
        temperatura[i] = runge_kutta(temperatura[i-1], fluxo_calor[i-1], dt)
    return tempo, temperatura

lock = threading.Lock()

def thread_auto_forno():
    global temperatura_atual, fluxo_calor_atual, fim, tempo, temperaturas
    dt = 1.0  # Passo de tempo da simulação (s)
    tempo_total = 1.0  # Tempo total de simulação (s) por iteração
    num_pontos = int(tempo_total/dt) + 1
    t = 0  # Tempo inicial
    while not fim:
        lock.acquire()
        fluxo_calor = np.full(num_pontos, fluxo_calor_atual)
        tempo_sim, temperatura = simular_alto_forno(temperatura_atual, tempo_total, dt, fluxo_calor)
        temperatura_atual = temperatura[-1]
        tempo.append(t)
        temperaturas.append(temperatura_atual)
        t += dt
        T.set_value(temperatura_atual)
        lock.release()
        time.sleep(1)

def thread_controle():
    global fluxo_calor_atual, integral_erro, erro_anterior, fim
    while not fim:
        lock.acquire()
        erro = T_ref - temperatura_atual
        integral_erro += erro * Ts 
        derivativo_erro = (erro - erro_anterior) / Ts  
        fluxo_calor_atual = K_p * erro + K_i * integral_erro + K_d * derivativo_erro
        erro_anterior = erro
        Q.set_value(fluxo_calor_atual)
        lock.release()
        time.sleep(0.5)
    

def thread_verificar_tecla():
    global fim
    while True:
        with lock:
            if keyboard.is_pressed('f'):
                fim = True
                print("Encerrando programa...")
                break
        time.sleep(0.1)

# Criar e iniciar as threads
t1 = threading.Thread(target=thread_auto_forno)
t2 = threading.Thread(target=thread_controle)
t3 = threading.Thread(target=thread_verificar_tecla)

t1.start()
t2.start()
t3.start()

# Esperar até que a thread de verificação de tecla termine
t3.join()

# Esperar as outras threads terminarem
t1.join()
t2.join()

# Plotar os resultados
plt.figure(figsize=(10, 6))
plt.plot(tempo, temperaturas, label='Temperatura no alto-forno')
plt.xlabel('Tempo (s)')
plt.ylabel('Temperatura (°C)')
plt.title('Simulação da Dinâmica de um Alto-Forno')
plt.legend()
plt.grid(True)
plt.show()

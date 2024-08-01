# Nesse programa devem ser inseridas todas as informações referentes a configuração do servidor

SERVER_ADDRESS = "opc.tcp://ULTRON:53530/OPCUA/SimulationServer "   # Insira aqui a url do seu servidor 
T_CONFIG = "ns=3;i= 1008" # Insira aqui o nodeId da variável relativa a temperatura criada no servidor
Q_CONFIG = "ns=3;i= 1009" # Insira aqui o nodeId da variável relativa ao fluxo de calor criada no servidor
TSP_CONFIG = "ns=3;i= 1010" # Insira aqui o nodeId da variável relativa à temperatura de Set Point criada no servidor

# README

Siga as instruções a seguir:

1. Clone os arquivos do repositório sda-project para o seu computador;
2. Instale o simulador do servidor OPC-UA chamado "Prosys OPC UA Simulation Server", por [esse endereço](https://ddjbcej.r.af.d.sendibt2.com/tr/cl/m-OP38ihvHD-j1gOH_CV6cf1rmgXAUFO-1og4wcyNQCKAirhNK37EVf3VgosmQ2BaOMNnjUP3kzyTEy9PmA32ey7eUSzLN-cazcIm3oI-q2DZMj9hvRfyBvTKqIDTfCsdIyavg1CFLmtrE1OzzOX4LAvvrGZWRA7EEtKQnrMrquA1aDoyTkm8O3N9DvUr9rU8i4usXw7kgaIKb0p4A6tPKxcDrGHh0y5dBG3uQskLkhzHePi8KINOnpsvO8cOrrePsTxeEXqyXMi2ugvtKsv1-gKUkLrnnqDrmjNEicdBHQMc63Ggfh3jDVcXsxK2JvCMXjpe1Mmt5P1ApKH) ou por [esse outro](https://prosysopc.com/products/opc-ua-simulation-server/);
3. Com o software instalado, o programa deve ser aberto e devem ser criadas 3 novas variáveis numéricas sendo elas T, Q e T_sp.;
4. Após a criação das variáveis e com o servidor rodando, é necessário ir no arquivo config.py e inserir a url do servidor, e o nodeId das três variáveis;
5. Execute o script ```run.py```, que executará automaticamente os programas ```clp.py```, ```scada.py```, ```MES.py``` e ```programa_autoForno.py``` em terminais diferentes;
    - Se por algum motivo o script falhar, execute os programas manualmente em terminais diferentes;
6. Uma janela com o plot da temperatura do alto forno será aberta e a variação da temperatura em tempo real poderá ser observada, com o **Set Point inicial de 250 °C**;
7. Para variar o Set Point, digite o valor desejado no terminal correspondente ao programa ```scada.py```;
8. Para observar os dados do historiador e do MES, abra os arquivos ```historiador.txt``` e ```mes.txt```.
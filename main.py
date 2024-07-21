import subprocess as subp

if __name__ == "main":

    # Inicializacao dos outros programas
    process_clp = subp.Popen(['python', 'clp.py'], creationflags=CREATE_NEW_CONSOLE)
    print("Inicializando programa clp.py...")
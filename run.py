import subprocess
import time
import signal
import platform

def open_program_in_terminal(command, title):
    system_name = platform.system()
    
    if system_name == 'Windows':
        subprocess.Popen(['start', 'cmd', '/k', f'title {title} & python {command}'], shell=True)
    elif system_name == 'Darwin':  # macOS
        script = f'''
            tell application "Terminal"
                do script "echo -n -e \"\\033]0;{title}\\007\"; python {command}"
                set custom title to "{title}"
            end tell'''
        subprocess.Popen(['osascript', '-e', script])
    elif system_name == 'Linux':
        subprocess.Popen(['gnome-terminal', '--title', title, '--', 'bash', '-c', f'echo -ne "\\033]0;{title}\\007"; python {command}'])
    else:
        raise NotImplementedError(f"Unsupported OS: {system_name}")

# Executar cada script Python em um terminal separado com título correspondente
scripts = ["programa_autoForno.py", "clp.py", "scada.py", "MES.py"]
for script in scripts:
    open_program_in_terminal(script, script)
    print(f"Inicializando processo {script}...")
    time.sleep(1)

print("Pressione CTRL-C para encerrar...")

# Esperar os processos (note que a espera será diferente, pois os terminais serão independentes)
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Programa encerrado.")
import subprocess
import time 
import os
# Lista de scripts a ejecutar
current_dir = os.path.dirname(__file__)

scripts = [current_dir+'/mon3.py', current_dir+'/cpu.py', current_dir+'/war_cpu.py',current_dir+'/war_disp.py',current_dir+'/war_logs.py']
# Lista para almacenar los procesos
procesos = []

# Iniciar cada script en un proceso separado
for script in scripts:
    print("-"*30)
    print("Se ejecuto el script",script)
    print("-"*30)
    proceso = subprocess.Popen(['python3', script])
    time.sleep(80)
    procesos.append(proceso)

# Opcional: Esperar a que todos los procesos terminen y capturar sus salidas
for proceso in procesos:
    proceso.wait()

print("Todos los scripts han terminado su ejecución.")

import subprocess

def epmiko(networking, password, host, comandos):
    # Asegúrate de que toda la indentación en esta función utiliza 4 espacios por nivel de indentación
    args = ['./tplink_auto.sh', networking, password, host, comandos] 

    try:
        # Ejecutar el comando y redirigir la salida al archivo
        with open('tplink_auto.txt', 'w') as output_file:
            subprocess.run(args, stdout=output_file, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el comando: {e}")


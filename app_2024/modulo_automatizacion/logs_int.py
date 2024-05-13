import conexion_ssh
import config_logs

def procesar_dispositivos_logs(datos_yaml):
    for grupo in datos_yaml:
        marca = datos_yaml[grupo]['vars']['marca']
        servidorIP= datos_yaml[grupo]['vars']['servidorIP']
        trap= datos_yaml[grupo]['vars']['trap']
        user = datos_yaml[grupo]['vars']['usuario']
        password = datos_yaml[grupo]['vars']['contrasena']
        device_type = datos_yaml[grupo]['vars']['device_type']
       

        for host, config in datos_yaml[grupo]['hosts'].items():
            ip = config['host']
            print(f"Configurando SNMP en {ip} para el dispositivo de marca {marca}...")

            # Diferenciar entre dispositivos usando marca
            if marca == '3COM':
                # Usar Paramiko para dispositivos 3Com
                config_logs.configurar_logs_3com(ip, user, password, servidorIP)
            elif marca == 'HPV1910':
                config_logs.configurar_logs_3com(ip, user, password, servidorIP)
            elif marca == 'TPLINK':
                archivo = config_logs.comandos_logs_tplink(servidorIP, trap)
                conexion_ssh.epmiko(user, password, ip, archivo)
            else:
                # Para Cisco y HP, se utiliza Netmiko
                dispositivo = {
                    'device_type': device_type,
                    'host': ip,
                    'username': user,
                    'password': password,
                }
                # Establecer conexión usando Netmiko
                connection = conexion_ssh.establecer_conexion_netmiko(dispositivo)
                if connection:
                    if marca == 'CISCO':
                        config_logs.configurar_logs_cisco(connection, servidorIP, trap)
                        print('CONFIGURACION EXITOSA')
                    elif marca == 'HPA5120':
                        config_logs.configurar_logs_hp(connection, servidorIP)
                    # No olvides desconectar después de configurar
                    connection.disconnect()
                else:
                    print(f"No se pudo conectar al dispositivo {ip} con Netmiko.")

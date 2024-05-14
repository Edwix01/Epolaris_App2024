import obt_infyam
import teleg
from influxdb import InfluxDBClient
import numpy as np
import time

# Configurar la conexión a la base de datos InfluxDB
client = InfluxDBClient(host='127.0.0.1', port=8086, database='influx')

def obt_cpudata(agentes):
    """
    Funcion para obtener los datos de consumo de cpu por dispositvo. 
    Retorna un valor promediado de consumo en los ultimos 30 min

    Parámetros:
    agentes (list): Lista con las direcciones IP de los dispositivos

    Retunrs:
    infcpuconsum (dict) :  Diccionario con el consumo por dispositivo
    
    """
    infcpuconsum = {}
    datos = []

    for agente in agentes:
        query = f'SELECT ("uso5min") FROM "cpupython" WHERE ("dispositivo" = \'{agente}\') AND time >= now() - 30m AND time <= now() fill(null)'
        # Ejecutar la consulta para el agente actual
        result = client.query(query)
        for point in result.get_points():
            datos.append(float(point["uso5min"]))
    
        des_esta = np.std(datos)
        media = np.mean(datos)
        mediana = np.median(datos)
        pico = max(datos)


        infcpuconsum[agente] = [des_esta,media,pico,mediana]

    # Cerrar la conexión
    client.close()
    return infcpuconsum

def warning_cpu(vn,datacpu):
    """
    Función para emitir una alerta a Telegram mediante un análisis de los datos

    Parámetros:
    datacpu(dict) :  Diccionario con los datos de consumo de cpu por dispositivo

    Returns:
    none
    """


    mdes =""
    detalles=""
    
    for disp in datacpu.keys():
        desviacion = datacpu[disp][0]
        media = datacpu[disp][1]
        pico = datacpu[disp][2]
        mediana = datacpu[disp][3]

        #Clasificación de notificaciones   
        if pico >= vn+2 and mediana >= vn and media >= vn+ 2:
            mdes = "Existio un sobrepico de Consumo"   
        elif desviacion >= 1 and mediana >= vn+0.5 and media >= vn+ 1.5:
            mdes = "Variaciones Suaves de Consumo"
        elif desviacion >= 5 and mediana >= vn+2.5 and media >= vn+ 5:
            mdes = "Variaciones Considerables de Consumo" 
        elif desviacion >= 10 and mediana >= vn+5 and media >= vn+ 8:
            mdes = "Variaciones Graves de Consumo"

        #Detalles de Consumo
        detalles = "--------------NOTIFICACION CPU---------------"+"\n"+mdes+"\nPromedio: " +str(media)[:5]+ "\nMediana:"+str(mediana)[:5]+"\nDesviación: "+str(desviacion)[:5]+"\nVal. Max:"+str(pico)[:5]+"\n---------------------------------------------------------------"

        teleg.enviar_mensaje(detalles)

        


#Pruebas de Funcionamiento
nombreyaml = "/home/edwin/Documents/Prototipo_App2024/Simulación/epopsSimulacion/inventarios/dispositivos.yaml"
datos = obt_infyam.infyam(nombreyaml)
direc = datos.keys()
while True:
    datacpu = obt_cpudata(direc)
    warning_cpu(10,datacpu)
    time.sleep(60*30) #Configurado para 30 minutos
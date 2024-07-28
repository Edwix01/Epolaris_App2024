import bridge_id
import stp_info
import com_conex
import map_int
import stp_blk
import verstp
import time 
import leer
import tp_linkssh
import sh_tplink
import obt_infyam
import obt_tplink
import obt_root
import bridge_id_root
import tree
import os
import dtsnmp
import json

def datos_topologia(nombreyaml):
    datos = obt_infyam.infyam(nombreyaml)
    direc = datos.keys()
    iptp,credenciales = obt_tplink.filtplink(nombreyaml)
    b_root,froot,fifroot = obt_root.obtr(datos,iptp)
    print("Ejecutando Fase 2 - Almacenamiento de Datos")

    #Fase 2
    #Informacion STP
    # Bridge ID, Designed Bridge
    b_id,f1,fif1 = bridge_id.bri_id(direc,datos)
    st_inf,f2,fif2 = stp_info.stp_inf(direc,datos)
    #Proceso extra para conmutadores TPLINK
    sh_tplink.epmiko(credenciales[iptp[0]]["usuario"],credenciales[iptp[0]]["contrasena"], iptp)
    tp_d = leer.fil_bid("b_id.txt")
    stn = tp_linkssh.tplink_id(b_root,st_inf,tp_d,iptp)

    print("Ejecutando Fase 3 - Identificacion de Conexiones")
    #Fase 3
    #Identificación de Conexiones
    l = com_conex.b_conex(direc,b_id,stn)
    #Mapeo de Las etiquetas
    info_int,f3,fif3 = map_int.ma_int(direc,datos)
    nf = verstp.obtener_numeros_despues_del_punto(l)
    nodb,f4,fif4=stp_blk.stp_status(direc,nf,datos)
    ff = f1 or f2 or f3 or f4
    fif = dtsnmp.snmt(fif1,fif2,fif3,fif4)

    #Fase 4 - Despligue del arbol en la web
    print("Ejecutando Fase 4 - Despliegue del Arbol")

    bridge_id_root_dis =  bridge_id_root.obtener_bridge_id_root_switch(direc, datos)
    b_root_gr = bridge_id_root.encontrar_ip_por_bridge_id(bridge_id_root_dis, b_id)
    bloq_int=tree.identificar_interfaces_bloqueadas(nodb, info_int)
    interconnections = tree.generar_arbol_conexiones_web(l,info_int)
    conexiones_blok = tree.marcar_puertos_bloqueados(interconnections, bloq_int)
    hostname = tree.obtener_hostname_dispositivos(direc,datos)
    info_disp = tree.informacion_dispositivos(nombreyaml)

    return direc, interconnections, b_root_gr, conexiones_blok, hostname, info_disp

def good_luck_have_fun():
    current_dir = os.path.dirname(__file__)
    nombreyaml = os.path.join(current_dir, 'inventarios', 'dispositivos.yaml')
    discovered_hosts, interconnections, b_root, conexiones_blok, host_name, info_disp = datos_topologia(nombreyaml)
    RUTA_ARCHIVO_TOPOLOGIA = r"/home/du/Prototipo_App2024/app_2024/src/public/js/topologia_fija.js"
    RUTA_ARCHIVO_DIFERENCIAS_TOPOLOGIA = r"/home/du/Prototipo_App2024/app_2024/src/public/js/topologia_diferencias.js"
    RUTA_ARCHIVO_TOPOLOGIA_CACHE = r"/home/du/Prototipo_App2024/app_2024/src/public/js/topologia_cache.json"

    CABECERA_ARCHIVO_TOPOLOGIA = f"\n\nvar topologyData = "
    DICCIONARIO_TOPOLOGIA = tree.generar_topologia_fija(discovered_hosts, interconnections,b_root,conexiones_blok, host_name, info_disp)
    TOPOLOGIA_CACHE = tree.leer_topologia_cache(RUTA_ARCHIVO_TOPOLOGIA_CACHE)
    tree.guardar_archivo_topologia(DICCIONARIO_TOPOLOGIA, CABECERA_ARCHIVO_TOPOLOGIA, RUTA_ARCHIVO_TOPOLOGIA)
    tree.guardar_topologia_cache(DICCIONARIO_TOPOLOGIA, RUTA_ARCHIVO_TOPOLOGIA_CACHE)

    if TOPOLOGIA_CACHE:
        DATOS_DIFERENCIA = tree.generar_topologia_diferencias(TOPOLOGIA_CACHE, DICCIONARIO_TOPOLOGIA)
        tree.imprimir_diferencias(DATOS_DIFERENCIA)
        tree.guardar_archivo_topologia(DATOS_DIFERENCIA[2], CABECERA_ARCHIVO_TOPOLOGIA, RUTA_ARCHIVO_DIFERENCIAS_TOPOLOGIA)
        # Verifica si hay cambios en los nodos o enlaces
        cambio_topologia = (len(DATOS_DIFERENCIA[0]['added']) > 0 or
                            len(DATOS_DIFERENCIA[0]['deleted']) > 0 or
                            len(DATOS_DIFERENCIA[1]['added']) > 0 or
                            len(DATOS_DIFERENCIA[1]['deleted']) > 0)
        if cambio_topologia:
                with open('/home/du/Prototipo_App2024/app_2024/src/public/js/changes_flag.json', 'w') as f:
                    json.dump({'changes': True}, f)
    else:
        # Guarda la topología actual en el archivo de diferencias si falta el caché
        tree.guardar_archivo_topologia(DICCIONARIO_TOPOLOGIA, CABECERA_ARCHIVO_TOPOLOGIA, RUTA_ARCHIVO_DIFERENCIAS_TOPOLOGIA)


if __name__ == '__main__':
    tiempos_ejecucion = []
    cont = 0

    for i in range(25):
        time_main_ini = time.time()
        good_luck_have_fun()
        time_main_fin = time.time()
        time_main = time_main_fin - time_main_ini
        tiempos_ejecucion.append(time_main)
        
        print('--------------------------------------------------------------------------------------------------')
        print('REPETICION: ', cont)
        print('--------------------------------------------------------------------------------------------------')
        print('--------------------------------------------------------------------------------------------------')
        print('El tiempo para ejecutar el algoritmo de descubrimiento y graficacion de topologia es: ', time_main)
        print('--------------------------------------------------------------------------------------------------')

        cont = cont+1
        if i < 24:  # Pausar solo si no es la última iteración
            time.sleep(10)  # Pausa de 10 segundos

    # Imprimir el vector de tiempos de ejecución al final
    print('Vector de tiempos de ejecución de las 25 simulaciones:')
    print(tiempos_ejecucion)


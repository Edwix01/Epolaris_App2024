import bridge_id
import stp_info
import com_conex
import des_disp
import des_int_act
import map_int
import stp_blk
import verstp
import time
import dtsnmp


direc = ["10.0.1.1","10.0.1.2","10.0.1.3","10.0.1.4","10.0.1.5"]

def main_top(direc):
    #Fase 1
    #print("Ejecutando fase 1")
    # Ingreso de Parametros - Comunidad SNMP, Direcciones IP
    comunidad = "public"
    #direc = des_disp.in_des()

    #Fase 2
    #print("Ejecutando fase 2")
    #Informacion STP
    # Bridge ID, Designed Bridge
    b_id,f1,fif1 = bridge_id.bri_id(direc,comunidad)
    st_inf,f2,fif2 = stp_info.stp_inf(direc,comunidad)
    f = f1 or f2

    fif = dtsnmp.snmt(fif1,fif2)

    l = com_conex.b_conex(direc,b_id,st_inf)
    #print(l)
    #Mapeo de Las etiquetas
    info_int,f3,fif3 = map_int.ma_int(direc,comunidad)
    #print(info_int)

    nf = verstp.obtener_numeros_despues_del_punto(l)
    #print(nf)
    nodb,f4,fif4=stp_blk.stp_status(direc,nf,comunidad)
    #print(nodb)
    ff = f1 or f2 or f3 or f4
    fif = dtsnmp.snmt(fif1,fif2,fif3,fif4)

    """ 
    #Fase 4
    print("Ejecutando Fase 4")
    #Deteccion de puertos habilitados
     con stp


    #Creación del grafo
    info_int = map_int.ma_int(direc,comunidad)
    grafo = gr.crear_grafo(direc, l, info_int,nodb)
    gr.dibujar_grafo(grafo)
    """
    return l,f,fif


#!/bin/bash

#echo "EMPEZANDO CONFIGURACION"
#cd /home/du/Prototipo_App2024/app_2024/Epops
#nohup python3 seg_proact.py > mi_log.log 2>&1 &
#echo "CONFIGURACION EXITOSA"

echo " ------------------------ INICIANDO CONFIGURACION -------------------------- "

# Buscar el directorio app2024/Epops
DIRECTORIO_BASE=$(find / -type d -name "Epops" -path "*/app_2024/Epops" 2>/dev/null | head -n 1)
if [ -z "$DIRECTORIO_BASE" ]; then
  echo "No se pudo encontrar el directorio app_2024/Epops"
  exit 1
fi

# Mostrar el directorio encontrado
echo "Directorio encontrado: $DIRECTORIO_BASE"
# Cambiar al directorio encontrado
cd "$DIRECTORIO_BASE" || { echo "Error al cambiar al directorio $DIRECTORIO_BASE"; exit 1; }
# Ejecutar el script Python con nohup
nohup python3 seg_proact.py > mi_log.log 2>&1 &

echo " ------------------------ CONFIGURACION EXITOSA --------------------------- "

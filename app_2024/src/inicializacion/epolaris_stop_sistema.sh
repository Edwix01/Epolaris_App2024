#!/bin/bash

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
sudo python3 stop_app.py
echo "Aplicación detenida"



#!/bin/bash

echo "EMPEZANDO CONFIGURACION"
cd /home/du/Prototipo_App2024/app_2024/Epops
nohup python3 seg_proact.py > mi_log.log 2>&1 &

echo "CONFIGURACION EXITOSA"

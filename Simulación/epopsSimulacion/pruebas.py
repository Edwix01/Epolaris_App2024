from datetime import datetime, timedelta
import time

# Registrar la hora inicial
start_time = datetime.now()

print(start_time)

# Calcular la hora objetivo (5 minutos después de la hora inicial)
target_time = start_time + timedelta(minutes=1)

print(target_time)
# Bucle para esperar y comprobar si han pasado 5 minutos
while datetime.now() < target_time:
    print("Esperando que pasen 5 minutos...")
    time.sleep(10)  # Dormir por 10 segundos antes de volver a verificar

print("Han pasado 5 minutos")

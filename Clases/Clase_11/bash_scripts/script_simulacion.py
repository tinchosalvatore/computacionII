"""
Cree un script Bash que ejecute en segundo plano un script Python que duerme 10 segundos 

Desde otra terminal, verifique su ejecución con ps, y envíe una señal para terminarlo prematuramente (SIGTERM)
"""
import os
import time
import signal
import sys

def signal_handler(signum, frame):
    print(f"Signal {signum} received, terminating the process.")
    sys.exit(0)

pid = os.fork()

if pid == 0:
    print(f"Soy el hijo {os.getpid()} voy a dormir por 25 segundos, esperanod una señal SIGTERM")
    signal.signal(signal.SIGTERM, signal_handler)
    time.sleep(25)


else:
    os.waitpid(pid, 0)
    print("Ejecucion del scrpit finalizada")
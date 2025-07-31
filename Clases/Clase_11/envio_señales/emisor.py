#!/usr/bin/env python3
"""
Implemente dos scripts: uno que espera indefinidamente (pause) 
y otro que envía señales (SIGUSR1, SIGUSR2) cada cierto tiempo

El receptor deberá reaccionar de forma distinta según la señal recibida.
"""
import os
import signal
import time
import sys
import random

def send_signals(pid):
    random_num = random.randint(1, 5)
    while True:
        print(f"Sending signals to process {pid}")

        time.sleep(random_num)
        os.kill(pid, signal.SIGUSR1)  # os.kill es el kill de UNIX, enviado con os de Python
        print(f"Sent SIGUSR1 to process {pid}")
        
        time.sleep(random_num)
        os.kill(pid, signal.SIGUSR2)
        print(f"Sent SIGUSR2 to process {pid}")
    
def main():
    if len(sys.argv) != 2:
        print("Deberia ejecutarse como 'emisor.py <pid_receptor>'")
        sys.exit(1)
    
    # Recibimos el PID del proceso receptor como argumento, posiblemente desde un pipe
    pid = int(sys.argv[1])
    send_signals(pid)


if __name__ == "__main__":
    main()
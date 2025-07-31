#!/usr/bin/env python3
"""
Implemente dos scripts: uno que espera indefinidamente (pause)
y otro que envía señales (SIGUSR1, SIGUSR2) cada cierto tiempo

El receptor deberá reaccionar de forma distinta según la señal recibida
"""
import os
import signal

def handle_sigusr1(signum, frame):
    print(f"[Receptor {os.getpid()}] Received SIGUSR1: {signum}", flush=True)

def handle_sigusr2(signum, frame):
    print(f"[Receptor {os.getpid()}] Received SIGUSR2: {signum}", flush=True)


signal.signal(signal.SIGUSR1, handle_sigusr1)
signal.signal(signal.SIGUSR2, handle_sigusr2)

print(os.getpid(), flush=True)  # flush asegura que el PID se envía inmediatamente

# Quedar esperando señales indefinidamente
while True:
    signal.pause() 
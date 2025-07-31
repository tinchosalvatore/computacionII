#!/bin/bash 

#Cree un script Bash que ejecute en segundo plano un script Python que duerme 10 segundos
# Desde otra terminal, verifique su ejecución con ps, y envíe una señal para terminarlo prematuramente (SIGTERM)

echo "Soy el coordinador y voy a ejecutar un script Python en segundo plano."

python3 script_simulacion.py &

# COMANDOS, el PID lo muestra el print del script
# ps -p PID
# kill -SIGTERM PID
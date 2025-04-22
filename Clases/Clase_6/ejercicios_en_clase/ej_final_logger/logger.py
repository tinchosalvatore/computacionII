import time

fifo_path = 'canal_logs'

with open(fifo_path, 'r') as fifo:
    with open('log_output.txt', 'a') as archivo_log:
        while True:
            linea = fifo.readline()
            if not linea:
                time.sleep(0.1)
                continue
            timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]")
            entrada = f"{timestamp} {linea}"
            print(entrada.strip())
            archivo_log.write(entrada)
            archivo_log.flush()

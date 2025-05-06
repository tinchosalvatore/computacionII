from multiprocessing import Process, current_process

def mostrar_info():
    print(f"Nombre: {current_process().name}, PID: {current_process().pid}")

if __name__ == '__main__':
    p = Process(target=mostrar_info, name='ProcesoSecundario')      # name cambia el nombre del proceso
    p.start()
    p.join()
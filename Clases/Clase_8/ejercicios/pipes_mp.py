from multiprocessing import Process, Pipe

def hijo(conn):
    conn.send("Hola padre, soy el hijo")
    respuesta = conn.recv()
    print(f"[Hijo] Recibido: {respuesta}")
    conn.close()

if __name__ == '__main__':
    padre_conn, hijo_conn = Pipe()
    p = Process(target=hijo, args=(hijo_conn,))
    p.start()

    mensaje = padre_conn.recv()
    print(f"[Padre] Recibido: {mensaje}")
    padre_conn.send("Hola hijo, recibido el mensaje")
    
    p.join()
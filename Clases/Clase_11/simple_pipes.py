"""
Cree un script en Python donde el proceso padre y el hijo se comuniquen usando un os.pipe().
El hijo deberá enviar un mensaje al padre, y este deberá imprimirlo por pantalla.

Debe usarse codificación binaria y control adecuado de cierre de descriptores.
"""
import os

def main():
    # Crear un pipe
    r, w = os.pipe()

    pid = os.fork()

    if pid == 0: 
        os.close(r)  # Cerramos lectura
        
        # b indica que es un bite string la cual es necesaria para comunicación por pipes 
        message = b"Aguanten las pipes!"  
        
        os.write(w, message)
        os.close(w)  # Al finalizar cerramos escritura

    else:
        os.close(w)
        os.wait()  # Chequeamos que termine el hijo 

        message = os.read(r, 1024)  # Especificamos un tamaño máximo de lectura en el cual seguro esta el mensaje
        os.close(r)

        print (f"Soy el proceso padrea y he recibido: '{message.decode('utf-8')}' desde mi hijo")



if __name__ == "__main__":
    main()
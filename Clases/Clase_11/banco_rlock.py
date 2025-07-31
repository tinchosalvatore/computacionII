"""
Diseñe una clase CuentaBancaria con métodos depositar y retirar, ambos protegidos con un RLock.
Permita que estos métodos se llamen recursivamente (desde otros métodos sincronizados).

Simule accesos concurrentes desde varios procesos.
"""
from threading import Thread, RLock
import time

class CuentaBancaria():
    def __init__(self, saldo_inicial=0):
        self.saldo = saldo_inicial
        self.lock = RLock()

# Vamos a usar el mismo lock en ambos metodos, para eso usamos RLock en vez de Lock Normal
# Tambien vamos a usar Hilos porque comparten memoria, con los procesos se iba a complicar un poco mas esa parte

    def depositar(self, cantidad):
        with self.lock:
            print(f"Depositando {cantidad}.")
            self.saldo += cantidad
            print(f"Saldo actual: {self.saldo}")



    def retirar(self, cantidad):
        with self.lock:
            if cantidad > self.saldo:
                print(f"No se puede retirar {cantidad}. El saldo es insuficiente: {self.saldo}")
                return
            print(f"Retirando {cantidad}.")
            self.saldo -= cantidad
            print(f"Saldo actual: {self.saldo}")

# main se va a encargar de generar procesos segun lo que pida el usuario por input
def main():
    cuenta = CuentaBancaria(0)
    hilos = []

    while True:
        accion = input("Ingrese 'd' para depositar, 'r' para retirar o 'q' para salir: ").strip().lower()
        
        if accion not in ('d', 'r'):
            break
        
        elif accion in ('d', 'r'):
            cantidad = int(input("Ingrese la cantidad: "))
            if accion == 'd':
                hilo = Thread(target=cuenta.depositar, args=(cantidad,))
            elif accion == 'r':
                hilo = Thread(target=cuenta.retirar, args=(cantidad,))
            hilos.append(hilo)
            hilo.start()


    # Una vez que se salio del bucle, hacemos el join de todos los procesos
    for h in hilos:
        h.join()


if __name__ == "__main__":
    print("Bienvenido al sistema de cuentas bancarias")
    print("Saldo actual: 0")
    main()
    print("Gracias por usar el sistema!")
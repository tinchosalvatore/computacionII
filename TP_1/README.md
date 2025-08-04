# Trabajo Práctico 1: "Sistema Concurrente de Análisis Biométrico con Cadena de Bloques Local"
## Martin Salvatore.  Ingeniería en Informática :computer::books:
### Legajo: 63181
---

## :bulb: Descripción :bulb:

Implementa un sistema concurrente en Python que simula señales biométricas-medicas (frecuencia cardíaca, presión arterial y oxígeno), las analiza en paralelo con una ventana móvil de 30 seg, detecta alertas simples, y asegura integridad de los resultados mediante una cadena de bloques local. Finalmente se verifica esa cadena y se genera un reporte en formato .txt

Todo esto haciendo la gestion de sus procesos usando el módulo `multiprocessing` de Python.
---

## :gear: Componentes :gear:

- `main.py`:  
  - Generador de datos biométricos (60 muestras, 1 por segundo).  
  - Analizadores concurrentes de frecuencia, presión y oxígeno (ventana de 30s, media y desviación estándar).  
  - Verificador que agrupa por timestamp, detecta alertas y arma bloques encadenados con hash SHA-256.  
  - Persiste la cadena en `blockchain.json` de forma atómica.

- `verificar.py`:  
  - Lee `blockchain.json`.  
  - Recalcula hashes y verifica encadenamiento.  
  - Detecta bloques corruptos.  
  - Calcula promedios generales (frecuencia, oxígeno, presión sistólica y diastólica) sobre bloques íntegros.  
  - Cuenta bloques con alerta válidos.  
  - Produce un `reporte.txt`.

## :package: Requisitos :package:

- Python 3.9 o superior  
- Módulos estándar usados: `multiprocessing`, `json`, `hashlib`, `os`, `datetime`, `random`
:bulb: Los módulos estándar son parte de la librería estándar de Python, no hace falta instalar ninguna dependencia adicional.
## :rocket: Cómo ejecutar :rocket:

1. Generar los datos y construir la blockchain (Tareas 1 y 2):

```bash
python3 main.py
```
Esto produce una cadena de bloques en blockchain.json y muestra por pantalla cada bloque con su hash y si tiene alerta.

2. Verificar la integridad y generar el reporte (Tarea 3):

```bash
python3 verificar.py
```
Esto genera reporte.txt con:
- Total de bloques.
- Bloques con alerta válidos.
- Bloques corruptos (detalle).
- Promedios generales sobre bloques íntegros: frecuencia, oxígeno, presión sistólica y diastólica.

3. Ver el reporte:
```bash
cat reporte.txt
```
o con un editor de código como `nano` o `vim`.
```bash
nano reporte.txt
```
---

### :alarm: Criterios de alerta de salud :alarm:

Un bloque se marca con "alerta": true si se incumple alguno de:

    Frecuencia >= 200

    Oxígeno fuera de [90,100]

    Presión sistólica >= 200
    (La diastólica no se usa para alerta según el enunciado actual.)

### :page_facing_up: Notas importantes :page_facing_up:

    La persistencia de la cadena es atómica: se escribe en un archivo temporal y luego se reemplaza.

    En la verificación (Tarea 3) se excluyen los bloques corruptos del cálculo de promedios generales.

    El primer bloque usa "prev_hash": "0"*64 como punto de partida.

    verificar.py no modifica la cadena, solo la lee y analiza.

---
### :outbox_tray: Salidas esperadas  :outbox_tray:
#### Formato de un bloque en blockchain.json
```json
{
  "timestamp": "YYYY-MM-DDTHH:MM:SS.ssssss",
  "datos": {
    "frecuencia": {"media": ..., "desv": ...},
    "presion": {
      "media": {"sistolica": ..., "diastolica": ...},
      "desv": {"sistolica": ..., "diastolica": ...}
    },
    "oxigeno": {"media": ..., "desv": ...}
  },
  "alerta": false,
  "prev_hash": "....",  
  "hash": "...."       
}
```
#### Ejemplo parcial de reporte.txt luego de una ejecucion de main.py exitosa:
```txt
Total de bloques: 60
Bloques con alerta (válidos): 5
Bloques corruptos: 0

Promedios (solo bloques íntegros):
  Frecuencia: 123.45
  Oxígeno: 96.78
  Presión sistólica: 142.33
  Presión diastólica: 89.10
```
---
## :lightning: Ejecucion rapida recomendada :lightning:
```bash
python3 main.py
python3 verificar.py
cat reporte.txt
```
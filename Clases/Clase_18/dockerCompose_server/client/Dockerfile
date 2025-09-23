FROM python:3.12-slim
# Imagen basica de python 3.12


WORKDIR /app

# Copiamos el script del cliente
COPY client.py .

# No necesitamos exponer puertos porque el cliente inicia la conexión, a diferencia del servidor
# Ejecutamos el script por defecto
CMD ["python3", "client.py"]
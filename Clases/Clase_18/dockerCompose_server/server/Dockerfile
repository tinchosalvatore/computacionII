FROM python:3.12-slim
# Imagen basica de python 3.12


# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar las dependencias (por ahora no hay)
# COPY requirements.txt ./
# RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el código del servidor
COPY server.py .

# Exponemos el puerto que usará el servidor
EXPOSE 9999

# Comando para ejecutar el servidor
CMD ["python3", "server.py"]
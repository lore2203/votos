# Usamos una imagen de Python ligera
FROM python:3.9-slim

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos la lista de librerías
COPY requirements.txt .

# Instalamos las librerías
RUN pip install -r requirements.txt


COPY . .

# *** AGREGAR ESTA LÍNEA ***
# Cambia los permisos para que todos puedan leer los archivos (necesario para .joblib)
RUN chmod -R a+r /app

# Comando para ejecutar la aplicación usando Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
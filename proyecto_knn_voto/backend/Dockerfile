# Usamos una imagen de Python ligera
FROM python:3.9-slim

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos la lista de librerías
COPY requirements.txt .

# Instalamos las librerías
RUN pip install -r requirements.txt

# Copiamos todo el resto del código (app.py y los .joblib)
COPY . .

# Comando para ejecutar la aplicación usando Gunicorn (servidor de producción)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
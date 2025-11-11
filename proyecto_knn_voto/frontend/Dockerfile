# Usamos una imagen de Nginx (servidor web) súper ligera
FROM nginx:alpine

# Copiamos nuestros 3 archivos (html, css, js) 
# al directorio por defecto de Nginx
COPY . /usr/share/nginx/html

# El puerto 80 es expuesto por Nginx por defecto, 
# así que no necesitamos hacer nada más.
# Usar una imagen base de Python
FROM python:3.9-slim-buster

# Directorio de trabajo
WORKDIR /app

# Copiar requirements e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el proyecto Django
COPY . .

# Script de entrada para esperar a PostgreSQL
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Puerto expuesto (coincide con el de Django)
EXPOSE 8000

# Comando de inicio
CMD ["./entrypoint.sh"]
# Usa una imagen base de Python
FROM python:3.12-slim

# Define el directorio de trabajo
WORKDIR /app

# Copia los archivos de tu proyecto
COPY . /app

# Instala las dependencias del sistema necesarias para mysqlclient
RUN apt-get update && apt-get install -y \
    pkg-config \
    default-libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Actualiza pip
RUN pip install --upgrade pip

# Instala las dependencias de Python
RUN pip install -r requirements.txt

# Expone el puerto 8000
EXPOSE 8000

# Comando para ejecutar Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

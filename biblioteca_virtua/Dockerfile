# Usa una imagen base de Python
FROM python:3.12-slim

# Define el directorio de trabajo
WORKDIR /app

# Instala las dependencias del sistema necesarias para mysqlclient
# Esto se hace primero para aprovechar el caché de Docker
RUN apt-get update && apt-get install -y --no-install-recommends \
    pkg-config \
    default-libmysqlclient-dev \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Actualiza pip
RUN pip install --upgrade pip --default-timeout=1000

# Copia solo requirements.txt primero (para cachés)
COPY requirements.txt /app/
RUN pip install --default-timeout=1000 -r requirements.txt

# Ahora copia el resto del proyecto
COPY . /app

# Expone el puerto 8000
EXPOSE 8000

# Comando para ejecutar Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

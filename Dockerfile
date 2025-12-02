FROM python:3.12-slim

# Establecer zona horaria
ENV TZ=America/Bogota
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    pkg-config \
    default-libmysqlclient-dev \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar requirements primero para aprovechar cachés
COPY biblioteca_virtua/requirements.txt /app/biblioteca_virtua/

# Actualizar pip con timeout largo
RUN pip install --upgrade pip --default-timeout=1000

# Instalar dependencias de Python
RUN pip install --default-timeout=1000 -r biblioteca_virtua/requirements.txt

# Copiar el resto del código
COPY . /app

# Exponer puerto
EXPOSE 8000

# Comando por defecto
CMD ["python", "biblioteca_virtua/manage.py", "runserver", "0.0.0.0:8000"]

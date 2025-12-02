FROM python:3.12-slim

# Establecer zona horaria y configuración
ENV TZ=America/Bogota
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependencias del sistema necesarias para Codeship
RUN apt-get update && apt-get install -y --no-install-recommends \
    pkg-config \
    default-libmysqlclient-dev \
    build-essential \
    git \
    curl \
    wget \
    ssh-client \
    openssh-client \
    rsync \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar requirements primero para aprovechar cachés
COPY biblioteca_virtua/requirements.txt /app/biblioteca_virtua/

# Actualizar pip con timeout largo
RUN pip install --upgrade pip --default-timeout=1000

# Instalar dependencias de Python con timeout
RUN pip install --default-timeout=1000 -r biblioteca_virtua/requirements.txt

# Instalar herramientas adicionales de CI/CD
RUN pip install --default-timeout=1000 \
    coverage \
    codecov \
    pytest \
    pytest-cov

# Copiar el resto del código
COPY . /app

# Crear script de entrada
RUN chmod +x /app/codeship_docker/entrypoint.sh 2>/dev/null || true

# Exponer puerto
EXPOSE 8000

# Comando por defecto
CMD ["sh", "-c", "cd /app/biblioteca_virtua && python manage.py runserver 0.0.0.0:8000"]

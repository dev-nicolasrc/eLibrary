FROM ubuntu:22.04

# Evitar prompts interactivos
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Bogota

# Instalar dependencias básicas
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    wget \
    software-properties-common \
    build-essential \
    apt-transport-https \
    ca-certificates \
    gnupg \
    lsb-release \
    && rm -rf /var/lib/apt/lists/*

# Instalar Python 3.12
RUN add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    python3.12 \
    python3.12-venv \
    python3.12-dev \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Instalar Docker CLI
RUN install -m 0755 -d /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg && \
    chmod a+r /etc/apt/keyrings/docker.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    docker-ce-cli \
    docker-compose-plugin && \
    rm -rf /var/lib/apt/lists/*

# Instalar Node.js (útil para ciertos tests)
RUN curl -sL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    rm -rf /var/lib/apt/lists/*

# Crear usuario travis
RUN useradd -m -s /bin/bash travis && \
    groupadd docker || true && \
    usermod -aG docker travis

# Instalar Ruby (opcional pero usado en Travis)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ruby \
    ruby-dev && \
    rm -rf /var/lib/apt/lists/*

# Instalar herramientas CLI adicionales
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    awscli \
    pytest \
    coverage

# Crear directorio de trabajo
WORKDIR /home/travis/build

# Cambiar a usuario travis
USER travis

# Mostrar versiones instaladas
RUN echo "=== Versiones ===" && \
    python3.12 --version && \
    docker --version && \
    git --version && \
    node --version && \
    ruby --version

# Comando por defecto
CMD ["/bin/bash"]

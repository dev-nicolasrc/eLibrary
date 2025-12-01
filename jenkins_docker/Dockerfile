FROM jenkins/jenkins:2.528.2-lts-jdk21

USER root

# Instalamos Docker CLI, Docker Compose, Git y herramientas útiles
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    git && \
    # Añadimos repositorio oficial de Docker
    install -m 0755 -d /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg && \
    chmod a+r /etc/apt/keyrings/docker.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
    $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    docker-ce-cli \
    docker-compose-plugin && \
    # Limpiamos caché para reducir tamaño de imagen
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Añadimos el usuario jenkins al grupo docker (GID 999 es común en Docker)
RUN groupadd -g 999 docker || true && \
    usermod -aG docker jenkins

# Volvemos al usuario jenkins por seguridad
USER jenkins

# Instalamos plugins recomendados de Jenkins (opcional)
RUN jenkins-plugin-cli --plugins \
    docker-workflow \
    docker-plugin \
    pipeline-stage-view \
    git \
    workflow-aggregator
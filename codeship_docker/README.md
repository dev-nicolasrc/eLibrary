# Codeship CI/CD para eLibrary

Este directorio contiene la configuración para ejecutar Codeship (servicio de CI/CD en la nube).

## Archivos

- **`codeship-services.yml`**: Define los servicios Docker (app + BD)
- **`codeship-steps.yml`**: Define los pasos del pipeline CI/CD
- **`Dockerfile`** (raíz): Imagen Docker principal de la aplicación
- **`docker-compose.yml`** (este directorio): Para pruebas locales
- **`entrypoint.sh`**: Script que ejecuta el pipeline localmente
- **`start-codeship.ps1`**: Script PowerShell para iniciar

## Uso

### Opción 1: Codeship en la Nube (Recomendado)

1. Ve a https://codeship.com/
2. Haz login/signup con GitHub
3. Conecta tu repositorio `eLibrary`
4. Selecciona "Docker" como imagen base
5. Codeship detectará automáticamente `codeship-services.yml` y `codeship-steps.yml`
6. ¡Listo! Codeship ejecutará en cada push

### Opción 2: Probar Localmente

```powershell
# En PowerShell (como administrador)
cd codeship_docker
.\start-codeship.ps1
```

Luego ver logs:
```powershell
docker-compose -f codeship_docker/docker-compose.yml logs -f codeship_app
```

### Opción 3: Ejecutar Pipeline Manualmente

```bash
# Dentro del contenedor
docker-compose -f codeship_docker/docker-compose.yml exec codeship_app bash /app/codeship_docker/entrypoint.sh
```

## Estructura del Pipeline

```
1. Verificar Salud
2. Instalar Dependencias (pip install)
3. Esperar BD (MySQL)
4. Ejecutar Migraciones
5. Pruebas Unitarias
6. Reporte de Cobertura
7. Enviar a Codecov
```

## Variables de Entorno

```yaml
DB_HOST: codeship_db
DB_NAME: biblioteca
DB_USER: usuario
DB_PASSWORD: usuario123
```

## Notificaciones

Codeship soporta:
- ✅ Email
- ✅ Slack
- ✅ GitHub (checks en PRs)
- ✅ Webhooks personalizados

Configura en el panel de Codeship.

## Troubleshooting

### "MySQL connection error"
- Aumenta el tiempo de espera en `wait_for_db`
- Verifica credenciales en `.env`

### "Python packages not found"
- Asegúrate de que `requirements.txt` existe
- Reinstala: `pip install -r biblioteca_virtua/requirements.txt`

### "Docker not found"
- Inicia Docker Desktop primero
- En Linux: `sudo usermod -aG docker $USER`

## Recursos

- [Documentación Codeship](https://codeship.com/documentation)
- [Docker en Codeship](https://documentation.codeship.com/docker/)
- [Variables de entorno](https://documentation.codeship.com/general/projects/project-settings/)

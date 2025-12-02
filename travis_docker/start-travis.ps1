# Script para iniciar Travis CI en Docker

Write-Host "🚀 Iniciando Travis CI local..." -ForegroundColor Cyan

# Verificar Docker
Write-Host "🔍 Verificando Docker..." -ForegroundColor Yellow
docker ps > $null 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Docker no está corriendo. Inicia Docker Desktop." -ForegroundColor Red
    exit 1
}
Write-Host "✅ Docker está corriendo" -ForegroundColor Green

# Ir a carpeta travis_docker
Set-Location "$PSScriptRoot\travis_docker"

# Reconstruir imagen
Write-Host "🔨 Reconstruyendo imagen de Travis CI..." -ForegroundColor Cyan
docker-compose build --no-cache

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Error en la compilación" -ForegroundColor Red
    exit 1
}

# Iniciar contenedor
Write-Host "🚀 Iniciando contenedor Travis CI..." -ForegroundColor Cyan
docker-compose up -d

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Error al iniciar contenedor" -ForegroundColor Red
    exit 1
}

# Dar permisos a Docker socket
Write-Host "🔐 Configurando permisos..." -ForegroundColor Cyan
Start-Sleep -Seconds 2
docker exec travis-ci chmod 666 /var/run/docker.sock 2>$null

# Mostrar status
Write-Host "`n✅ Travis CI iniciado exitosamente!" -ForegroundColor Green
Write-Host "📋 Estado:" -ForegroundColor Cyan
docker-compose ps

Write-Host "`n📝 Para entrar al contenedor:" -ForegroundColor Cyan
Write-Host "   docker exec -it travis-ci bash" -ForegroundColor Yellow

Write-Host "`n🧪 Para ejecutar los tests:" -ForegroundColor Cyan
Write-Host "   docker exec travis-ci bash -c 'cd /home/travis/build/elibrary && bash .travis.sh'" -ForegroundColor Yellow

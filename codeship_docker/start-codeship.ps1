# Script para iniciar Codeship en Docker

Write-Host "🚀 Iniciando Codeship local..." -ForegroundColor Cyan

# Verificar Docker
Write-Host "🔍 Verificando Docker..." -ForegroundColor Yellow
docker ps > $null 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Docker no está corriendo. Inicia Docker Desktop." -ForegroundColor Red
    exit 1
}
Write-Host "✅ Docker está corriendo" -ForegroundColor Green

# Ir a carpeta raíz del proyecto
Set-Location $PSScriptRoot
Set-Location "..\..\"

# Limpiar builds anteriores
Write-Host "🧹 Limpiando builds anteriores..." -ForegroundColor Yellow
docker-compose -f codeship_docker/docker-compose.yml down -v 2>$null
Start-Sleep -Seconds 2

# Reconstruir imagen
Write-Host "🔨 Reconstruyendo imagen de Codeship..." -ForegroundColor Cyan
docker-compose -f codeship_docker/docker-compose.yml build --no-cache

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Error en la compilación" -ForegroundColor Red
    exit 1
}

# Iniciar contenedores
Write-Host "🚀 Iniciando contenedores..." -ForegroundColor Cyan
docker-compose -f codeship_docker/docker-compose.yml up -d

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Error al iniciar contenedores" -ForegroundColor Red
    exit 1
}

# Esperar a que servicios estén listos
Write-Host "⏳ Esperando a que servicios estén listos..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Mostrar status
Write-Host "`n✅ Codeship iniciado exitosamente!" -ForegroundColor Green
Write-Host "📋 Estado:" -ForegroundColor Cyan
docker-compose -f codeship_docker/docker-compose.yml ps

Write-Host "`n📝 Para ver los logs:" -ForegroundColor Cyan
Write-Host "   docker-compose -f codeship_docker/docker-compose.yml logs -f" -ForegroundColor Yellow

Write-Host "`n🧪 Para ejecutar los tests:" -ForegroundColor Cyan
Write-Host "   docker-compose -f codeship_docker/docker-compose.yml exec codeship_app bash /app/codeship_docker/entrypoint.sh" -ForegroundColor Yellow

Write-Host "`n🌐 Aplicación disponible en: http://localhost:8000" -ForegroundColor Green

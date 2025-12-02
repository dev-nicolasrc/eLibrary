#!/bin/bash

# Script para ejecutar el pipeline de Travis CI localmente

set -e  # Exit on error

echo "🚀 =========================================="
echo "   Travis CI Local Build"
echo "=========================================="

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configurar variables de entorno
export DB_HOST=${DB_HOST:-localhost}
export DB_NAME=${DB_NAME:-biblioteca}
export DB_USER=${DB_USER:-usuario}
export DB_PASSWORD=${DB_PASSWORD:-usuario123}

echo -e "${BLUE}📋 Configuración:${NC}"
echo "  DB_HOST: $DB_HOST"
echo "  DB_NAME: $DB_NAME"
echo "  DB_USER: $DB_USER"

# Stage: before_install
echo -e "\n${YELLOW}[1/6] BEFORE_INSTALL${NC}"
echo "Esperando a que MySQL esté listo..."
for i in {30..0}; do
    if mysql -h "$DB_HOST" -e "select 1" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ MySQL está listo${NC}"
        break
    fi
    echo "  Intento $((30-i))/30..."
    sleep 1
done

if [ "$i" = 0 ]; then
    echo -e "${RED}❌ MySQL no respondió a tiempo${NC}"
    exit 1
fi

# Crear base de datos
echo "Configurando base de datos..."
mysql -h "$DB_HOST" -u root -e "CREATE DATABASE IF NOT EXISTS $DB_NAME;" || true
mysql -h "$DB_HOST" -u root -e "CREATE USER '$DB_USER'@'localhost' IDENTIFIED BY '$DB_PASSWORD';" 2>/dev/null || true
mysql -h "$DB_HOST" -u root -e "GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$DB_USER'@'localhost';" || true
mysql -h "$DB_HOST" -u root -e "FLUSH PRIVILEGES;" || true
echo -e "${GREEN}✅ Base de datos configurada${NC}"

# Stage: install
echo -e "\n${YELLOW}[2/6] INSTALL${NC}"
cd /home/travis/build/elibrary/biblioteca_virtua
echo "Instalando dependencias..."
pip install --upgrade pip > /dev/null
pip install -r requirements.txt
echo -e "${GREEN}✅ Dependencias instaladas${NC}"

# Stage: before_script
echo -e "\n${YELLOW}[3/6] BEFORE_SCRIPT${NC}"
echo "Ejecutando migraciones..."
python manage.py migrate
echo -e "${GREEN}✅ Migraciones completadas${NC}"

# Stage: script
echo -e "\n${YELLOW}[4/6] SCRIPT - Pruebas Unitarias${NC}"
echo "Ejecutando pruebas..."
python run_unit_tests.py
echo -e "${GREEN}✅ Pruebas completadas${NC}"

# Stage: coverage
echo -e "\n${YELLOW}[5/6] SCRIPT - Cobertura${NC}"
echo "Generando reporte de cobertura..."
coverage run --source=libros,usuarios,prestamos,core run_unit_tests.py > /dev/null 2>&1
coverage report -m
coverage xml
echo -e "${GREEN}✅ Cobertura generada${NC}"

# Stage: after_success
echo -e "\n${YELLOW}[6/6] AFTER_SUCCESS${NC}"
echo "Enviando reportes..."
pip install codecov > /dev/null
codecov || echo "⚠️  Codecov no disponible"
echo -e "${GREEN}✅ Reportes enviados${NC}"

# Summary
echo -e "\n${GREEN}=========================================="
echo "✅ Pipeline completado exitosamente"
echo "==========================================${NC}\n"

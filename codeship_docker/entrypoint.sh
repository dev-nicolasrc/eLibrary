#!/bin/bash

# Script de entrada para Codeship

set -e

echo "🚀 =========================================="
echo "   Codeship Pipeline"
echo "=========================================="

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Cambiar a directorio de app
cd /app/biblioteca_virtua

# Variables de entorno
export DB_HOST=${DB_HOST:-localhost}
export DB_NAME=${DB_NAME:-biblioteca}
export DB_USER=${DB_USER:-usuario}
export DB_PASSWORD=${DB_PASSWORD:-usuario123}

echo -e "${BLUE}📋 Configuración:${NC}"
echo "  DB_HOST: $DB_HOST"
echo "  DB_NAME: $DB_NAME"
echo "  DB_USER: $DB_USER"

# Función para ejecutar comando con manejo de errores
run_step() {
    local step_name=$1
    local step_num=$2
    local total_steps=$3
    shift 3
    
    echo -e "\n${YELLOW}[$step_num/$total_steps] $step_name${NC}"
    if "$@"; then
        echo -e "${GREEN}✅ $step_name completado${NC}"
    else
        echo -e "${RED}❌ $step_name falló${NC}"
        exit 1
    fi
}

# Step 1: Esperar BD
echo -e "\n${YELLOW}[1/7] ESPERANDO BD${NC}"
echo "Esperando a que MySQL esté listo..."
for i in {60..0}; do
    if python -c "import MySQLdb; MySQLdb.connect(host='$DB_HOST', user='$DB_USER', passwd='$DB_PASSWORD', db='$DB_NAME')" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ MySQL está listo${NC}"
        break
    fi
    if [ $((i % 10)) -eq 0 ]; then
        echo "  Intento $((60-i))/60..."
    fi
    sleep 1
done

if [ "$i" = 0 ]; then
    echo -e "${RED}❌ MySQL no respondió a tiempo${NC}"
    exit 1
fi

# Step 2: Instalar dependencias
run_step "Instalar Dependencias" 2 7 \
    pip install --upgrade pip -q && pip install -r requirements.txt -q

# Step 3: Migraciones
run_step "Ejecutar Migraciones" 3 7 \
    python manage.py migrate

# Step 4: Pruebas Unitarias
run_step "Pruebas Unitarias" 4 7 \
    python run_unit_tests.py

# Step 5: Generar Cobertura
echo -e "\n${YELLOW}[5/7] GENERAR COBERTURA${NC}"
echo "Generando reporte de cobertura..."
coverage run --source=libros,usuarios,prestamos,core run_unit_tests.py > /dev/null 2>&1
coverage report -m
coverage xml
echo -e "${GREEN}✅ Cobertura generada${NC}"

# Step 6: Verificar sintaxis
run_step "Verificar Sintaxis" 6 7 \
    python -m py_compile libros/*.py usuarios/*.py prestamos/*.py core/*.py

# Step 7: Enviar Cobertura a Codecov
echo -e "\n${YELLOW}[7/7] ENVIAR COBERTURA${NC}"
echo "Enviando reporte de cobertura a Codecov..."
pip install codecov -q 2>/dev/null || true
codecov 2>/dev/null || echo -e "${YELLOW}⚠️  Codecov no disponible (configuración opcional)${NC}"
echo -e "${GREEN}✅ Reporte enviado${NC}"

# Summary
echo -e "\n${GREEN}=========================================="
echo "✅ Pipeline completado exitosamente"
echo "==========================================${NC}\n"

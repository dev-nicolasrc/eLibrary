#!/usr/bin/env python
"""
Ejecuta solo los tests unitarios mockeados (ViewTest)
que NO requieren base de datos
"""
import os
import sys
from pathlib import Path

# CRÍTICO: Establecer TESTING=1 ANTES de cualquier importación de Django
# Esto previene que Django intente usar MySQL
os.environ['TESTING'] = '1'

# Usar settings.py que ahora detecta automáticamente cuando se ejecutan tests
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'biblioteca_virtua.settings')

# Inicializar Django
import django
django.setup()

# Verificar que la configuración es correcta
from django.conf import settings
from django.db import connection

print("⚙️ MODO TEST: Verificando configuración de base de datos")
print(f"   Base de datos configurada: {settings.DATABASES['default']['ENGINE']}")
print(f"   NAME: {settings.DATABASES['default']['NAME']}")
print(f"   Conexión activa: {connection.settings_dict['ENGINE']}")

# Verificar que estamos usando SQLite
if 'mysql' in connection.settings_dict['ENGINE'].lower():
    print("   ❌ ERROR: Django está intentando usar MySQL en lugar de SQLite!")
    print("   Esto no debería suceder. Verifica la configuración.")
    sys.exit(1)

# Importar unittest después de configurar Django
import unittest

if __name__ == '__main__':
    # Verificar una vez más que estamos usando SQLite
    db_engine = settings.DATABASES['default']['ENGINE']
    if 'sqlite' not in db_engine.lower():
        print(f"❌ ERROR: Base de datos configurada incorrectamente: {db_engine}")
        print("   Se esperaba SQLite pero se encontró otra configuración.")
        sys.exit(1)
    
    # Crear test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Cargar solo los tests que usan unittest.TestCase (ViewTest)
    # Estos NO requieren base de datos porque usan mocks
    suite.addTests(loader.loadTestsFromName('libros.tests.LibroViewTest'))
    suite.addTests(loader.loadTestsFromName('usuarios.tests.UsuarioViewTest'))
    suite.addTests(loader.loadTestsFromName('prestamos.tests.PrestamoViewTest'))
    
    print("=" * 70)
    print("🧪 EJECUTANDO TESTS UNITARIOS CON MOCKS (usando SQLite en memoria)")
    print("=" * 70)
    
    # Ejecutar tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Exit code
    sys.exit(0 if result.wasSuccessful() else 1)

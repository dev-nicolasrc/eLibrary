#!/usr/bin/env python
"""
Script para ejecutar tests con SQLite en memoria
NO usa settings.py, configura todo directamente
"""
import os
import sys
from pathlib import Path

# Determinar BASE_DIR
BASE_DIR = Path(__file__).resolve().parent

# NO establecer DJANGO_SETTINGS_MODULE
# Vamos a configurar manualmente TODO

# Importar Django
from django.conf import settings

# Configurar Django manualmente (sin usar settings.py)
settings.configure(
    DEBUG=True,
    BASE_DIR=BASE_DIR,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    INSTALLED_APPS=[
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'core',
        'usuarios',
        'libros',
        'prestamos',
    ],
    SECRET_KEY='test-secret-key-for-testing-only',
    ROOT_URLCONF='biblioteca_virtua.urls',
    MIDDLEWARE=[
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ],
    TEMPLATES=[{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'biblioteca_virtua' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    }],
    STATIC_URL='/static/',
    DEFAULT_AUTO_FIELD='django.db.models.BigAutoField',
    AUTH_USER_MODEL='auth.User',
)

print("⚙️ MODO TEST: SQLite configurado manualmente")
print(f"   Base de datos: {settings.DATABASES['default']['ENGINE']}")
print(f"   Templates DIR: {settings.TEMPLATES[0]['DIRS']}")

# Ejecutar el comando test
if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    
    # Construir argumentos para el comando test
    argv = ['manage.py', 'test'] + sys.argv[1:]
    
    print(f"   Ejecutando: {' '.join(argv)}\n")
    execute_from_command_line(argv)

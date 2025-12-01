"""
Comando personalizado para ejecutar tests con SQLite
"""
from django.core.management.commands.test import Command as TestCommand
from django.conf import settings


class Command(TestCommand):
    help = 'Ejecuta tests usando SQLite en memoria en lugar de la base de datos configurada'

    def handle(self, *args, **options):
        # Forzar el uso de SQLite en memoria
        settings.DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        }
        
        print("⚙️ Ejecutando tests con SQLite en memoria")
        
        # Ejecutar el comando test normal
        super().handle(*args, **options)

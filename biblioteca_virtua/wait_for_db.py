import time
import MySQLdb
import os
import sys

db_host = os.getenv("DB_HOST", "db")
db_user = os.getenv("DB_USER", "usuario")
db_pass = os.getenv("DB_PASSWORD", "usuario123")
db_name = os.getenv("DB_NAME", "biblioteca")

print("⏳ Esperando a que la base de datos esté lista...")
print(f"📍 Conectando a: {db_host} (usuario: {db_user})")

max_attempts = 60  # 60 * 3 = 180 segundos (3 minutos)
attempt = 0

while attempt < max_attempts:
    try:
        conn = MySQLdb.connect(
            host=db_host,
            user=db_user,
            passwd=db_pass,
            db=db_name,
            connect_timeout=5
        )
        conn.close()
        print("✅ Base de datos lista y disponible.")
        sys.exit(0)
    except MySQLdb.OperationalError as e:
        attempt += 1
        print(f"⚠️  Intento {attempt}/{max_attempts}: Base de datos no disponible. Error: {e}")
        if attempt < max_attempts:
            time.sleep(3)
        else:
            print("❌ Timeout: No se pudo conectar a la base de datos después de 3 minutos")
            sys.exit(1)
    except Exception as e:
        attempt += 1
        print(f"❌ Error inesperado (Intento {attempt}/{max_attempts}): {e}")
        if attempt < max_attempts:
            time.sleep(3)
        else:
            sys.exit(1)

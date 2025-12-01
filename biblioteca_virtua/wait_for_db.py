import time
import MySQLdb
import os

db_host = os.getenv("DB_HOST", "db")
db_user = os.getenv("DB_USER", "usuario")
db_pass = os.getenv("DB_PASSWORD", "usuario123")
db_name = os.getenv("DB_NAME", "biblioteca")

print("⏳ Esperando a que la base de datos esté lista...")

while True:
    try:
        conn = MySQLdb.connect(
            host=db_host,
            user=db_user,
            passwd=db_pass,
            db=db_name
        )
        conn.close()
        print("✅ Base de datos lista y disponible.")
        break
    except MySQLdb.OperationalError:
        print("⚠️  Base de datos no disponible todavía. Reintentando en 3 segundos...")
        time.sleep(3)

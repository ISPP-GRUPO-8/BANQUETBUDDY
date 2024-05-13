"""
Script: delete_all_tables.py

Descripción:
Este script se utiliza para eliminar todas las tablas de nuestra base de datos.
Es útil para limpiar la base de datos sin tener que eliminarla.

Advertencia: Este script eliminará permanentemente todas las tablas y los datos contenidos en ellas.
"""

import psycopg2

def delete_all_tables(dbname, user, password, host):
    try:
        print("Conectando a la base de datos...")
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
        cur = conn.cursor()
        print("Conexión establecida.")

        # Obtener todas las tablas
        print("Obteniendo lista de tablas...")
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        tables = cur.fetchall()
        print(f"Se encontraron {len(tables)} tablas.")

        # Eliminar todas las tablas
        for table in tables:
            print(f"Eliminando tabla: {table[0]}...")
            cur.execute(f"DROP TABLE {table[0]} CASCADE")
            conn.commit()
        print("Todas las tablas han sido eliminadas.")

        cur.close()
        conn.close()
    except Exception as e:
        print(f"Ocurrió un error: {e}")

# Configuración de conexión a la base de datos
dbname = "ispp"
user = "ispp"
password = "ispp"
host = "localhost"

delete_all_tables(dbname, user, password, host)

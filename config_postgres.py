import psycopg2

try:
    conexion = psycopg2.connect(
    database='empleados',
    user='postgres',
    password='root'
    )

    print("Connection successful")
except psycopg2.DatabaseError as e:
    print(f"Error {e}")
finally:
        if conexion:
            conexion.close()
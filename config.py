import mysql
import mysql.connector


#Database
config = {
'user' : 'root',
'password' : 'root',
'host' : 'localhost',
'database' : 'empleados'
}

# Establecer la conexión
try:
    connection = mysql.connector.connect(**config)
    if connection.is_connected():
        print("Conexión exitosa a la base de datos")
except mysql.connector.Error as err:
    print(f"Error: {err}")
# finally:
#     if connection.is_connected():
#         connection.close()
#         print("Conexión cerrada")
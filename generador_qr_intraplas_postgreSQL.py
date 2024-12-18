import pyqrcode
import png
import os
import psycopg2
from psycopg2 import Error

def generar_codigos_qr(QR_INTRAPLAS):
    """
    Genera códigos QR únicos para cada empleado desde la base de datos PostgreSQL
    
    :param QR_INTRAPLAS: Directorio donde se guardarán los códigos QR
    """
    try:
        # Configuración de conexión a la base de datos PostgreSQL
        conexion = psycopg2.connect(
            host='localhost',        # Cambia esto por tu host
            database='empleados',    # Nombre de tu base de datos
            user='postgres',         # Tu nombre de usuario de PostgreSQL
            password='postgres'      # Tu contraseña de PostgreSQL
        )
        
        # Asegurar que la carpeta de salida exista
        if not os.path.exists(QR_INTRAPLAS):
            os.makedirs(QR_INTRAPLAS)
        
        # Crear un objeto cursor
        cursor = conexion.cursor()
        
        # Consulta para obtener información de empleados
        consulta = """ SELECT id, nombre, departamento FROM empleados_info """
        
        # Ejecutar la consulta
        cursor.execute(consulta)
        
        # Obtener todos los empleados
        empleados = cursor.fetchall()
        
        # Contador para seguimiento
        total_generados = 0
        
        # Generar código QR para cada empleado
        for empleado in empleados:
            # Desempaquetar detalles del empleado
            id = empleado[0]
            nombre = empleado[1]
            departamento = empleado[2]
            
            # Crear identificador único 
            id_unico = f"{id}"
            
            # Crear código QR
            qr = pyqrcode.create(id_unico, error='L')
            
            # Generar nombre de archivo 
            # Eliminar caracteres especiales del nombre para evitar errores
            nombre_limpio = ''.join(c for c in nombre if c.isalnum())
            departamento_limpio = ''.join(c for c in departamento if c.isalnum())
            
            nombre_archivo = f"{nombre_limpio}_{departamento_limpio}_{id}.png"
            ruta_archivo = os.path.join(QR_INTRAPLAS, nombre_archivo)
            
            # Guardar código QR
            qr.png(ruta_archivo, scale=6)
            
            total_generados += 1
            print(f"Generado código QR para {nombre} {departamento}")
        
        # Imprimir resumen
        print(f"\n--- Resumen ---")
        print(f"Total de códigos QR generados: {total_generados}")
        
        # Cerrar cursor y conexión
        cursor.close()
        conexion.close()
        
    except (Error, psycopg2.Error) as error:
        print(f"Error al conectar o generar códigos QR: {error}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

# Definir la carpeta de salida
QR_INTRAPLAS = 'C:/Users/andres.salcedo.INTRAPLAS/Desktop/Codigos_qr_intraplas/QR_INTRAPLAS'

# Llamar a la función para generar códigos QR
generar_codigos_qr(QR_INTRAPLAS)
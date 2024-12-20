import cv2
from pyzbar.pyzbar import decode
import numpy as np
from datetime import datetime
import openpyxl as xl
import time
import os
import psycopg2


class EscanerQR:
    def __init__(self):
        # Configuración de conexión a la base de datos PostgreSQL
        self.conexion = psycopg2.connect(
            host='localhost',
            database='empleados_id',
            user='postgres',
            password='root'
        )
        self.cursor = self.conexion.cursor(dictionary=True)
        
        # Configuración de la cámara
        self.cap = cv2.VideoCapture(0)
        
        # Variables de registro
        self.codigos_registrados = set()
        
        # Carpeta de destino para registros
        self.carpeta_destino = 'C:/Users/andres.salcedo.INTRAPLAS/Desktop/Codigos_qr_intraplas/registro_entradas'
        
        # Verificar existencia de la carpeta
        if not os.path.exists(self.carpeta_destino):
            os.makedirs(self.carpeta_destino)

    def validar_codigo_qr(self, codigo):
        
        #Valida el código QR contra la base de datos de empleados
        try:
            # Consulta para buscar el empleados_id
            consulta = """ SELECT id, nombre, departamento, Tokens FROM empleados_id WHERE id = %s """

            # Ejecutar consulta
            self.cursor.execute(consulta, (codigo,))
            
            # Obtener resultado
            empleados_id = self.cursor.fetchone()
            
            return empleados_id
        except Exception as e:
            print(f"Error al validar código: {e}")
            return None

    def registrar_entrada(self, empleados_id,Tokens,  hora, fecha):
        
        #Registra la entrada del empleados_id en un archivo Excel
        try:
            # Crear libro de Excel
            wb = xl.Workbook()
            hoja = wb.active
            hoja.title = "Consumo_tokens"
            
            # Encabezados
            hoja['A1'] = 'ID'
            hoja['B1'] = 'NOMBRE'
            hoja['C1'] = 'AREA'
            hoja['D1'] = 'TOKENS'
            hoja['E1'] = 'FECHA'
            hoja['F1'] = 'HORA'
            
            # Datos
            hoja['A2'] = empleados_id['id']
            hoja['B2'] = f"{empleados_id['nombre']}" 
            hoja['C2'] = f"{empleados_id['departamento']}"
            hoja['D2'] = f"{empleados_id['Tokens']}"
            hoja['E2'] = fecha
            hoja['F2'] = hora
            
            # Nombre de archivo
            nombre_archivo = f"{fecha}.xlsx"
            ruta_completa = os.path.join(self.carpeta_destino, nombre_archivo)
            
            # Guardar
            
            wb.save(ruta_completa)
            print(f"Token de almuerzo de {empleados_id['nombre']} del area {empleados_id['departamento']} fue consumido el {fecha} a las {hora} tokens restantes: {Tokens}")
        
        except Exception as e:
            print(f"Error al registrar entrada: {e}")

    def iniciar_escaneo(self):
        
        #Iniciar el escaneo continuo de códigos QR
        while True:
            # Leer frame
            ret, frame = self.cap.read()
            
            # Mostrar instrucciones
            cv2.putText(frame, 'Presiona ESC para salir', (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
            
            # Área de escaneo
            cv2.rectangle(frame, (170, 100), (470, 400), (0, 255, 0), 2)
            
            # Obtener hora y fecha
            hora = datetime.now().strftime('%H:%M:%S')
            fecha = datetime.now().strftime('%Y-%m-%d')
            
            # Decodificar QR
            for codigo_qr in decode(frame):
                # Extraer información
                codigo = codigo_qr.data.decode('utf-8')
                
                # Validar y registrar si no ha sido registrado
                if codigo not in self.codigos_registrados:
                    # Buscar empleados_id
                    empleados_id = self.validar_codigo_qr(codigo)
                    
                    if empleados_id:
                        # Registrar entrada
                        self.registrar_entrada(empleados_id, hora, fecha)
                        
                        # Marcar como registrado
                        self.codigos_registrados.add(codigo)
                        
                        # Dibujar en el frame
                        pts = np.array([codigo_qr.polygon], np.int32)
                        pts = pts.reshape((-1, 1, 2))
                        cv2.polylines(frame, [pts], True, (0, 255, 0), 5)
                        cv2.putText(frame, 'ENTRADA REGISTRADA', 
                                    (codigo_qr.rect.left, codigo_qr.rect.top - 30), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                    else:
                         # QR no válido
                         cv2.putText(frame, 'QR NO RECONOCIDO', 
                                     (codigo_qr.rect.left, codigo_qr.rect.top - 30), 
                                     cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                         
                elif codigo in self.codigos_registrados:
                     # Dibujar en el frame
                        pts = np.array([codigo_qr.polygon], np.int32)
                        pts = pts.reshape((-1, 1, 2))
                        cv2.polylines(frame, [pts], True, (0, 255, 0), 5)
                        cv2.putText(frame, 'REGISTRO YA EXISTENTE', 
                                    (codigo_qr.rect.left, codigo_qr.rect.top - 30), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        print(f"{empleados_id['nombre']} ya cuenta con una entrada registrada")         
            
            # Mostrar frame
            cv2.imshow('Escáner QR', frame)
            
            # Salir con ESC
            if cv2.waitKey(1) == 27:
                break
        
        # Limpiar
        self.cap.release()
        cv2.destroyAllWindows()
        self.conexion.close()

# Iniciar escáner
if __name__ == "__main__":
    escaner = EscanerQR()
    escaner.iniciar_escaneo()
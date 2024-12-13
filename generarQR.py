import pyqrcode
import png
from pyqrcode import QRCode
import os

# Ruta de destino de la carpeta
carpeta_destino = 'C:/Users/VIVOBOOK/Desktop/Asistencias QR/QR'  # Cambia la ruta según tu necesidad

# Asegúrate de que la carpeta de destino exista, si no, créala
if not os.path.exists(carpeta_destino):
    os.makedirs(carpeta_destino)

# Contador
con = 100

# Generamos el código QR
while con <= 102:
    roster = con 
    id = '71' + str(con)
    
    # Creamos los QR
    qr = pyqrcode.create(id, error='L')
    
    # Especificamos la ruta completa al guardar el archivo
    archivo_destino = os.path.join(carpeta_destino, 'G' + str(roster) + '.png')
    
    # Guardamos los QR en la carpeta de destino
    qr.png(archivo_destino, scale=6)

    # Aumentamos el contador
    con = con + 1

while con <= 105:
    roster = con 
    id = '69' + str(con)
    
    # Creamos los QR
    qr = pyqrcode.create(id, error='L')
    
    # Especificamos la ruta completa al guardar el archivo
    archivo_destino = os.path.join(carpeta_destino, 'E' + str(roster) + '.png')
    
    # Guardamos los QR en la carpeta de destino
    qr.png(archivo_destino, scale=6)

    # Aumentamos el contador
    con = con + 1

while con <= 108:
    roster = con 
    id = '83' + str(con)
    
    # Creamos los QR
    qr = pyqrcode.create(id, error='L')
    
    # Especificamos la ruta completa al guardar el archivo
    archivo_destino = os.path.join(carpeta_destino, 'C' + str(roster) + '.png')
    
    # Guardamos los QR en la carpeta de destino
    qr.png(archivo_destino, scale=6)

    # Aumentamos el contador
    con = con + 1
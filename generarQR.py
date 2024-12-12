import pyqrcode
from pyqrcode import QRCode
import png


#CODIGOS QR

con = 100

#Generamos el codigo QR
while con <= 102:

    roster = con 
    id = '71' + str(con)
    #Creamos los QR
    qr = pyqrcode.create(71 and id, error = 'L')
    #Guardamos los QR
    qr.png('G' + str(roster) + '.png', scale = 6)

    #Aumentamos el contador
    con = con + 1
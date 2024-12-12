import cv2
# import pyqrcode 
# import png
# from pyqrcode import QRCode
from pyzbar.pyzbar import decode
import numpy as np


#Creamos la videocaptura
cap = cv2.VideoCapture(0)


while True: 
    #leemos los frames 
    ret, frame = cap.read()

    #leemos los codigos QR 
    for codes in decode(frame):

        #Decodificamos los codigos QR
        info = codes.data.decode('utf-8')

        #Tipos de codigos QR
        tipo = info[0:2]
        tipo = int(tipo)


        #Extraemos coordenadas  
        pts = np.array([codes.polygon], np.int32)
        xi, yi = codes.rect.left, codes.rect.top


        #Redireccionamos 
        pts = pts.reshape((-1, 1, 2))

        if tipo == 71:
            #Dibujamos el rectangulo
            cv2.polylines(frame, [pts], True, (255, 255, 0), 5)
            cv2.putText(frame, 'G0' + (info[2:]), (xi - 15, yi - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
            print("Entrada registrada exitosamente \n"
                  "id: G", str(info[2:]))
            

    #Mostramos el frame
    cv2.imshow('LECTOR DE QR', frame)
    t = cv2.waitKey(1)
    if t == 27:
        break

cv2.destroyAllWindows()
cap


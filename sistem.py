import cv2
from pyzbar.pyzbar import decode
import numpy as np
from datetime import datetime
import openpyxl as xl
import time 


#Creamos la videocaptura
cap = cv2.VideoCapture(0)


#Comprobamos la camara
if not cap:
    print("No se pudo abrir la camara")
    exit()

#Variables de registro  
Entrada = []
Salida = []
Entrada_sb = []
Salida_sb = []
entrada_comida = []
salida_comida = []

#HORARIO 
def infhora():
    inf = datetime.now()
    #Extraemos la fecha
    fecha = inf.strftime('%Y/%m/%d')
    #Extraemos la hora
    hora = inf.strftime('%H:%M:%S')

    return hora, fecha

#Principal function
while True: 
    #leemos los frames
    ret, frame = cap.read()

    #Interfaz
    cv2.putText(frame, 'Presiona ESC para salir', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
    #Ubicamos el rectangulo en las zonas extraidas
    cv2.rectangle(frame, (170, 100), (470, 400), (0, 255, 0), 2)
    

    #Extraemos la hora y fecha 
    hora, fecha = infhora()
    diasem = datetime.today().weekday()

    print(diasem)

    #AÑO #MES #DIA 
    a, me, d = fecha[0:4], fecha[5:7], fecha[8:10]
    #HORA #MINUTOS #SEGUNDOS
    h, m, s = int(hora[0:2]), int(hora[3:5]), int(hora[6:8])
    

    #Creamos el archivo excel
    nomar = str(a) + '-' + str(me) + '-' + str(d)
    texth = str(h) + ':' + str(m) + ':' + str(s)
    print(texth)
    print(nomar)
    wb = xl.Workbook()



    #leemos los codigos QR
    for codes in decode(frame):
        #Extraemos el valor
        info = codes.data.decode('utf-8')


        tipo = info[0:2]
        tipo = int(tipo)
        letr = chr(tipo)

        #Numero 
        num = info[2:]
           

        #Extraemos coordenadas
        pts = np.array([codes.polygon], np.int32)	
        xi, yi = codes.rect.left, codes.rect.top


        #Redireccionamos
        pts = pts.reshape((-1, 1, 2))

        #ID de los codigos QR
        codigo = letr + num

    #SEMANA 
    if 4 >= diasem >= 0:
        
      #ENTRADA DIURNO
    #   if  8 >= h >= 12:

         if tipo == 71:
            #Dibujamos el rectangulo
            cv2.polylines(frame, [pts], True, (255, 255, 0), 5)
            cv2.putText(frame, 'G' + (info[2:]), (xi - 15, yi - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
            print("Regitro de AREA RECURSOS exitosamente \n"
                  "id: G", str(info[2:]))
            
         if tipo == 69:
            #Dibujamos el rectangulo
            cv2.polylines(frame, [pts], True, (255, 255, 0), 5)
            cv2.putText(frame, 'E' + (info[2:]), (xi - 15, yi - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
            print("Registro de Area CONTABILIDAD exitosamente \n"
                  "id: E", str(info[2:]))
            

         if tipo == 83:
            #Dibujamos el rectangulo
            cv2.polylines(frame, [pts], True, (255, 255, 0), 5)
            cv2.putText(frame, 'S' + (info[2:]), (xi - 15, yi - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
            print("Registro de Area SISTEMAS exitosamente \n"
                  "id: S", str(info[2:]))


                  
            #Guardamos el ID 
            if codigo not in Entrada:             

                #Agregamos el ID
                pos = len(Entrada)
                Entrada.append(codigo)

                #Guardamos DB
                hojas = wb.create_sheet("ENTRADAS")
                datos = hojas.append(Entrada) 
                wb.save(nomar + '.xlsx')

                #Dibujamos  
                cv2.polylines(frame,  [pts], True, (255, 255, 0), 5)
                cv2.putText(frame, 'ENTRADA REGISTRADA', (xi - 45, yi - 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(frame, 'CON EXITO' , (xi - 45, yi - 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                #Dibujamos 
                # cv2.putText(frame, '0' + str(num), (xi - 45, yi - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)  

            #Avisamos 
            elif codigo in Entrada:
                cv2.putText(frame, 'EL ID ' + str(codigo),
                            (xi - 45, yi - 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(frame, 'YA FUE REGISTRADO',
                        (xi - 45, yi - 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
            # print(Entrada)


    #Mostramos el frame
    cv2.imshow('LECTOR DE QR', frame)
    t = cv2.waitKey(1)
    if t == 27:
        break

cv2.destroyAllWindows()
cap






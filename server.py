_author_ = "Miguel Andres Herrero, Carlos Congosto Sandoval"
import socket
import serial
import time
import RPi.GPIO as GPIO
import os

arduino = serial.Serial('/dev/ttyUSB0',baudrate=9600, timeout=1.0)#establecemos la conexion con el arduino

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)#se crea el socket

s.bind(("",5555))#abrimos el puerto
txt = "" #valor que lee del arduino
s.listen(1)
print "Inicio de ejecucion del servidor"
sc , addr = s.accept()#aceptamos la conexión con el cliente
print "Conexion establecida"
recibido = ""
while True:
        
        print arduino.read(3)
        txt+=arduino.read(3)
        recibido = sc.recv(1024)#Se lee el dato del cliente
        print "recibido " +recibido
    
        if recibido[0] == "d": 
                #apagar la luz
                print 'dormido'
                arduino.write('1')#se apaga si o si
        if recibido[0] == "l":
                #encender la luz
                print 'leyendo'
                arduino.write('0')#se enciende si o si
        if recibido[0] == "t":
                sc.send(txt) #se envia a la otra raspy el valor leido por el arduino
                print "viendo la tele"
                print recibido[2:] # nos quedamos con el valor numerico
				#como a veces la lectura fallaba y los valores eran en torno a 8XX hacemos el siguiente tratamiento a la lectura
				#el el caso de "x" se realiza la misma operacion
                aux = int(txt)
                if int(txt) < 100:
                        aux+=800
                print "nuevo valor: " + str(aux)
				
                if aux < int(recibido[2:]):#se comparan las lecturas de ambis sistemas
                        #enciendo luz
                        arduino.write('0')
                else:
                        #apago
                        arduino.write('1')
                aux=0
        if recibido[0] == "x": #en este caso se hace lo mismo que en el anterior
                #envio mi info
                sc.send(txt)
                aux = int(txt)
                print "haciendo otra cosa"
                if int(txt) < 100:
                        aux+=800
                print "nuevo valor: " + str(aux)
                if aux > int(recibido[2:]):
                        #enciendo luz
                        arduino.write('0')
                else:
                        #apago
                        arduino.write('1')
                aux=0
        if recibido[:5] == "close": #se solicita el fin de la conexion
                arduino.write('1')#se apaga el LED
                break
        
        txt = ''
print "Cierre del servidor"
sc.close()
s.close()

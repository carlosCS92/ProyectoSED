_author_ = "Miguel Andres Herrero, Carlos Congosto Sandoval"
import socket
import serial
import time
import RPi.GPIO as GPIO
import os

arduino = serial.Serial('/dev/ttyUSB0',baudrate=9600, timeout=1.0)#establecemos la conexion con el arduino
valor = ''

s = socket.socket()#se crea el socket
s.connect(("192.168.0.1", 5555))#conectamos con la otra raspy

while True:
	valor+=arduino.read(3)#leemos el valor del arduino
	mensaje = raw_input("Mensaje a enviar >> ")#accion que se realiza
	enviar = mensaje + " "+valor#generamos el mensaje que se envia al otro sistema
	s.send(enviar)#se envia la informacion al server
	if mensaje == "d":
		print "d"
		#apagar la luz
		arduino.write('1')#se apaga si o si
	elif mensaje == "l":
		print "l"
		#encender la luz
		arduino.write('0')#se enciende si o si
	elif mensaje == "t":
		print "t"
		#recibo info
		recibido = s.recv(1024)
		aux = int(valor)
		if int(valor) < 100:
				aux+=800
		if aux < int(recibido):
			#enciendo luz
			arduino.write('0')
		else:
			#apago
			arduino.write('1')
		aux = 0
	elif recibido == "x":
		#recibo info
		recibido = s.recv(1024)
		aux = int(valor)
		if int(valor) < 100:
				aux+=800
		if aux > int(recibido):
			#enciendo luz
			arduino.write('0')
		else:
			#apago
			arduino.write('1')
		aux = 0
	if mensaje == "close":
		arduino.write('1')#se apaga el LED
		break
	valor = ''#limpiamos el valor
print "adios"
s.close()

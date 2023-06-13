import RPi.GPIO as GPIO
import time

#SOlamente prende el led 5 segundos y se apaga

# Configurar el modo de pines:
GPIO.setmode(GPIO.BOARD)

# Configurar el pin 11 como salida:
GPIO.setup(11, GPIO.OUT)

#Encender el LED:
print("Prende Led")
GPIO.output(11, GPIO.HIGH)

#Espera 5 segundos
time.sleep(5)

#Apagar el Led:
print("Apaga Led")
GPIO.output(11, GPIO.LOW)

#LImpiar los pines GPIO
GPIO.cleanup() #usar esto previene el errror de channel already in use.VAMOS


print('Finalizado')
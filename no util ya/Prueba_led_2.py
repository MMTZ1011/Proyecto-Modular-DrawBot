import RPi.GPIO as GPIO
import time

#AL INICIO BORRA ESTO POR que por su naturaleza de este while nunca podría
GPIO.cleanup() #usar esto previene el errror de channel already in use.VAMOS



#PRende y apaga el led cada segundo hasta que le des a stop al código o borres compilador

# Configurar el modo de pines:
GPIO.setmode(GPIO.BOARD)

# Configurar el pin 11 como salida:
GPIO.setup(11, GPIO.OUT)

while (True):
    #Encender el LED:
    print("Prende Led")
    GPIO.output(11, GPIO.HIGH)

    #Espera 1 segundo
    time.sleep(1)

    #Apagar el Led:
    print("Apaga Led")
    GPIO.output(11, GPIO.LOW)

    #Espera 1 segundo
    time.sleep(1)
####


#LImpiar los pines GPIO
GPIO.cleanup() #usar esto previene el errror de channel already in use.VAMOS


print('Finalizado')
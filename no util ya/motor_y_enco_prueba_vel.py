import RPi.GPIO as GPIO
import time
import numpy as np
from gpiozero import RotaryEncoder 


# ESTABLECE EL Modo de identificación de pines
GPIO.setmode(GPIO.BCM)


################################################################
# Configuración de los pines del puente H L298N:
ENA = 18 #13#13 #PWM
IN1 = 14 #3#19
IN2 = 15 #4#26
# Configuración de los pines del encoder:
Enco_CA = 17
Enco_CB = 27

################################################################
# variables configurables


################################################################
# setup

# Configuración de los pines del puente H L298N como salidas:
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
# Configuración de los pines del ENCODER JGA25-370 como entradas:
#GPIO.setup(Enco_CA, GPIO.IN)
#GPIO.setup(Enco_CB, GPIO.IN)
encoder = RotaryEncoder(Enco_CA, Enco_CB, max_steps=600,wrap=True)


# Inicializamos estados del los motoresa como detenido:
GPIO.output(IN1, GPIO.LOW)
GPIO.output(IN2, GPIO.LOW)



################################################################
# Definimos funciones que utilizaremos

#Funciones motores
def Direccion_motores(direction):
    if direction == 1:
        print("Foward")
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
    elif direction == -1:
        print("backward")
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
    elif direction == 0:
        print("Stop")
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.LOW)
    ####
#### de funcion de direccion de motores

def Velocidad_motores(vel):
    #Velocidad Minima: 6 a 9
    # Velocidad maxima: 100
    p.ChangeDutyCycle(vel) #maximo 100
####

# FUnción para manejar la interrupción del encoder
def print_encoder_estado():
    #Leer el estado actual del pin A y el pin B del encoder:
    estado_A = GPIO.input(Enco_CA)
    estado_B = GPIO.input(Enco_CB)

    # Imprimir el estado actual del encoder:
    print("Encoder A:", estado_A)
    print("Encoder B:", estado_B)
####def encoder callback


# Funcion para posicion del moto


################################################################
# callabacks 

################################################################
#Empieza el código de ejecución:

# Creación de objeto PWM
p = GPIO.PWM(ENA, 100) # El segundo valor es algo de PWM
p.start(0) #VAlor con el que iniciados



#Direccion_motores(1)
#time.sleep(0.5)
#Direccion_motores(-1)
#time.sleep(0.5)
#Direccion_motores(1)
#time.sleep(0.5)
Velocidad_motores(20)
Direccion_motores(-1)


########################

ppr = 11
radio = 0.01


time.sleep(1)


########################

print("steps:",encoder.steps) 
print("pos", encoder.value)

##Termikna
Direccion_motores(0) #detiene los motores


#GPIO.cleanup()
encoder.close()


print("Finalizado")
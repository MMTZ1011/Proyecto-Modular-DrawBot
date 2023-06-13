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
encoder = RotaryEncoder(Enco_CA, Enco_CB, max_steps=0)


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
ppr = 678
tstop = 5.1
tsample = 0.01
tdisp = 0.5

########
anglecurr = 0
tprev = 0
tcurr = 0
tstart = time.perf_counter()



################################################################
# callabacks 

#Detectar direccion:
#GPIO.add_event_detect(Enco_CA, GPIO.RISING, callback=detectar_direccion)



################################################################
#Empieza el código de ejecución:

# Creación de objeto PWM
p = GPIO.PWM(ENA, 25) # El segundo valor es algo de PWM
p.start(0) #VAlor con el que iniciados



#Direccion_motores(1)
#time.sleep(0.5)
#Direccion_motores(-1)
#time.sleep(0.5)
#Direccion_motores(1)
#time.sleep(0.5)



'''
step_dt = 0.1
for i in range(0, int(1/step_dt)):
    #print("Segundo:",i*step_dt)
    #print_encoder_estado()
    time.sleep(0.1)# 5 segundos
####
'''

'''
while tcurr <= tstop:
    time.sleep(tsample)
    stepscurr = encoder.steps
    tcurr = time.perf_counter() -tstart
    anglecurr = 360 / ppr * stepscurr
    print("steps:", stepscurr)
    print("Angle: ", anglecurr)
    ####
    tprev = tcurr
####
'''

Velocidad_motores(20)
Direccion_motores(-1)

deseado = 678 #360 equivalente
t0 = time.perf_counter()
while encoder.steps <= deseado:
    time.sleep(tsample)
    stepscurr = encoder.steps
    tcurr = time.perf_counter() -tstart
    anglecurr = 360 / deseado * stepscurr
    print("steps:", stepscurr)
    print("Angle: ", anglecurr)
    ####
    tprev = tcurr
####
t1 = time.perf_counter()
t_total = t1-t0
frecu = 1/t_total
rpm = frecu*60

Direccion_motores(1) #detiene los motores

print("steps:",encoder.steps) 
print("deseado:", deseado)
print("Tiempo total:", t_total)
print()
print("rpm:", rpm)

time.sleep(0.1)
Direccion_motores(0) #detiene los motores

#GPIO.cleanup()
encoder.close()


print("Finalizado")
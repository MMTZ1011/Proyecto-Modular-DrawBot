import RPi.GPIO as GPIO
import time
import numpy as np
from gpiozero import RotaryEncoder 
from math import pi

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


# NO EDITAR CASI:
ppr = 690 #PUlsos por revolución creo que 690 es el chido
tsample= 0.005 #Tiempo para fors y whiles 

##VAriables:
current_direction = 0
current_velocidad = 0

################################################################
# setup

# Configuración de los pines del puente H L298N como salidas:
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
# Configuración de los pines del ENCODER JGA25-370 como entradas:
encoder = RotaryEncoder(Enco_CA, Enco_CB, max_steps=0)


# Inicializamos estados del los motoresa como detenido:
GPIO.output(IN1, GPIO.LOW)
GPIO.output(IN2, GPIO.LOW)



################################################################
# Definimos funciones que utilizaremos

#Funciones motores (FUNCION VIEJA)
def Direccion_motores(direction):
    global current_direction
    if direction > 0:
        #print("Foward")
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
        current_direction = 1
    elif direction < 0:
        #print("backward")
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)
        current_direction = -1
    elif direction == 0:
        #print("Stop")
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.LOW)
        current_direction = 0
    ####
#### de funcion de direccion de motores


# FUncion vieja de poner velocidad
def Velocidad_motores(vel):
    #Velocidad Minima: 6 a 9
    # Velocidad maxima: 100
    p.ChangeDutyCycle(vel) #maximo 100
    current_velocidad = vel
####

#FUnciones de encoders:
def get_angle():
    stepscurr = encoder.steps
    #print("stepscurr:", stepscurr)
    anglecurr = (360 / ppr * stepscurr) % 360
    return anglecurr
####


## funcion para poner angulo (error de como -10 a -20 angulos)
def set_angle(desired_angle):
    #desired_angle = desired_angle - 20
    Direccion_motores(0)
    time.sleep(0.01)
    current_angle = get_angle()
    #print("theta_0:", current_angle)
    
    if current_angle < desired_angle :
        Direccion_motores(1)
        while (get_angle() < desired_angle  ): #mientras no llegue
            time.sleep(tsample)
        ####
    elif current_angle > desired_angle :
        Direccion_motores(-1)
        while (get_angle() > desired_angle  ): #mientras no llegue
            time.sleep(tsample)
        ####
    ##fin de condiciones para la dirección
    Direccion_motores(0) #lo detiene
    #print("theta_1:", get_angle())
####


# NUEVA FUNCION PARA ASIGNAR
def entrada_velocidad( velocidad):
    global current_direction, current_velocidad

    abs_velocidad = abs(velocidad)

    #satura:
    if abs_velocidad < 6 :
        abs_velocidad = 6
    elif abs_velocidad > 25:
        abs_velocidad = 25
    ####

    if velocidad > 0: # Sentido antihorario
        p.ChangeDutyCycle(abs_velocidad) 
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)

        current_direction = 1
        current_velocidad = abs_velocidad
    elif velocidad < 0: # Sentido Horario
        #print("backward")
        p.ChangeDutyCycle(abs_velocidad) 
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)

        current_direction = -1
        current_velocidad = abs_velocidad
    elif velocidad == 0: # Detener
        p.ChangeDutyCycle(0) 
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.LOW)

        current_direction = 0
        current_velocidad = 0
    ####
####
    
def Detener_motor():
    entrada_velocidad(0) #manda 0 para que se detenga mas facil
####Detener

# para la velocidad
def obtener_step_actual():
    stepscurr = encoder.steps
    return stepscurr
####

# espera y devuelve el tiempo dt para la velocidad
def tiempo_para_vel(tiempo):
    time.sleep(tiempo)
    return tiempo
###

# calcula la velocidad
def calcula_velocidad(delta_time, steps_0, steps_1, tipo):
    delta_steps = steps_1 - steps_0
    speed = delta_steps / delta_time

    grados = (speed / ppr)*360 # grados por segundo

    if tipo == 'rad':
        return (grados*pi)/180 #rad/s
    elif tipo == "deg": 
        return grados #grad/s
    else: ##los steps
        return speed #steps/s
    ####
####



################################################################
#Empieza el código de ejecución: (lo anterior eran funciones y configuracion aca empieza)

# Creación de objeto PWM
p = GPIO.PWM(ENA, 50) # El segundo valor es algo de PWM
p.start(0) #VAlor con el que iniciados
tstart = time.perf_counter() #para las cosas que ocupan tiempo


#Velocidad_motores(10)
#set_angle(360) #establece que queremos este angulo

entrada_velocidad(25)

time.sleep(1) ###Esto para quje siga corriendo con velocidad
steps_0 = obtener_step_actual()
dt = tiempo_para_vel(0.05)
steps_1 = obtener_step_actual()
vel_actual = calcula_velocidad(dt, steps_0, steps_1, 'deg')
print("Velocidad_actual:", vel_actual)
time.sleep(1) ###Esto para quje siga corriendo con velocidad

entrada_velocidad(7)
time.sleep(1)
entrada_velocidad(-7)
time.sleep(1)
entrada_velocidad(-10)
time.sleep(1)
entrada_velocidad(0)
time.sleep(1)
entrada_velocidad(15)

#### Termina
print("steps:", encoder.steps)
print("angulo: ",get_angle())
time.sleep(1) # imrprime 1 segundo despues para que veamos como hay error
Detener_motor()
print("después de 1 segundo:")
print("steps:", encoder.steps)
print("angulo: ",get_angle())




#####
#GPIO.cleanup()
encoder.close()

print("Finalizado")
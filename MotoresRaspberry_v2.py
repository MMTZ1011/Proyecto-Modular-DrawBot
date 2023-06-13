# CODIGO PARA LA RASPBERRY PI 
import RPi.GPIO as GPIO
import time
import math 
#import curses


#importa demás:
import numpy as np
import json
from gpiozero import RotaryEncoder 
from pynput import mouse
from pynput import keyboard
from math import pi


#recordar: math.radians(45), math.degrees(1.57)

#importa variables
from configuracion_Motores import tsample, min_vel_saturacion, max_vel_saturacion, Ppr_Calibra, ENA, IN1, IN2, Enco_CA, Enco_CB, ppr_1, A_vel_calibra, A_ppr_calibra, ENB, IN3, IN4, Enco_CC, Enco_CD, ppr_2, B_vel_calibra, B_ppr_calibra, A_Kp_set_angle, B_Kp_set_angle, tolerancia_error


# ESTABLECE EL Modo de identificación de pines
GPIO.cleanup() #lo limpia desde antes
GPIO.setmode(GPIO.BCM)



# NO EDITA DESDE ESTE PUNTO
archivo_datos = "drawbotDATA.json" #NO EDITAR
Datos_default = { #NO EDITAR SOLO CASO DONDE NO HAY datos guardados antes
    "angle_motor_A": 0.0,#
    "angle_motor_B": 0.0, 
}
mis_datos = Datos_default #esto se sobreescribirá después
def Cargar_datos():
    global mis_datos
    #carga el json:
    with open(archivo_datos, "r") as f:
        mis_datos = json.load(f)
    ####
    print("Cargado:",mis_datos)
####CArgar datos robot


def Guardar_datos():
    #Guarda los datos nuevos:
    mis_datos = { 
    "angle_motor_A": Motor_A.current_angle ,
    "angle_motor_B": Motor_B.current_angle , 
}
    #guarda el json:
    with open(archivo_datos, 'w') as f:
        json.dump(mis_datos, f)
    ####
    print("Guardado:",mis_datos)
####



###########################
#Definimos clase de motor (esta estructura se clona cada vez que lo inicialicemos):
class Eslabon:
    #Cuando se llama esta función de Eslabon __init__() es lo primero en ejecutarse:
    def __init__(self, ENA, IN1, IN2, Enco_CA, Enco_CB, ppr, ang_inicial, Kp_set_angle ):

        print()
        # Configuración de los pines del puente H L298N:
        self.pinENA = ENA
        self.pinIN1 = IN1
        self.pinIN2 = IN2
        self.ppr = ppr
        self.Kp = Kp_set_angle #para posicionar en pos inicial con set_angle_new

        # Configuración de los pines del encoder:
        self.Enco_CA = Enco_CA
        self.Enco_CB = Enco_CB

        #Propiedades o variables:
        self.angulo_inicial =  ang_inicial#el angulo cargado del json
        self.current_angle = ang_inicial #este lo carga del json
        self.current_direction = 0
        self.current_velocidad = 0

        # setup
        # Configuración de los pines del puente H L298N como salidas:
        GPIO.setup(ENA, GPIO.OUT)
        GPIO.setup(IN1, GPIO.OUT)
        GPIO.setup(IN2, GPIO.OUT)

        # Configuración de los pines del ENCODER JGA25-370 como entradas:
        self.encoder = RotaryEncoder(Enco_CA, Enco_CB, max_steps=0, wrap=True)

        # Inicializamos estados del motor para que esté:
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.LOW)

        # Creación de objeto PWM
        self.p = GPIO.PWM(ENA, 50) # El segundo valor es algo de PWM
        self.p.start(0) #VAlor con el que iniciados

    #### fin del def innit



    def get_angle(self):
        stepscurr = self.encoder.steps
        anglecurr = (self.angulo_inicial +((360 / self.ppr)*stepscurr)) % 360 #grados
        self.current_angle = anglecurr #GUARDA A DIFERENCIA DE RAD
        return anglecurr
    #### get angle


    def get_angle_rad(self):
        stepscurr = self.encoder.steps
        anglecurr = (self.angulo_inicial +((360 / self.ppr)*stepscurr)) % 360 #grados
        self.current_angle = anglecurr #GUARDA A DIFERENCIA DE RAD

        angle_rad = math.radians(anglecurr) #radianes
        return angle_rad
    #### get angle


    # Funcion para posicionar en un angulo en degrados/grados (NO LLAMAR )
    def set_angle(self, desired_angle):
        #desired_angle = desired_angle - 20
        self.entrada_velocidad(0)
        time.sleep(0.01)
        current_angle = self.get_angle()
        #print("theta_0:", current_angle)
        
        if current_angle < desired_angle :
            self.entrada_velocidad(8)
            while (self.get_angle() < desired_angle  ): #mientras no llegue
                time.sleep(tsample)
            #### while
        elif current_angle > desired_angle :
            self.entrada_velocidad(-8)
            while (self.get_angle() > desired_angle  ): #mientras no llegue
                time.sleep(tsample)
            #### while
        ##fin de condiciones para la dirección

        self.entrada_velocidad(0) #lo detiene
    #### set angle

    def set_angle_new(self, desired_angle): #esta en grados (deg)

        ciclo = True
        while ciclo==True:
            #obtenemos valor controlador:
            Kp = self.Kp

            #obtenemos el angulo actual y calculamos el error
            angle_actual = self.get_angle()
            error_angulo = angle_actual - desired_angle

            
            if error_angulo < tolerancia_error: #tolerancia error es un grado deg que definimos en configuracionMotores
                ciclo = False
                self.entrada_velocidad(0) #detiene motor
                wait(0.5)#se espera un poquito si según eso no hay error y hara el ciclo una vez más para comprobar el error.

                #hace de nuevo lo de obtener todo para comprobar una vez más tras los 0.5 segundos:
                angle_actual = self.get_angle()
                error_angulo = angle_actual - desired_angle
                if error_angulo > tolerancia_error: #si no es cierto que esta dentro de la tolerancia entonces
                    ciclo = True #se vuelve true para que siga repitiendo
                ###

            else: #si no esta dentro de la tolerancia entonces sigue controlando
                #ahora creamos el controlador
                vel_controlador = -(Kp*error_angulo)

                #enviamos velocidad:
                self.entrada_velocidad(vel_controlador)
            #### if del error
            
        ##while de ciclo
    ####set angle_new


    def entrada_velocidad(self, velocidad):

        abs_velocidad = abs(velocidad)

        #satura:
        if abs_velocidad < min_vel_saturacion :
            abs_velocidad = min_vel_saturacion
        elif abs_velocidad > max_vel_saturacion:
            abs_velocidad = max_vel_saturacion
        ####

        if velocidad > 0: # Sentido antihorario (hacia delante)
            self.p.ChangeDutyCycle(abs_velocidad) 
            GPIO.output(self.pinIN1, GPIO.LOW)
            GPIO.output(self.pinIN2, GPIO.HIGH)

            self.current_direction = 1
            self.current_velocidad = abs_velocidad
        elif velocidad < 0: # Sentido Horario (hacia atras)
            self.p.ChangeDutyCycle(abs_velocidad) 
            GPIO.output(self.pinIN1, GPIO.HIGH)
            GPIO.output(self.pinIN2, GPIO.LOW)

            self.current_direction = -1
            self.current_velocidad = abs_velocidad
        elif velocidad == 0: # Detener
            self.p.ChangeDutyCycle(0) 
            GPIO.output(self.pinIN1, GPIO.LOW)
            GPIO.output(self.pinIN2, GPIO.LOW)

            self.current_direction = 0
            self.current_velocidad = 0

            self.get_angle()
        ####
    #### de entrada de velocidad



    def Detener_motor(self):
        self.entrada_velocidad(0) #manda 0 para que se detenga mas facil
    ####Detener



    # UTIL para calculo de su velocidad angular:
    def obtener_step_actual(self):
        stepscurr = self.encoder.steps
        return stepscurr
    ####
####fin de la clase de eslabon robotico





# espera y devuelve el tiempo dt para la velocidad
def tiempo_para_vel(tiempo):
    time.sleep(tiempo)
    return tiempo
###tiempo para velocidad 



# calcula la velocidad
def calcula_velocidad(delta_time, steps_0, steps_1, ppr_motor, tipo):

    delta_speed = steps_1 - steps_0

    speed = delta_speed / delta_time

    grados = (speed / ppr_motor)*360 

    if tipo == 'rad':
        rads = (grados*pi)/180 #rad/s
        return rads
    elif tipo == "deg": 
        return grados #grad/s
    else: ##los steps
        return speed #steps/s
    ####
####


#Funcion que les establece velocidad a ambos motores
def u_vel(vel_A, vel_B):
    global Motor_A, Motor_B

    # conversion de rad/m a entradas validas para el motor 6 a 25 pwm
    conv_A = vel_A #aun pendiente
    conv_B = vel_B #aun pendiente

    Motor_A.entrada_velocidad(conv_A)
    Motor_B.entrada_velocidad(conv_B)
    return 
####


#Funcion que obtiene el step actual de ambos motores
def get_current_steps():
    global Motor_A, Motor_B

    step_A = Motor_A.obtener_step_actual()
    step_B = Motor_B.obtener_step_actual()

    return [step_A, step_B]
####


#Funcion que obtiene las velocidades de ambos motores
def get_current_vel(delta_time, steps_0, steps_1, tipo):
    global Motor_A, Motor_B
    vel_A = calcula_velocidad(delta_time, steps_0[0], steps_1[0], Motor_A.ppr, tipo)
    vel_B = calcula_velocidad(delta_time, steps_0[1], steps_1[1], Motor_B.ppr, tipo)
    return [vel_A, vel_B]
####

#Funcion que detiene a ambos motores
def motores_detener():
    global Motor_A, Motor_B

    Motor_A.Detener_motor()
    Motor_B.Detener_motor() 
####


#Funcion obtiene los angulos en grados de los dos motores:
def get_angles_deg():
    global Motor_A, Motor_B
    
    deg_A = Motor_A.get_angle()
    deg_B = Motor_B.get_angle()
    return [deg_A, deg_B]
####

#Funcion obtiene los angulos en radianes de ambos motores: (Puede ser para actualizar la posición)
def get_angles_rad():
    global Motor_A, Motor_B
    
    rad_A = Motor_A.get_angle_rad()
    rad_B = Motor_B.get_angle_rad()
    return [rad_A, rad_B]
####

def actualizar_current_motores(t ):
    global Motor_A, Motor_B

    wait(t)
    Motor_A.get_angle()
    Motor_B.get_angle()
#####


#para poner los angulos en radianes como pos inicial angulos en radianes
def Set_Angulos_iniciales_rad(rad_1, rad_2):
    global Motor_A, Motor_B

    grados_1 = math.degrees(rad_1)
    grados_2 = math.degrees(rad_2)

    Motor_A.set_angle_new(grados_1)
    Motor_B.set_angle_new(grados_2)

###Poner_angulos_iniciales


#para poner los angulos en radianes como pos inicial angulos en deg
def Set_Angulos_iniciales_deg(grados_1, grados_2):
    global Motor_A, Motor_B

    Motor_A.set_angle_new(grados_1)
    Motor_B.set_angle_new(grados_2)

###Poner_angulos_iniciales




#Funcion que detiene a ambos motores
def encoder_close():
    global Motor_A, Motor_B

    Motor_A.encoder.close()
    Motor_B.encoder.close()
####


#para no escribir time.sleep():
def wait(t):
    time.sleep(t)
####

def obtener_vel_test(t ):
    steps_0 = get_current_steps()
    dt = tiempo_para_vel(t)
    steps_1 = get_current_steps()
    vel_actual = get_current_vel(dt, steps_0, steps_1, 'deg')
    print("Velocidades_actuales:", vel_actual)
#### obtener velocidad rapida




###############################
###############################
###############################



def Main_calibracion():
    ##FUNCIONES CALIBRACION

    global motor_calibrando

    motor_calibrando = "A"

    #### funciones:
    def on_scroll(x, y, dx, dy):
        global motor_calibrando
        if dy <0 : #down
            if motor_calibrando == "A":
                Motor_A.entrada_velocidad(-A_vel_calibra)
            else:
                Motor_B.entrada_velocidad(-B_vel_calibra)
            ####
            wait(0.05)
            if motor_calibrando == "A":
                Motor_A.entrada_velocidad(0)
            else:
                Motor_B.entrada_velocidad(0)
            ####
        elif dy >0: #up
            if motor_calibrando == "A":
                Motor_A.entrada_velocidad(A_vel_calibra)
            else:
                Motor_B.entrada_velocidad(B_vel_calibra)
            ####
            wait(0.05)
            if motor_calibrando == "A":
                Motor_A.entrada_velocidad(0)
            else:
                Motor_B.entrada_velocidad(0)
            ####
        ####
    ####funcion on scroll

    def on_click(x, y, button, pressed):
        global motor_calibrando
        if button == mouse.Button.left and pressed:
            if motor_calibrando == "A":
                print("se cambio a motor B")
                motor_calibrando = "B"
            elif motor_calibrando == "B":
                print("se cambio a motor A")
                motor_calibrando = "A"
            ####
        ####
    ####
    def on_presskey(key):
        if (key == keyboard.Key.enter or key == keyboard.Key.esc) :
            mouse_listener.stop()
        ####
    #####
    def on_relasekey(key):
        if key == keyboard.Key.enter:
            pass
        ####
    #####

    ##EJECUCION:

    print("MODO DESARROLLADOR DE DRAWBOT")
    print("MODO SET DE ANGULOS")
    print("1) Presiona 'Enter' para continuar con configuracion")

    #Listeners especificos para calibracion:
    mouse_listener = mouse.Listener(on_scroll = on_scroll, on_click=on_click)
    keyboard_listener = keyboard.Listener(on_press=on_presskey, on_relasekey=on_relasekey )
    
    #inicia listener
    mouse_listener.start()
    keyboard_listener.start()

    #pausa:
    mouse_listener.join() #Hasta que la función de keyboard detecte el enter

    # aca continua después de la pausa:

    # pide que escriba cosas de los motores que calibro.
    while True:
        try:
            grados_motor_1 = float(input("¿En cuantos grados(deg) quedó el motor 1?: "))
            grados_motor_2 = float(input("¿En cuantos grados(deg) quedó el motor 2?: "))
            break#termina while de que no hubo error
        except ValueError:
            print("Ingresa valores validos porfa")
        ####
    ####
    
    #lo guarda dentro de cada uno
    Motor_A.current_angle = grados_motor_1
    Motor_B.current_angle = grados_motor_2

    #Manda a guardar:
    Guardar_datos()
#### Main_calibracion




def Main_ppr():
##FUNCIONES PPR

    global motor_calibrando

    motor_calibrando = "A"

    #### funciones:
    def on_scroll(x, y, dx, dy):
        global motor_calibrando
        if dy <0 : #down
            if motor_calibrando == "A":
                Motor_A.entrada_velocidad(-A_ppr_calibra)
            else:
                Motor_B.entrada_velocidad(-B_ppr_calibra)
            ####
            wait(0.05)
            if motor_calibrando == "A":
                Motor_A.entrada_velocidad(0)
            else:
                Motor_B.entrada_velocidad(0)
            ####
        elif dy >0: #up
            if motor_calibrando == "A":
                Motor_A.entrada_velocidad(A_ppr_calibra)
            else:
                Motor_B.entrada_velocidad(B_vel_calibra)
            ####
            wait(0.05)
            if motor_calibrando == "A":
                Motor_A.entrada_velocidad(0)
            else:
                Motor_B.entrada_velocidad(0)
            ####
        ####

        #Ahora imprime los steps:
        if motor_calibrando == "A":
            stepscurr = Motor_A.encoder.steps
            print("motor A steps:", stepscurr)
        elif motor_calibrando == "B":
            stepscurr = Motor_B.encoder.steps
            print("motor B steps:", stepscurr)
        #####
    ####funcion on scroll

    def on_click(x, y, button, pressed):
        global motor_calibrando
        
        if button == mouse.Button.left and pressed:
            if motor_calibrando == "A":
                print("se cambio a motor B")
                motor_calibrando = "B"
            elif motor_calibrando == "B":
                print("se cambio a motor A")
                motor_calibrando = "A" 
            ####
        elif button == mouse.Button.right and pressed:
            if motor_calibrando == "A":
                stepscurr = Motor_A.encoder.steps
                print("motor A steps:", stepscurr)
            elif motor_calibrando == "B":
                stepscurr = Motor_B.encoder.steps
                print("motor B steps:", stepscurr)
            #####
        ####
    ####
    def on_presskey(key):
        if (key == keyboard.Key.enter or key == keyboard.Key.esc) :
            mouse_listener.stop()
        ####
    #####
    def on_relasekey(key):
        if key == keyboard.Key.enter:
            pass
        ####
    #####

    ##EJECUCION:

    print("MODO DESARROLLADOR DE DRAWBOT")
    print("MODO PPR")
    print("1) Presiona 'Enter' para salir con configuracion")

    #Listeners especificos para calibracion:
    mouse_listener = mouse.Listener(on_scroll = on_scroll, on_click=on_click)
    keyboard_listener = keyboard.Listener(on_press=on_presskey, on_relasekey=on_relasekey )
    
    #inicia listener
    mouse_listener.start()
    keyboard_listener.start()

    #pausa:
    mouse_listener.join() #Hasta que la función de keyboard detecte el enter

    #NO GUARDA DATOS
#### def Main_ppr():

def Main_ProbarMotores():
    ##EJECUCION:

    print("MODO DESARROLLADOR DE DRAWBOT")
    print("MODO Probar motores")
    print("¡Esta prueba solo sirve para ver que este conectado todo bien!")
    print("probando motores en: ")
    segundos = 3
    for i in range(segundos, 0, -1):
        print(i)
        wait(i)
    ####
    print("vel(7, 7) 0.1 segundos")
    u_vel(7, 7)
    obtener_vel_test(0.5)
    u_vel(0, 0)
    wait(0.5)

    print("vel(-10, -10) 0.1 segundos")
    u_vel(-10, -10)
    obtener_vel_test(0.5)
    u_vel(0, 0)
    wait(0.5)

    print("vel(25, 25) 0.1 segundos")
    u_vel(25, 25)
    obtener_vel_test(0.5)
    u_vel(0, 0)
    wait(0.5)


    # actualiza motores
    actualizar_current_motores(1)

    #Manda a guardar:
    Guardar_datos()
    print("¡Termino la prueba, recomendado que se vuelva a calibrar el angulo!")
####




def Main_Set_Grados():
    ##EJECUCION:

    print("MODO DESARROLLADOR DE DRAWBOT")
    print("MODO Poner angulos iniciales")
    print("Esta prueba sirve para garantizar que puede posicionarse en angulos")
    
    while True:
        try:
            grados_motor_1 = float(input("¿En cuantos grados(deg) se debe posicionar el motor 1?: "))
            grados_motor_2 = float(input("¿En cuantos grados(deg) se debe posicionar el motor 1?: "))
            break#termina while de que no hubo error
        except ValueError:
            print("Ingresa valores validos porfa")
        ####
    ####

    Set_Angulos_iniciales_deg(grados_motor_1, grados_motor_2)

    wait(0.5)
    print("Ya terminó de colocar ambos motores quedarón en:")
    print("Motor 1 quedó en ", Motor_A.get_angle(), " grados (deg)")
    print("Motor 2 quedó en ", Motor_B.get_angle(), " grados (deg)")

####Main_set_grados():


def MainLibre():
    ##FUNCIONES LIBRE

    global motor_calibrando

    motor_calibrando = "A"

    #### funciones:
    def on_scroll(x, y, dx, dy):
        global motor_calibrando
        if dy <0 : #down
            if motor_calibrando == "A":
                Motor_A.entrada_velocidad(-A_vel_calibra)
            else:
                Motor_B.entrada_velocidad(-B_vel_calibra)
            ####
            wait(0.05)
            if motor_calibrando == "A":
                Motor_A.entrada_velocidad(0)
            else:
                Motor_B.entrada_velocidad(0)
            ####
        elif dy >0: #up
            if motor_calibrando == "A":
                Motor_A.entrada_velocidad(A_vel_calibra)
            else:
                Motor_B.entrada_velocidad(B_vel_calibra)
            ####
            wait(0.05)
            if motor_calibrando == "A":
                Motor_A.entrada_velocidad(0)
            else:
                Motor_B.entrada_velocidad(0)
            ####
        ####
        if motor_calibrando == "A":
            curr_ang = Motor_A.get_angle()
            print("Ang(deg) motor A:",curr_ang)
        elif motor_calibrando == "B":
            curr_ang = Motor_B.get_angle()
            print("Ang(deg) motor B:",curr_ang)
        ####
    

    ####funcion on scroll

    def on_click(x, y, button, pressed):
        global motor_calibrando
        if button == mouse.Button.left and pressed:
            if motor_calibrando == "A":
                print("se cambio a motor B")
                motor_calibrando = "B"
            elif motor_calibrando == "B":
                print("se cambio a motor A")
                motor_calibrando = "A"
            ####
        ####
    ####
    def on_presskey(key):
        if (key == keyboard.Key.enter or key == keyboard.Key.esc) :
            mouse_listener.stop()
        ####
    #####
    def on_relasekey(key):
        if key == keyboard.Key.enter:
            pass
        ####
    #####

    ##EJECUCION:

    print("MODO DESARROLLADOR DE DRAWBOT")
    print("MODO Libre")
    print("1) Presiona 'Enter' o 'Esc' para terminar ")

    #Listeners especificos para calibracion:
    mouse_listener = mouse.Listener(on_scroll = on_scroll, on_click=on_click)
    keyboard_listener = keyboard.Listener(on_press=on_presskey, on_relasekey=on_relasekey )
    
    #inicia listener
    mouse_listener.start()
    keyboard_listener.start()

    #pausa:
    mouse_listener.join() #Hasta que la función de keyboard detecte el enter

    # aca continua después de la pausa:

    #Manda a guardar:
    Guardar_datos()
#### MAin_libre







################################################################
################################################################
#Empieza el código de ejecución: (lo anterior eran funciones y configuracion aca empieza)

# CArgamos datos: (último angulo de cada eslabónn)
Cargar_datos()
ang_ini_A = mis_datos['angle_motor_A']
ang_ini_B = mis_datos['angle_motor_B']


#Configuramos motores y sus pines:
Motor_A = Eslabon(ENA, IN1, IN2, Enco_CA, Enco_CB, ppr_1, ang_ini_A, A_Kp_set_angle) #Primer Motor:
Motor_B = Eslabon(ENB, IN3, IN4, Enco_CC, Enco_CD, ppr_2, ang_ini_B, B_Kp_set_angle) #Segundo Motor:

#Empieza a contar el tiempo.
tstart = time.perf_counter() 


#main()



def cerrar_encoder():
    encoder_close()
####






###################################
####### Termina
''''
print("-------")
print("steps:", get_current_steps() )
print("angulo grados: ", get_angles_deg())
time.sleep(1) # imrprime 1 segundo despues para que veamos como hay error
motores_detener()
print("-------")
print("después de 1 segundo:")
print("steps:", get_current_steps() )
print("angulo grados: ",get_angles_deg())

print("Posición en angulos del robot:", get_angles_rad()) #util para actualizar el valor de q del robot de la posición angular
'''

#####
#GPIO.cleanup()
#encoder_close()

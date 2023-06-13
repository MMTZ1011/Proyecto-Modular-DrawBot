import RPi.GPIO as GPIO
import numpy as np
import time
 
#Este permite poner en posiciones.

# ES MUY IMPORTANTE NOTAR QUE EL MODO DE LA SETMODE ES BCM Para conectar todo segun el tipo BCM y no Board


#COnfigurables:
#Definimos los ángulos a los que queremos llevar el motor y lo guardamos en una lista

#1) calibrar
angles = [0]

#2) de 0 a 90
angles = [0, 90]

#3) de 0, 90, 180, 270, 360
angles = [0, 90, 180, 270, 360]

#4) de 0, 90, 
angles = [0, 90, 45, 90, 0]

#5) ENtrada senoidal.
t = np.linspace(0, 2*np.pi, 20)
x_rad = np.degrees(np.sin(t))
#angles = x_rad


#Define el angulo inicial del motor (0 grados de preferencia)
current_angle = 0 #aca se cambia si se requiere


## Desde esta parte no moverle de ser posible
in1 = 17 #BCM
in2 = 18 #BCM
in3 = 27 #BCM
in4 = 22 #BCM
motor_pins = [in1,in2,in3,in4] #NO SE MODIFICA


# Se define la secuencia de fases para el motor (ESTO PARA NADA SE MODIFICA cambia segun el tipo de motor)
step_sequence = [[1,0,0,1],
                 [1,0,0,0],
                 [1,1,0,0],
                 [0,1,0,0],
                 [0,1,1,0],
                 [0,0,1,0],
                 [0,0,1,1],
                 [0,0,0,1]]

# Se establecen los pines de salida de la Raspberry
GPIO.setmode( GPIO.BCM ) 
GPIO.setup( in1, GPIO.OUT )
GPIO.setup( in2, GPIO.OUT )
GPIO.setup( in3, GPIO.OUT )
GPIO.setup( in4, GPIO.OUT )
# Se inicializan los estados de los pines (NINGUNO que este prendido al iniciarse)
GPIO.output( in1, GPIO.LOW ) 
GPIO.output( in2, GPIO.LOW )
GPIO.output( in3, GPIO.LOW )
GPIO.output( in4, GPIO.LOW )





#Funciones definidas:

def rotate_to_angle(angle):
    
    global current_angle #Definimos que vamos a extrar la variable global fuera de la funcion sino pensara que es local
    print("Angulo_Actual:", current_angle)
    print("Angulo deseado:", angle)

    #Calcula la cantidad de pasos necesarios para llegar al ángulo deseado
    steps = abs(int(((angle-current_angle)/5.625)*64))

    
    #Determina la dirección del movimiento (horario o antihorario)
    if angle > current_angle:
        direction = 1
    else:
        direction = -1
    ##fin de condiciones para la dirección
    print("Direccion:", direction)
    

    #Inicializa en 0
    sequence_index = 0

    # Gira el motor hasta llegar al ángulo deseado:
    for i in range(steps):
        #CAlcula el índice de la secuencia de pasos según la dirección de movimiento
        if direction == 1:
            #sequence_index = 1 % 8
            sequence_index = (sequence_index - 1) % 8
        else: #sentido inverso o antihorario
            #sequence_index = (7 - i) % 8
            sequence_index = (sequence_index + 1) % 8
        ####
        
        # Activa cada uno de los pines del motor según la secuencia de pasos:
        for pin in range(0, len(motor_pins)):
            GPIO.output( motor_pins[pin], step_sequence[sequence_index][pin] )
        #### fin recorrer cada motor y poner output

        time.sleep(0.001) #Espera un breve instante antes de avanzar al siguiente paso (VELOCIDAD)
    ### fin for de recorrer los pasos requeridos para posicionarse ahí.


    # Actualiza el ángulo actual del motor con el angulo en el que acabó.
    current_angle = angle
    print("--------------")
## fin funcion

for angle in angles:
    rotate_to_angle(angle)
    time.sleep(1)
####



#LImpiar los pines GPIO ya que no los necesite
GPIO.cleanup() #usar esto previene el errror de channel already in use.VAMOS

print("Finalizado")
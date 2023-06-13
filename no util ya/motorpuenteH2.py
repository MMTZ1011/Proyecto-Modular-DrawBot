import RPi.GPIO as GPIO
import time


# Configuración de los pines del puente H L298N
ENA = 18#13#13 #PWM
IN1 = 14#3#19
IN2 = 15#4#26

# Configuración de los pines del puente H L298N como salidas

# Configuración de los pines de la Raspberry Pi
GPIO.setmode(GPIO.BCM)

GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)



# Configuración de los pines del puente H L298N como salidas
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)


# Lo inicializa detenido
GPIO.output(IN1, GPIO.LOW)
GPIO.output(IN2, GPIO.LOW)



# Creación de objeto PWM
p = GPIO.PWM(ENA, 50)

p.start(25)

# establece:
direction = -1 #direccion

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

p.ChangeDutyCycle(50) #maximo 100

time.sleep(5)# 5 segundos
GPIO.output(IN1, GPIO.LOW)
GPIO.output(IN2, GPIO.LOW)


GPIO.cleanup()
print("Finalizado")
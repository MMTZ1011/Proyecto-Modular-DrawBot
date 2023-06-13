import RPi.GPIO as GPIO
from machine import ADC
import time

# Configurar los pines del potenciómetro
pot_pin = 290
GPIO.setmode(GPIO.BCM)
GPIO.setup(pot_pin, GPIO.IN)

# Función para leer el valor del potenciómetro
def read_pot():
    pot_value = GPIO.input(pot_pin)
    return pot_value
####

# Loop principal
while True:
    pot_val = read_pot()
    print(pot_val)
    print("Valor del potenciómetro: {}".format(pot_val))
    time.sleep(0.1) # Esperar un poco antes de leer de nuevo
####



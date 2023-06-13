import time
import pygame
import pygame.camera
from pygame.locals import *
import matplotlib.pyplot as plt
from PIL import Image
import cv2

nomb = "tempfoto.jpg"

resolucion = (640, 480)

pygame.init()
pygame.camera.init()

# Configura la cámara
cam = pygame.camera.Camera("/dev/video0", resolucion)
cam.start()

# Configura la ventana
pygame.display.set_caption("Vision del DrawBot-2D (presiona 'ESC' para salir)")
screen = pygame.display.set_mode(resolucion)

# Bucle principal
while True:
    # Obtiene la imagen de la cámara y la convierte a un objeto de superficie de Pygame
    imagen = cam.get_image()
    imagen = pygame.transform.rotate(imagen, 180) # Rota la imagen para que se vea en posición horizontal
    imagen = pygame.transform.flip(imagen, False, False) # Voltea la imagen horizontalmente

    # Dibuja la imagen en la ventana
    screen.blit(imagen, (0, 0))
    pygame.display.update()

    # Comprueba si se ha pulsado la tecla ESC para salir
    for event in pygame.event.get():
        if event.type == KEYDOWN and event.key == K_ESCAPE: # si es tecla abajo y tecla esc
            
            #CRea una imagen pil apartir de la de la camara

            #imagen = pygame.transform.rotate(imagen, 0) # Rota la imagen para que se vea en posición horizontal
            #imagen = pygame.transform.flip(imagen, False, True) # Voltea la imagen horizontalmente
            pil_img = Image.frombytes("RGB", imagen.get_size(), pygame.image.tostring(imagen, "RGB"))

            #guarda en el disco duro:
            pil_img.save(nomb)



            # Detiene todo lo de la camara
            cam.stop() #camara
            pygame.quit() #dejamos de usar esta cosa


            #PRocesa la imagen:
            frame = cv2.imread(nomb )
            frame = cv2.flip(frame, 0) #Voltea eje y
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            plt.imshow(frame, origin='lower', cmap='viridis' )
            plt.title("1.1) Frame Original")
            plt.show()


            quit()
        ###
    #####
    time.sleep(0.035)
####



print("Finalizado")

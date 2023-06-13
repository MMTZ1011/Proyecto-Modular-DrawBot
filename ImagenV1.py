import cv2 #Biblioteca open cv
import numpy as np
import matplotlib.pyplot as plt
from skimage.morphology import skeletonize
from skimage import io, img_as_ubyte



def Cargar_Imagen(P_plotear, ruta_img):
    frame = cv2.imread(ruta_img) #Carga la imagen por la ruta o nombre
    if P_plotear:
        plt.xlabel("Ancho (Pixeles)"); plt.ylabel("Alto (Pixeles)")
        imshow(P_plotear, frame, '1.1) Frame Original', 'upper', 'rgb')
    ####
    


    frame_i = np.flipud(frame) #Invierte el eje Y de la imagen
    if P_plotear:
        plt.xlabel("Ancho (Pixeles)"); plt.ylabel("Alto (Pixeles)")
        imshow(P_plotear, frame_i, '1.2) Frame invertido', 'lower', 'rgb')
    ####

    return frame_i


def Get_Seleccion(P_plotear, frame_i, lower_select, upper_select): #hace el open, close, erode y obtiene seleccion

    hsv = cv2.cvtColor(frame_i, cv2.COLOR_BGR2HSV)
    if P_plotear:
        plt.xlabel("Ancho (Pixeles)"); plt.ylabel("Alto (Pixeles)")
        imshow(P_plotear, hsv, '2.1) Conversion HSV', 'lower', 'hsv')
    ####

    #ww Crea una máscara que detecte los valores de color de la pelota verde en el espacio de color HSV
    mask = cv2.inRange(hsv, lower_select, upper_select)
    if P_plotear:
        plt.xlabel("Ancho (Pixeles)"); plt.ylabel("Alto (Pixeles)")
        imshow(P_plotear, mask, '2.2) Mask', 'lower', 'gray')
    ####


    # Aplica una serie de operaciones morfológicas para eliminar el ruido y mejorar la forma de la pelota
    #kernel = np.ones((5,5),np.uint8) ##Original
    kernel = np.ones((2,2),np.uint8) # 2,2 es perfecto
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    if P_plotear:
        plt.xlabel("Ancho (Pixeles)"); plt.ylabel("Alto (Pixeles)")
        imshow(P_plotear, opening, '2.3) Opening', 'lower', 'gray')
    ####

    # hace fill
    kernel = np.ones((0,0),np.uint8) # 0,0 es perfecto por que sino genera problemas skeleton
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

    #extra de erosion
    #kernel = np.ones((2,2),np.uint8)
    #closing = cv2.erode(closing,kernel,iterations = 1)
    #fin extra

    if P_plotear:
        plt.xlabel("Ancho (Pixeles)"); plt.ylabel("Alto (Pixeles)")
        imshow(P_plotear, closing, '2.4) Closing o Fill', 'lower', 'gray')
    #####

    

    # toma la mascara PARA IMPRIMIR
    seleccion_rgb = cv2.bitwise_and(frame_i, frame_i, mask=closing) # Aplicar la máscara para extraer el color verde
    if P_plotear:
        plt.xlabel("Ancho (Pixeles)"); plt.ylabel("Alto (Pixeles)")
        imshow(P_plotear, seleccion_rgb, '2.5) Seleccion', 'lower', 'gray')
    ####

    return closing, seleccion_rgb

def Get_Skeletization(P_plotear, seleccion):
    #IMPORTANTE: APARENTEMENTE con el method='lee' no requiero hacer spur, falta comprobar con ejemplos 
    # posiblemente deba aplicarles una erosion por que podria producir grosor en pixeles
    #investigar el seam en metodo zhang si no resulta este método

    # Realiza esqueletización de la imagen binaria (blanco y negro)
    #skel_lines = skeletonize(seleccion, method='lee') original
    skel_lines = skeletonize(seleccion, method='lee')

    # convertir imagen esqueletizada a uint8
    skel_uint8 = img_as_ubyte(skel_lines)

    #Vamos a quitar donde hay branches
    #kernel = np.ones((1,1),np.uint8)
    #skel_uint8 = cv2.erode(skel_uint8,kernel,iterations = 2)
    #fin adicional

    if P_plotear:
        plt.xlabel("Ancho (Pixeles)"); plt.ylabel("Alto (Pixeles)")
        imshow(P_plotear, skel_uint8, '2.6) Esqueletizacion', 'lower', 'gray')
    ####

    


    return skel_uint8


def Get_Propiedades(img):
    # Obtiene propiedades
    img_width = np.size(img, 1)
    img_height = np.size(img, 0)
    return img_width, img_height


#Los endpoints es donde termina
def Get_EndPoints(skel_uint8):
    # https://stackoverflow.com/questions/72323491/find-end-point-on-each-line-using-opencv
    # kernels to find endpoints in all 4 directions
    #https://docs.opencv.org/4.x/db/d06/tutorial_hitOrMiss.html
    #La flecha señala de donde a donde
    k1 = np.array(([-1,  1, -1], 
                   [-1,  1, -1], 
                   [-1, -1, -1]), dtype="int") # ABAJO ↓
    
    k2 = np.array(([-1, -1, -1], 
                   [ 1,  1, -1], 
                   [-1, -1, -1]), dtype="int") # DERECHA →
    
    k3 = np.array(([-1, -1, -1], 
                   [-1,  1,  1], 
                   [-1, -1, -1]), dtype="int") # IZQUIERDA ←
    
    k4 = np.array(([-1, -1, -1], 
                   [-1,  1, -1], 
                   [-1,  1, -1]), dtype="int") # ARRIBA ↓
    
    k5 = np.array(([ 1, -1, -1], 
                   [-1,  1, -1], 
                   [-1, -1, -1]), dtype="int") # ↘
    
    k6 = np.array(([-1, -1,  1], 
                   [-1,  1, -1], 
                   [-1, -1, -1]), dtype="int") # ↙
    
    k7 = np.array(([-1, -1, -1], 
                   [-1,  1, -1], 
                   [-1, -1,  1]), dtype="int") # ↖

    k8 = np.array(([-1, -1, -1], 
                   [-1,  1, -1], 
                   [ 1, -1, -1]), dtype="int") # ↗

    #Probablemente haga falta añadir mas kernels para las 4 posibles diagonales


    # perform hit-miss transform for every kernel
    o1 = cv2.morphologyEx(skel_uint8, cv2.MORPH_HITMISS, k4) #ABAJO
    o2 = cv2.morphologyEx(skel_uint8, cv2.MORPH_HITMISS, k2) #DERECHA
    o3 = cv2.morphologyEx(skel_uint8, cv2.MORPH_HITMISS, k3) #IZQUIERDA
    o4 = cv2.morphologyEx(skel_uint8, cv2.MORPH_HITMISS, k4) #ARRIBA

    o5 = cv2.morphologyEx(skel_uint8, cv2.MORPH_HITMISS, k5) #  ↘
    o6 = cv2.morphologyEx(skel_uint8, cv2.MORPH_HITMISS, k6) #  ↙
    o7 = cv2.morphologyEx(skel_uint8, cv2.MORPH_HITMISS, k7) #  ↖
    o8 = cv2.morphologyEx(skel_uint8, cv2.MORPH_HITMISS, k8) #  ↗


    #arriba probablemente haga falta añadir mas operaciones de HITMISS para las 4 diagonales

    # add results of all the above 4
    endpoints_img = o1 + o2 + o3 + o4 + o5 + o6 + o7 + o8
    # arriba probablemente haga falta sumar otra 4 de las diagonales

    # Busca exactamente cada endpoint
    end_pts_array = np.argwhere(endpoints_img != 0) #Antes era: endpoints_img == 255 pero a veces no servia
    #print("aca:", end_pts_array)
    num_pts = len(end_pts_array)

    return end_pts_array, num_pts, endpoints_img
#####


def PrintImgEndpoint(end_pts_array, frame_i):
    frame_bgr = cv2.cvtColor(frame_i, cv2.COLOR_RGB2BGR)

    for pt in end_pts_array:
        #print(pt)
        frame_bgr = cv2.circle(frame_bgr, (pt[1], pt[0]), 6, (0,255,0),-1)
        plt.xlabel("Ancho (Pixeles)"); plt.ylabel("Alto (Pixeles)")
    ####
    imshow(True, frame_bgr, '2.7) EndPoints', 'lower', 'hsv')
    return

def Copiar(frame_i):
    return frame_i.Copy() 
####


#Funcion que se usará dentro de como se determina que tan cerca esta un endpoint del eslabón del robot
def Pixel_a_metro(P_plotear, pos_en_pixel, px_width, px_height, pos_m_min, pos_m_max):
    pos_deseada_en_m_x = [] 
    pos_deseada_en_m_y = []

    #obtenemos el tamaño del recuadro para disponible para escribir (metros):
    m_width = pos_m_max[0] - pos_m_min[0]  #mx
    m_height = pos_m_max[1] - pos_m_min[1] #my

    #el offset determinado por nosotros aca se establece:
    m_x_offset = pos_m_min[0]
    m_y_offset = pos_m_min[1]

    #aca se obtiene cada componente:
    px_x_i = pos_en_pixel[0] #r
    px_y_i = pos_en_pixel[1] #c

    #aca se convierte a metros dichos componentes:
    m_x_i = m_x_offset + (( px_x_i / px_width) * m_width)
    m_y_i = m_y_offset + (( px_y_i / px_height) * m_height)

    #guarda en tablas.
    pos_deseada_en_m_x.append(m_x_i)
    pos_deseada_en_m_y.append(m_y_i)
    
    #lo pasa a array 
    pos_deseada_en_m = [pos_deseada_en_m_x, pos_deseada_en_m_y]
    nparray = np.array(pos_deseada_en_m)

    
    return nparray
###funcion end




def imshow(P_plotear, img, titulo, origintipo, cmaptipo):
    if P_plotear:
        if (cmaptipo=='rgb'):
            plt.imshow(img, origin=origintipo ); plt.title(titulo); plt.show()
        else:
            plt.imshow(img, origin=origintipo, cmap=cmaptipo ); plt.title(titulo); plt.show()
####




print("Ejecuta el otro archivo")
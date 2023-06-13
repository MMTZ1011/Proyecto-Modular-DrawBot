import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle


def Buscar(P_plotear, copia_skel, punto_i ):
    
    # obtiene los puntos x y y
    inicio_x = punto_i[1] 
    inicio_y = punto_i[0]

    #INICIA EL ALGORITMO:
    # aca es donde guarda la secuencia de la trayectoria total

    pos_x = inicio_x #asigna 
    pos_y = inicio_y #asigna

    secuencia_x = [inicio_x] #guarda en pixeles sin considerar centro 
    secuencia_y = [inicio_y] #guarda en pixeles sin considerar centro
    copia_skel[pos_y][pos_x] = 0 #debe borrar el del inicio para que lo ignore:
    num_pts_trackeados = 1 #guarda los puntos que ya ha eliminado o trackeado para la trayectoria

    ciclo = True ; # ciclo de que estará haciendo iteraciones

    while ciclo: #Mientras el ciclo sea verdadero
        encontro = False # Inicializa en falso

        #print("Nuevo pixel, "+ "R coord: [ "+ str(pos_x) +" , "+ str(pos_y) +"]=") #Descomentar para ver el proceso
        #recorre de izquierda a derecha de abajo para arriba alrededor del punto, hasta pasa por donde estaba el punto
        for pos_y_i in range(pos_y-1, pos_y+2):  # y horizontal
            for pos_x_i in range(pos_x-1, pos_x+2):  # x vertical
                # aca es el código para ver que pasa con el pixel candidato a ser el siguiente
                # vamos averiguar si lo termina siendo 
                pixel_i = copia_skel[pos_y_i][pos_x_i] 
                #print("R coord: [ "+ str(pos_x_i) +" , "+ str(pos_y_i) +"]= "+ str(pixel_i)  ) #Descomentar para ver el proceso

                if pixel_i == 255: #si es 255 que equivale a blanco entonces:
                    # En este bloque de código es lo que pasa si el pixel que encontro alrededor del nuevo pixel

                    # guarda el resultado en una nueva posicion para la secuencia:
                    secuencia_x.append(pos_x_i)
                    secuencia_y.append(pos_y_i)

                    #Actualiza el numero de puntos que ya trackeo
                    num_pts_trackeados += 1 

                    # Asigna 0 para que no vuelva a detectarlo al pasar el algoritmo:
                    copia_skel[pos_y][pos_x] = 0 

                    #Nuevas asignaciones para el proximo while
                    pos_x = pos_x_i 
                    pos_y = pos_y_i

                    # Dice que ya encontro para que no siga haciendo fors
                    encontro = True

                    break #rompe el for para x (pos_x_i)
                # end de si el pixel es 255
                
                if encontro == True:
                  break #rompe el for para x (pos_x_i)
                # End de si encontro debe romper el for de x
            
            if encontro == True:
                break #rompe el for para y (pos_y_i)
            # End de si encontro debe romper el for de y

            # end for para eje horizontal (pos_x)
        #end for para eje vertical (pos_y)

        # cierra ciclo si no encontro nada extiende poquito más su filtro
        if  encontro == False:
            ciclo = False #detiene esta funcion y la terminará
        #end de encontro
    #### ciclo


    if (P_plotear):
        plt.xlabel("Ancho (Pixeles)"); plt.ylabel("Alto (Pixeles)")
        imshow(P_plotear, copia_skel, '3.1) Trayectoria Resultado', 'lower', 'gray')

        img_width = np.size(copia_skel, 1)
        img_height = np.size(copia_skel, 0)

        ## Vamos a plotear la trayectoria
        plt.plot(secuencia_x, secuencia_y); plt.title('3.2) Secuencia de Trayectoria,'+ ' num_puntos='+ str(num_pts_trackeados) ); 
        plt.xlim(0, img_width); plt.ylim(0, img_height)
        plt.xlabel("Ancho (Pixeles)"); plt.ylabel("Alto (Pixeles)")
        plt.show()
    ###fin if
    
    return  secuencia_x, secuencia_y, num_pts_trackeados



def Reducir_Calidad(P_plotear, segundos_laser, resolucion, num_pts_trackeados, secuencia_x, secuencia_y, img_width, img_height):
    # Vamos a reducir la cantidad de puntos
    tl = np.linspace(0, segundos_laser, num_pts_trackeados, dtype="float")

    # Utilizando acá nos da esto pero sin en HD
    secuencia_x_sin_HD = secuencia_x[::resolucion]
    secuencia_y_sin_HD = secuencia_y[::resolucion]
    tl_sin_HD = tl[::resolucion]
    num_pts_trackeados_sin_HD = len(tl_sin_HD)

    if (P_plotear):
        plt.plot(secuencia_x_sin_HD, secuencia_y_sin_HD, linestyle = 'dotted', marker = '.', ms = 7);
        plt.xlabel("Ancho (Pixeles)"); plt.ylabel("Alto (Pixeles)")
        plt.title('3.3) Reduccion calidad trayectoria,'+ ' num_puntos='+ str(num_pts_trackeados_sin_HD))
        plt.plot(secuencia_x_sin_HD[0], secuencia_y_sin_HD[0], linestyle = 'dashed', marker = 'o', ms = 8)
        plt.legend(['Trayectoria', 'Punto inicio de trayectoria'])
        plt.xlim(0, img_width); plt.ylim(0, img_height)
        plt.show()


        #Imprime las trayectorias deseadas en grafica lineal respecto al tiempo
        plt.plot(tl_sin_HD, secuencia_x_sin_HD, linestyle = 'dashed', marker = 'o', ms = 8)
        plt.plot(tl_sin_HD, secuencia_y_sin_HD, linestyle = 'dashed', marker = 'o', ms = 8)
        plt.title('3.4) Trayectoria de posiciones deseadas, '+'resolucion='+str(resolucion)); 
        plt.xlabel("Tiempo (segundos)"); plt.ylabel("Posiciones (pixeles)"); plt.legend(['pos-deseada_x', 'pos-deseada_y'])
        plt.show()
    #####

    return secuencia_x_sin_HD, secuencia_y_sin_HD, tl_sin_HD, num_pts_trackeados_sin_HD
#####




def PosDeseadas_Pixels(P_plotear, secuencia_x_sin_HD, secuencia_y_sin_HD, num_pts_trackeados_sin_HD, img_width, img_height):
    #Unimos las dos secuencias con resolucion (no full HD)
    pos_deseada_en_pixeles_x = [] 
    pos_deseada_en_pixeles_y = []

    #Recorre cada punto de la secuencia:
    for index in range(num_pts_trackeados_sin_HD):
        #pos_deseada_en_pixeles.append([secuencia_x_sin_HD[index], secuencia_y_sin_HD[index]])
        pos_deseada_en_pixeles_x.append(secuencia_x_sin_HD[index])
        pos_deseada_en_pixeles_y.append(secuencia_y_sin_HD[index])
    # del recorrido fors

    pos_deseada_en_pixeles = [pos_deseada_en_pixeles_x, pos_deseada_en_pixeles_y]
    if (P_plotear):
        plt.plot(pos_deseada_en_pixeles_x, pos_deseada_en_pixeles_y, linestyle = 'dotted', marker = '.', ms = 7);
        plt.xlim(0, img_width); plt.ylim(0, img_height)
        plt.xlabel("Ancho (Pixeles)"); plt.ylabel("Alto (Pixeles)")
        plt.title('4.1) Imagen en plano Pixeles ')
        plt.show()

        #print("Esta es la lista de trayectorias finales que debe seguir (en pixeles):")
        #print(pos_deseada_en_pixeles)
    #######
    
    
    return pos_deseada_en_pixeles




def PosDeseada_m(P_plotear, PosDeseadas_pixels, px_width, px_height, pos_m_min, pos_m_max):
    pos_deseada_en_m_x = [] 
    pos_deseada_en_m_y = []

    #obtenemos el tamaño del recuadro para disponible para escribir (metros):
    m_width = pos_m_max[0] - pos_m_min[0]  #mx
    m_height = pos_m_max[1] - pos_m_min[1] #my

    m_x_offset = pos_m_min[0]
    m_y_offset = pos_m_min[1]

    #print(PosDeseadas_pixels)
    
    for index in range( len(PosDeseadas_pixels[0]) ):
        #Obtenemos el la pos en pixeles actuales:
        px_x_i = PosDeseadas_pixels[0][index] #r
        px_y_i = PosDeseadas_pixels[1][index] #c

        #convertimos la pos en pixeles a metros:
        m_x_i = m_x_offset + (( px_x_i / px_width) * m_width)
        m_y_i = m_y_offset + (( px_y_i / px_height) * m_height)

        #guarda en tablas.
        pos_deseada_en_m_x.append(m_x_i)
        pos_deseada_en_m_y.append(m_y_i)
    ############

    pos_deseada_en_m = [pos_deseada_en_m_x, pos_deseada_en_m_y]
    ##IMPRIME
    if (P_plotear):
        fig, ax = plt.subplots()
        plt.plot(pos_deseada_en_m_x, pos_deseada_en_m_y, linestyle = 'dotted', marker = '.', ms = 7);
        plt.axis('image')
        plt.xlim(-0.1, pos_m_max[0]+0.1); plt.ylim(-0.1, pos_m_max[1]+0.1)
        plt.xlabel("Ancho (metros)"); plt.ylabel("Alto (metros)")
        plt.title('4.2) Imagen en plano metros')
        plt.axhline(y=0, color='black', linestyle = 'dashed') #Linea en eje x
        plt.axvline(x=0, color='black', linestyle = 'dashed') #Linea en eje y
        zone = Rectangle((pos_m_min[0], pos_m_min[1]), pos_m_max[0] - pos_m_min[0], pos_m_max[1]- pos_m_min[1], linewidth=1, edgecolor='r', facecolor='none')
        ax.add_patch(zone)
        plt.show()

        #print("Esta es la lista de trayectorias finales que debe seguir (en Metros):")
        #print(pos_deseada_en_m)
    ###
    nparray = np.array(pos_deseada_en_m)

    
    return nparray
###funcion end



def Elegir_Endpoint(P_plotear, Modo):
    if Modo == "n_efector":
        print(1)
    elif Modo == "escritura":
        print(2)
    elif Modo == "puntorojo":
        print(2)
    ###
####

def imshow(P_plotear, img, titulo, origintipo, cmaptipo):
    if P_plotear:
        if (cmaptipo=='rgb'):
            plt.imshow(img, origin=origintipo ); plt.title(titulo); plt.show()
        else:
            plt.imshow(img, origin=origintipo, cmap=cmaptipo ); plt.title(titulo); plt.show()
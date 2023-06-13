import matplotlib.pyplot as plt
import math
from matplotlib.patches import Circle
from matplotlib.patches import Rectangle


def Trayectoria(P_plotear, titulo, nombre_archivo, theta_plot, q_plot,  q_inicial, PosDeseadas_m, pos_m_min, pos_m_max, longitud_Eslabones, x_lim_inferior, x_lim_superior, y_lim_inferior, y_lim_superior):
    # Imprime una gráfica que muestra la trayectoria deseada y la que se otuvos
    fig, ax = plt.subplots()
    plt.plot(q_plot[0], q_plot[1], linestyle = 'dashed', marker = '*', ms = 3) # grafica de posicion obtenida
    plt.plot(PosDeseadas_m[0], PosDeseadas_m[1], linestyle = 'dotted', marker = '.', ms = 3) #grafica de posiciones deseadas
    plt.legend(['Trayectoria Obtenida','Trayectoria deseada'])
    plt.plot(q_inicial[0], q_inicial[1], linestyle = 'dashed', marker = '*', ms = 15)  #plotea la posicion inicial del robot al comenzar
    plt.xlabel("Ancho (metros)"); plt.ylabel("Alto (metros)")
    plt.title(titulo)
    #plt.axhline(y=0, color='black', linestyle = 'dashed')
    plt.axis('image')
    plt.xlim(x_lim_inferior, x_lim_superior); 
    plt.ylim(y_lim_inferior, y_lim_superior)
    plt.axhline(y=0, color='black', linestyle = 'dashed') #Linea en eje x
    plt.axvline(x=0, color='black', linestyle = 'dashed') #Linea en eje y

    #rectangulo zona escritura:
    zone = Rectangle((pos_m_min[0], pos_m_min[1]), pos_m_max[0] - pos_m_min[0], pos_m_max[1]- pos_m_min[1], linewidth=1, edgecolor='r', facecolor='none')
    #circulo art 1
    circ_art_1 = Circle(xy=(0, 0), radius=0.025 , edgecolor='black', facecolor='#87CEFA', linewidth=2)
    
    # Eslabón 1 linea/rectangulo
    width, height = 1, 0 # Ancho y altura del rectángulo
    x0, y0 = 0, -(height/2) # Coordenadas del punto ancla
    angle_deg =  math.degrees(theta_plot[0][-1])
    angle_rad = math.radians(angle_deg) # Convertir el ángulo de rotación a radianes
    # Calcular las coordenadas de las esquinas del rectángulo después de la rotación:
    Rect_eslabon_1 = Rectangle((x0, y0), width, height, angle=angle_deg, edgecolor='b', facecolor='none')# Crear el rectángulo rotado

    #circulo art 2
    otro_x = x0 + longitud_Eslabones[1] * math.cos(angle_rad)
    otro_y = y0 + longitud_Eslabones[1] * math.sin(angle_rad)
    circ_art_2 = Circle(xy=(otro_x, otro_y), radius=0.025 , edgecolor='black', facecolor='#87CEFA', linewidth=2)

    #eslabón 2 linea/rectangulo
    width, height = 1, 0 # Ancho y altura del rectángulo
    x0, y0 = otro_x, otro_y # Coordenadas del punto ancla
    angle_deg =  math.degrees(theta_plot[1][-1]) + math.degrees(theta_plot[0][-1])
    angle_rad = math.radians(angle_deg) # Convertir el ángulo de rotación a radianes
    Rect_eslabon_2 = Rectangle((x0, y0), width, height, angle=angle_deg, edgecolor='b', facecolor='none')# Crear el rectángulo rotado

    # Añadir el círculo al plot
    ax.add_patch(zone)
    ax.add_patch(circ_art_1)
    ax.add_patch(Rect_eslabon_1)
    ax.add_patch(circ_art_2)
    ax.add_patch(Rect_eslabon_2)

    
    #plt.savefig(nombre_archivo)
    plt.show()


####



def Errores(P_plotear, titulo_1, titulo_2, e_plot, tplot):
    if P_plotear:
        # IMPRIME dos graficas de los Errores en 'x' y 'y'
        plt.subplot(2,1,1)
        plt.plot(tplot, e_plot[0])
        plt.xlabel("Tiempo (segundos)"); plt.ylabel("Posicion x (metros)")
        plt.title(titulo_1)
        plt.axis([0, tplot[-1], min(e_plot[0]), max(e_plot[0])])
        plt.axhline(y=0, color='orange', linestyle = 'dashed')

        plt.subplot(2,1,2)
        plt.plot(tplot, e_plot[1])
        plt.xlabel("Tiempo (segundos)"); plt.ylabel("Posicion y (metros)")
        plt.title(titulo_2)
        plt.axis([0, tplot[-1], min(e_plot[1]), max(e_plot[1])])
        plt.axhline(y=0, color='orange', linestyle = 'dashed')

        plt.show()
    #####
###


def Ganancias(P_plotear, titulo_1, titulo_2,  w_1, w_2, tplot):
    if P_plotear:
        # IMPRIME Las ganancias
        plt.subplot(2,1,1)
        plt.plot(tplot, w_1[0])
        plt.plot(tplot, w_1[1])
        plt.plot(tplot, w_1[2])
        plt.legend(['kd','kd','ki'])
        plt.xlabel("Tiempo (segundos)"); plt.ylabel("Valores (metros)")
        plt.title(titulo_1)

        plt.subplot(2,1,2)
        plt.plot(tplot, w_2[0])
        plt.plot(tplot, w_2[1])
        plt.plot(tplot, w_2[2])
        plt.legend(['kd','kd','ki'])
        plt.xlabel("Tiempo (segundos)"); plt.ylabel("Valores (metros)")
        plt.title(titulo_2)

        plt.show()
    ######
####



def Tau(P_plotear, titulo_1, titulo_2, tau_plot,  tplot):
    if P_plotear:
        # IMPRIME dos graficas de la acción de control.
        plt.subplot(2,1,1)
        plt.plot(tplot, tau_plot[0])
        plt.xlabel("Tiempo (segundos)"); plt.ylabel("Voltaje")
        plt.title(titulo_1)
        plt.axis([0, tplot[-1], min(tau_plot[0]), max(tau_plot[0])])
        plt.axhline(y=0, color='orange', linestyle = 'dashed')

        plt.subplot(2,1,2)
        plt.plot(tplot, tau_plot[1])
        plt.xlabel("Tiempo (segundos)"); plt.ylabel("Voltaje")
        plt.title(titulo_2)
        plt.axis([0, tplot[-1], min(tau_plot[1]), max(tau_plot[1])])
        plt.axhline(y=0, color='orange', linestyle = 'dashed')

        plt.show()
    #####
####
 

def Impresion_Rapida(img, title, xlabel, ylabel, origin, cmap):
    plt.xlabel(xlabel); plt.ylabel(ylabel)
    plt.imshow(img, origin=origin, cmap=cmap ); plt.title(title); plt.show()
####
# Ejemplo:
# Imprimir.Impresion_Rapida(skel_Total, '1 de impresion', 'Ancho (Pixeles)', 'Alto (Pixeles)', 'lower', 'gray')






## aca de imprimir procesos en lo del robot:

#Pos home
def Print_Home_tray(P_plotear, Imprimir_home, theta_plot, q_plot, q_inicial, pos_0, pos_m_min, pos_m_max, longitud_Eslabones, x_lim_inferior, x_lim_superior, y_lim_inferior, y_lim_superior, e_plot, tplot, w_1, w_2, tau_plot, Imprimir_Errores, Imprimir_Ganancias, Imprimir_AccionControl):
    # IMPRIMIR pos home
    if Imprimir_home:
        Trayectoria(P_plotear, '4.3) Pos plano "x" "y" vs deseada', 'pos_home.png', theta_plot, q_plot,  q_inicial, pos_0, pos_m_min, pos_m_max, longitud_Eslabones, x_lim_inferior, x_lim_superior, y_lim_inferior, y_lim_superior)
        Errores(Imprimir_Errores, '4.4) Errores de pos x', 'Errores de pos y', e_plot, tplot)
        Ganancias(Imprimir_Ganancias, '4.5) Ganancias Articulación 1', 'Ganancias Articulación 2', w_1, w_2, tplot)
        Tau(Imprimir_AccionControl, '4.6) Acción de control art. 1', 'Acción de control art. 2', tau_plot,  tplot)
    ####
### Funcion 




#Pos trayectorias
def Print_trayec_tray(P_plotear, Imprimir_trayecto, theta_plot, q_plot, q_inicial, PosDeseadas_m, pos_m_min, pos_m_max, longitud_Eslabones, x_lim_inferior, x_lim_superior, y_lim_inferior, y_lim_superior, e_plot, tplot, w_1, w_2, tau_plot, Imprimir_Errores, Imprimir_Ganancias, Imprimir_AccionControl):
    # IMPRIMIR pos trayectoria
    if Imprimir_trayecto:
        Trayectoria(P_plotear, '4.7) Pos plano "x" "y" vs deseada', 'Trayectoria_generada.png', theta_plot, q_plot,  q_inicial, PosDeseadas_m, pos_m_min, pos_m_max, longitud_Eslabones, x_lim_inferior, x_lim_superior, y_lim_inferior, y_lim_superior)
        Errores(Imprimir_Errores, '4.8) Errores de pos x', 'Errores de pos y', e_plot, tplot)
        Ganancias(Imprimir_Ganancias, '4.9) Ganancias Articulación 1', 'Ganancias Articulación 2', w_1, w_2, tplot)
        Tau(Imprimir_AccionControl, '4.10) Acción de control art. 1', 'Acción de control art. 2', tau_plot,  tplot)
    ####
### Funcion 



#Pos trayectorias
def Print_final_tray(P_plotear, Imprimir_final, theta_plot, q_plot, q_inicial, pos_0, pos_m_min, pos_m_max, longitud_Eslabones, x_lim_inferior, x_lim_superior, y_lim_inferior, y_lim_superior, e_plot, tplot, w_1, w_2, tau_plot, Imprimir_Errores, Imprimir_Ganancias, Imprimir_AccionControl):
    # IMPRIMIR pos final
    if Imprimir_final:
        Trayectoria(P_plotear, '4.11) Pos plano "x" "y" vs deseada','pos_final.png', theta_plot, q_plot,  q_inicial, pos_0, pos_m_min, pos_m_max, longitud_Eslabones, x_lim_inferior, x_lim_superior, y_lim_inferior, y_lim_superior)
        Errores(Imprimir_Errores, '4.12) Errores de pos x', 'Errores de pos y', e_plot, tplot)
        Ganancias(Imprimir_Ganancias, '4.13) Ganancias Articulación 1', 'Ganancias Articulación 2', w_1, w_2, tplot)
        Tau(Imprimir_AccionControl, '4.14) Acción de control art. 1', 'Acción de control art. 2', tau_plot,  tplot)
    ####
### Funcion 



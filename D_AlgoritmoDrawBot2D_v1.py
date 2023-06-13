import numpy as np
import matplotlib.pyplot as plt
import math
from datetime import datetime


#de aca obtiene las variables:


# version 2 actualizada hasta el 3 de mayo


# Librerias hechas por nosotros:
import ImagenV1 as Imagen
import Trayectoria as Trayectoria
import neuronaadaptativav3 as Neurona
import Resultadosv1 as Imprimir
import RobotFuncionesV1 as RobotFx


#esto se edita desde "configuracion_proyecto.py" 

from configuracion_proyecto import longitud_Eslabones, angulos_iniciales, pos_m_min
from configuracion_proyecto import Kp, Ki, Kd
from configuracion_proyecto import eta, alpha, dt
from configuracion_proyecto import rango_minimo_Posicionamiento, rango_minimo_trayectoria
from configuracion_proyecto import resolucion
from configuracion_proyecto import x_lim_inferior, y_lim_inferior, x_lim_extra_offset , y_lim_extra_offset




#### DESDE ESTE PUNTO NADA ES CONFIGURABLE LO CALCULA EDITAR EL "configuracion_proyecto.py" 

# NO CAMBIAR:
segundos_laser = 5 #segundos que dura la cnc esto no es necesario configurar

## Parametros de area de trabajod el robot: (ESTO LO CALCULAMOS)
hipotenusa = longitud_Eslabones[0] + longitud_Eslabones[1] # NO MODIFICAR (PERO SE PUEDE MODIFICAR EL TAMAÑO DE CADA ESLABON DEL ROBOT)
pos_m_max = [(hipotenusa* math.sin(math.radians(45) ) ), (hipotenusa* math.cos(math.radians(45) ) )] # NO MODIFICAR

## PARAMETROS IMPRESION RESULTADO (lo calcula)
x_lim_superior = pos_m_max[0] + x_lim_extra_offset     #Valor defecto: pos_m_max[0] + 0.1
y_lim_superior = pos_m_max[1] + y_lim_extra_offset   #valor defecto:    pos_m_max[1] + 0.1 

## Parametros para la neurona: ( lo calculo)
w = np.concatenate((Kp, Ki, Kd), axis=1)





def Main_algoritmo(RASPBERRY_PI_MODE, SOLO_1_VEZ, img_i, lower_select, upper_select, P_plotear_img, P_plotear_skeleto, P_plotear_Secuencia, P_plotear_resolucion_baja, P_plotear_PosDeseadas_pixels, P_plotear_PosDeseadas_m, Imprimir_home, Imprimir_trayecto, Imprimir_final, Imprimir_Errores, Imprimir_Ganancias, Imprimir_AccionControl,nombre_imagen):
    ##### ACA EMPIEZA EL CODIGO
    # 0) Empieza el código:
    print(datetime.now().strftime("%H:%M:%S"),"-", "Ejecutando código... ")


    # 1) Cargamos imagen
    img_width, img_height = Imagen.Get_Propiedades(img_i)

    # 2) Seleccionamos un segmento de la imagen basado en color
    seleccion, seleccion_rgb = Imagen.Get_Seleccion(P_plotear_img, img_i, lower_select, upper_select)

    # 3) Realiza esqueletización de la imagen binaria (blanco y negro)
    skel_Total = Imagen.Get_Skeletization(P_plotear_skeleto, seleccion) #primer skel que hace para luego copiar



    # A) Inicia ciclo para hacer robot.
    Repetir = True # por defecto esta en true (NO MODIFICAR)
    # Variables del robot: (NO EDITAR) esto se va actualizando
    if RASPBERRY_PI_MODE== True:
        pass
    elif RASPBERRY_PI_MODE==False:
        angulos_actuales = angulos_iniciales
    ####modo



#####################################################################
    # Empieza con el proceso de seguir trayectos.
    iteracion_num = 1
    while (Repetir==True):
        print("---------------------------------------")
        print("Iniciando trayector #", iteracion_num)

        # 4) Obtiene array de Endpoints del skel
        EndPoints_array, EndPoints_Num, endpoints_img = Imagen.Get_EndPoints(skel_Total)
        #print("End points detectados:", EndPoints_Num)
        if (EndPoints_Num > 0):
            print("Hay trayectos")
            Repetir = True
        else:
            print("No hay más trayectos")
            #print("No encontró ningun trayecto a recorrer")
            Repetir = False #No intentará hacer trayectos
            
            #Imprimir.Impresion_Rapida(endpoints_img, '-1) No encontro endpoints aquí::', 'Ancho (Pixeles)', 'Alto (Pixeles)', 'lower', 'gray')
            break #Rompe el codigo
        ###
        #Imprimir.Impresion_Rapida(endpoints_img, '0) End points', 'Ancho (Pixeles)', 'Alto (Pixeles)', 'lower', 'gray')

        # B) Elije el i de los Endpoints
        pos_actual_m = RobotFx.pos(angulos_actuales, longitud_Eslabones) #Posicion actual del n-efector en metro
        

        # AHORA BUSCA EL pixel mas cerca de donde está el robot
        pixel_menor_distancia = None
        menor_distancia = float('inf')
        for pos_i_px in EndPoints_array: #Recorre cada edpoint
            pos_i_m = Imagen.Pixel_a_metro(P_plotear_img, pos_i_px, img_width, img_height, pos_m_min, pos_m_max)
            distancia = np.linalg.norm(pos_actual_m - pos_i_m)
            if distancia < menor_distancia:
                menor_distancia = distancia
                pixel_menor_distancia = pos_i_px
            ####
        ####
        punto_i = pixel_menor_distancia #Punto elegido para empezar
        #print(punto_i)
        
        #Imprimir.Impresion_Rapida(skel_Total, '1) de impresion', 'Ancho (Pixeles)', 'Alto (Pixeles)', 'lower', 'gray')




        # 5) busca la secuencia de la trayectoria basandonos en el punto
        secuencia_x, secuencia_y, num_pts_trackeados = Trayectoria.Buscar(P_plotear_Secuencia, skel_Total, punto_i )
        #Imprimir.Impresion_Rapida(skel_Total, '2) de impresion', 'Ancho (Pixeles)', 'Alto (Pixeles)', 'lower', 'gray')

        # 6) Reducimos la cantidad de puntos de la secuencia de trayectoria
        secuencia_x_sin_HD, secuencia_y_sin_HD, tl_sin_HD, num_pts_trackeados_sin_HD = Trayectoria.Reducir_Calidad(P_plotear_resolucion_baja, segundos_laser, resolucion, num_pts_trackeados, secuencia_x, secuencia_y, img_width, img_height)
        
        # 7) Genera la lista con las posiciones deseadas en pixeles
        PosDeseadas_pixels = Trayectoria.PosDeseadas_Pixels(P_plotear_PosDeseadas_pixels, secuencia_x_sin_HD, secuencia_y_sin_HD, num_pts_trackeados_sin_HD, img_width, img_height)

        # 8) Proceso para posiciones deseadas m
        PosDeseadas_m = Trayectoria.PosDeseada_m(P_plotear_PosDeseadas_m, PosDeseadas_pixels, img_width, img_height, pos_m_min, pos_m_max) #Recorrido
        pos_0 = PosDeseadas_m[:,0] # posicion 1 de la trayectoria encontrada
        pos_final = RobotFx.pos(angulos_iniciales, longitud_Eslabones) #Guarda esta posición posicion i=0 del recorrido a la 



        # 9) ETAPA RED NEURONAL Adaptativa

        # 10) Pos home.
        P_plotear = True
        w = np.concatenate((Kp, Ki, Kd), axis=1) #pone esto para reiniciar
        theta_plot, qp_plot, q_plot, tau_plot, e_plot, w_1, w_2, q_inicial, tiempo_total, tplot = Neurona.C_Posicionamiento(Imprimir_home, pos_0, longitud_Eslabones, angulos_actuales, w, eta, alpha[0], dt,rango_minimo_Posicionamiento )
        Imprimir.Print_Home_tray(P_plotear, Imprimir_home, theta_plot, q_plot, q_inicial, pos_0, pos_m_min, pos_m_max, longitud_Eslabones, x_lim_inferior, x_lim_superior, y_lim_inferior, y_lim_superior, e_plot, tplot, w_1, w_2, tau_plot, Imprimir_Errores, Imprimir_Ganancias, Imprimir_AccionControl)


        # 11) Trayectoria que imita el robot.
        angulos_actuales = np.array([ theta_plot[0][-1] , theta_plot[1][-1] ]).reshape(2,1)#este serán los angulos iniciales
        w = np.concatenate((Kp, Ki, Kd), axis=1) #pone esto para reiniciar
        theta_plot, qp_plot, q_plot, tau_plot, e_plot, w_1, w_2, q_inicial, tiempo_total, tplot = Neurona.C_Trayectoria(Imprimir_trayecto, PosDeseadas_m, longitud_Eslabones, angulos_actuales, w, eta, alpha[1], dt, rango_minimo_trayectoria)
        Imprimir.Print_trayec_tray(P_plotear, Imprimir_trayecto, theta_plot, q_plot, q_inicial, PosDeseadas_m, pos_m_min, pos_m_max, longitud_Eslabones, x_lim_inferior, x_lim_superior, y_lim_inferior, y_lim_superior, e_plot, tplot, w_1, w_2, tau_plot, Imprimir_Errores, Imprimir_Ganancias, Imprimir_AccionControl)


        #actualiza los angulos actuales y el w lo reinicia # ANTES:12) Pos final.
        angulos_actuales = np.array([ theta_plot[0][-1] , theta_plot[1][-1] ]).reshape(2,1) #angulos finales en los que se quedó el robot.
        w = np.concatenate((Kp, Ki, Kd), axis=1) #pone esto para reiniciar
        #theta_plot, qp_plot, q_plot, tau_plot, e_plot, w_1, w_2, q_inicial, tiempo_total, tplot = Neurona.C_Posicionamiento(P_plotear, pos_final, longitud_Eslabones, angulos_actuales, w, eta, alpha[2], dt,rango_minimo_Posicionamiento )
        Imprimir.Print_final_tray(P_plotear, Imprimir_final, theta_plot, q_plot, q_inicial, pos_0, pos_m_min, pos_m_max, longitud_Eslabones, x_lim_inferior, x_lim_superior, y_lim_inferior, y_lim_superior, e_plot, tplot, w_1, w_2, tau_plot, Imprimir_Errores, Imprimir_Ganancias, Imprimir_AccionControl)

        print("Terminado un trayecto #", iteracion_num)


        #Imprimir.Impresion_Rapida(skel_Total, '3) de impresion', 'Ancho (Pixeles)', 'Alto (Pixeles)', 'lower', 'gray')

        if SOLO_1_VEZ ==True:
            Repetir = False #Con esto rompe el ciclo
        ####

        iteracion_num += 1
    #### while de repetir

    print("Terminó todos los trayectos. En total: ",iteracion_num-1 )

    #Ahora si ya que terminó


    # 12) Pos final.
    angulos_actuales = np.array([ theta_plot[0][-1] , theta_plot[1][-1] ]).reshape(2,1) #angulos finales en los que se quedó el robot.
    w = np.concatenate((Kp, Ki, Kd), axis=1) #pone esto para reiniciar
    theta_plot, qp_plot, q_plot, tau_plot, e_plot, w_1, w_2, q_inicial, tiempo_total, tplot = Neurona.C_Posicionamiento(Imprimir_final, pos_final, longitud_Eslabones, angulos_actuales, w, eta, alpha[2], dt,rango_minimo_Posicionamiento )
    #Imprimir.Print_final_tray(P_plotear, Imprimir_final, theta_plot, q_plot, q_inicial, pos_0, pos_m_min, pos_m_max, longitud_Eslabones, x_lim_inferior, x_lim_superior, y_lim_inferior, y_lim_superior, e_plot, tplot, w_1, w_2, tau_plot)



    print("---------------------------------------")
    print(datetime.now().strftime("%H:%M:%S"),"-" ,"Código ejecutado correctamente...")
####Main_algoritmo
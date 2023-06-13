import numpy as np
import math


#****************************************# CONFIGURACIONES IMPORTANTES: #****************************************# 

## Parametros fisicos para El robot:
longitud_Eslabones = np.transpose( np.array([1, 1])    ) #Longitsud de eslabones (esta en metros)
angulos_iniciales = np.array([                #(esta en radianes)
                        math.radians(-45) , 
                        math.radians(135)
                        ]).reshape(2,1) 

# posicion minima desde donde el robot empieza a escribir ()
pos_m_min = [ (0.15), (0.15)]  # MODIFICAR (esta en metros)

#****************************************#  Parametros controlador: #****************************************# 

# Parametros para la neurona:
Kp = np.array([1.0, 1.0]).reshape(2,1)  # ganancias proporcionales
Ki = np.array([0.0, 0.0]).reshape(2,1)  # ganancias integrales
Kd = np.array([0.0, 0.0]).reshape(2,1)  # ganancias derivativas
# w = np.concatenate((Kp, Ki, Kd), axis=1) esto lo hace en D_algoritmoDrawbot2D_v1

eta = np.array([[1, 1, 0.00001],
                [1, 1, 0.00001]])  # pesos para el controlador proporcional y derivativo

alpha = np.array([0.01, 0.01, 0.1])  # factor de ajuste para el controlador proporcional y derivativo

dt = 0.001  # tiempo de muestreo (triangulo t)




## Parametros globales:
P_plotear = False #Si va poner graficas o qué
resolucion = 1 #Mejor resolucion de si reduce puntos o no

### Esto es para el error
rango_minimo_Posicionamiento = 0.005 #Rango minimo de error diferencia de distancias en m para pos home
rango_minimo_trayectoria = 0.01 #Rango minimo de error diferencia de distancias en m para trayectoria


#****************************************# PARAMETROS CAMARA #****************************************#
#solo funcionan y se ven en la raspberry pi
resolucion_cam = (640, 480)
resolucion_display = (640, 480) #de la pantalla que se abre

nombre_foto = "tempfoto.png" #NO CAMBIAR
brillo_automatico = False
contraste = 0.5
brillo = 0.5




#****************************************#  PARAMETROS PARA RANGOS DE COLORES #****************************************#

#para caundo estamos cargando dibujos que ya tenemos
lower_select_dibujos = np.array([30, 50, 50]) #color RGB
upper_select_dibujos = np.array([70, 255, 255]) #color RGB

#para las fotos ahora si:
lower_select_camara_verde = np.array([30, 50, 50]) #color RGB
upper_select_camara_verde = np.array([70, 255, 255]) #color RGB

lower_select_camara_rojo = np.array([30, 50, 50]) #color RGB
upper_select_camara_rojo = np.array([70, 255, 255]) #color RGB

lower_select_camara_negro = np.array([30, 50, 50]) #color RGB
upper_select_camara_negro = np.array([70, 255, 255]) #color RGB

## PARAMETROS IMPRESION RESULTADO: (NO MODIFICAR) es para como plotea las graficas que simulan el robot
x_lim_inferior = -0.1   #Valor defecto: -0.5
x_lim_extra_offset = 0.1     #Valor defecto: pos_m_max[0] + 0.1
y_lim_inferior = -0.1      # valor defecto: -0.8
y_lim_extra_offset = 0.1   #valor defecto:    pos_m_max[1] + 0.1 






# Para que no accedan en la presetacion weyes a las configuraciones y nos desconfiguren
#esto funciona en la raspberry
Proteger_con_contra = False
contrasena_dev_mode = "inro"

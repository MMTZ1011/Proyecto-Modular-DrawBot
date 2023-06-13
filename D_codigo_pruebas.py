# CODIGO PARA LA RASPBERRY PI 
import MotoresRaspberry_v2 as CodeMotores

#ESTE MODO ES PARA PROBAR CODIGO EJECUTANDOSE

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

#Librerias Nosotros raspberry pi: 




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





def Main_Custom():
    print("Ejecutando codigo custom")





    print("Termino ejecución de codigo custom")
###fin de Main_Custom

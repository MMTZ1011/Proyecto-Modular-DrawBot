import D_AlgoritmoDrawBot2D_v1

# Librerias hechas por nosotros:
import ImagenV1 as Imagen

#CARGA TODAS LAS VARIABLES DE COLORES DE "Configuracion_proyecto.py" (ignorar)
from configuracion_proyecto import lower_select_dibujos, upper_select_dibujos
from configuracion_proyecto import lower_select_camara_verde, upper_select_camara_verde
from configuracion_proyecto import lower_select_camara_rojo, upper_select_camara_rojo
from configuracion_proyecto import lower_select_camara_negro, upper_select_camara_negro


#MODIFICAR
# informacion de imagen que queremos cargar
nombre_imagen = 'prueba_1' 



#plots de que queremos ver
P_plotear_img = False # si deseas que plote el procesamiento de imagen
P_plotear_skeleto = True #si deseas que plotee el eskeleto
P_plotear_Secuencia = False #si queremos que plotee la secuencia
P_plotear_resolucion_baja = False #si queremos que plote como baja la resolucion
P_plotear_PosDeseadas_pixels = False #si queremos que plotee las posiciones deseadas en pixeles
P_plotear_PosDeseadas_m = False #si queremos que plotee las pos deseadas en m

# De las trayectorias 
Imprimir_home = False
Imprimir_trayecto = True #Casi siempre True para ver que hizo
Imprimir_final = False

#Graficas finales
Imprimir_Errores = False
Imprimir_Ganancias = True
Imprimir_AccionControl = False


#############(NO MODIFICAR):
SOLO_1_VEZ = True #Solo intenta seguir una unica trayectoria sin buscar las demás
RASPBERRY_PI_MODE = False #NO PONER True por que este es el modo PC y este pasa la función Main_Algoritmo con cosas adaptadas para la raspberry pi y los motores
lower_select = lower_select_dibujos
upper_select = upper_select_dibujos




#lo de arriba era configuracion
####### ACA EMPIEZA EL CODIGO (NO MODIFICAR)

ruta_completa = 'VisionEjemplos/' + nombre_imagen + '.png'
# 1) Cargamos imagen
img_i = Imagen.Cargar_Imagen(False, ruta_completa)

#MainAlgoritmo del archivo D_AlgoritmoDrawBot2D_v1.py es el que era Ejemplo1 pero ahora como función

# 2) Ahora ejecuta esto
D_AlgoritmoDrawBot2D_v1.Main_algoritmo(RASPBERRY_PI_MODE, SOLO_1_VEZ, img_i, lower_select, upper_select, 
                                       #aca se ve raro por que hay enter
                                       P_plotear_img, P_plotear_skeleto, P_plotear_Secuencia, P_plotear_resolucion_baja, P_plotear_PosDeseadas_pixels, P_plotear_PosDeseadas_m, 
                                       Imprimir_home, Imprimir_trayecto, Imprimir_final,
                                       Imprimir_Errores, Imprimir_Ganancias, Imprimir_AccionControl,
                                       nombre_imagen
                                       )



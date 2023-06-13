# CODIGO PARA LA RASPBERRY PI 

#Librerias:
import cv2
import matplotlib.pyplot as plt

#Librerias hechas por nosotros:
import MotoresRaspberry_v2 as CodeMotores
import D_camarav1 as CodeCamera
import Proteccion_dev_mode_v1 as CodeProteccion
import D_codigo_pruebas as CodePruebas
import D_AlgoritmoDrawBot2D_v1
import ImagenV1 as Imagen



#CARGA TODAS LAS VARIABLES DE COLORES DE "Configuracion_proyecto.py" (ignorar)
from configuracion_proyecto import lower_select_dibujos, upper_select_dibujos
from configuracion_proyecto import lower_select_camara_verde, upper_select_camara_verde
from configuracion_proyecto import lower_select_camara_rojo, upper_select_camara_rojo
from configuracion_proyecto import lower_select_camara_negro, upper_select_camara_negro

from configuracion_proyecto import nombre_foto

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
RASPBERRY_PI_MODE = False #Este ahora si es true
lower_select = lower_select_dibujos
upper_select = upper_select_dibujos


##funciones

#MODO DE CARGAR SOLO IMAGEN
def MainImagen():
    ##FUNCIONES imagen


    ##EJECUCION:
    print("MODO Carga Imagen")
    print("1) Ingresa un nombre de archivo imagen para cargar")
    print("El archivo debe estar en la raíz del proyecto")
    print("por ejemplo: foto.png")
    while True:
        try:
            nombre_imagen = input("nombre archivo: ")
            #ruta_completa = 'VisionEjemplos/' + nombre_imagen + '.png'
            ruta_completa = nombre_imagen
            img = cv2.imread(ruta_completa)
            if img is None:
                raise ValueError('La imagen no se pudo cargar')
            break#termina while de que no hubo error
        except Exception as e:
            print("Error al cargar la imagen: ", e)
            print("Ingresa un nombre valido para la imagen porfa")
        ####
    ####
    print(" ")
    print("Imagen encontrada.")

    ####### ACA EMPIEZA EL CODIGO (NO MODIFICAR)
    ruta_completa =  nombre_imagen
    #ruta_completa = 'VisionEjemplos/' + nombre_imagen 
    # 1) Cargamos imagen
    img_i = Imagen.Cargar_Imagen(False, ruta_completa)

    # 2) Ahora ejecuta esto
    D_AlgoritmoDrawBot2D_v1.Main_algoritmo(RASPBERRY_PI_MODE, SOLO_1_VEZ, img_i, lower_select, upper_select, 
                                       #aca se ve raro por que hay enter
                                       P_plotear_img, P_plotear_skeleto, P_plotear_Secuencia, P_plotear_resolucion_baja, P_plotear_PosDeseadas_pixels, P_plotear_PosDeseadas_m, 
                                       Imprimir_home, Imprimir_trayecto, Imprimir_final,
                                       Imprimir_Errores, Imprimir_Ganancias, Imprimir_AccionControl
                                       )


    
    #Manda a guardar:
    CodeMotores.Guardar_datos()
#### Main imagen carga

#MODO DE CARGAR SOLO IMAGEN
def MainCamara_DrawBot2D():
    ##EJECUCION:
    print("MODO Camara DrawBot 2D")
    print("Presiona 'Esc' o 'Enter' para tomar captura")

    CodeCamera.Main_Esperar_foto()
    print("Cargando foto...")

    ####### ACA EMPIEZA EL CODIGO (NO MODIFICAR)
    ruta_completa =  nombre_foto
    # 1) Cargamos imagen
    img_i = Imagen.Cargar_Imagen(False, ruta_completa)
    #Invierte la imagen:
    img_i = cv2.flip(img_i, 0) #Voltea eje y
    
    # 2) Ahora ejecuta esto
    D_AlgoritmoDrawBot2D_v1.Main_algoritmo(RASPBERRY_PI_MODE, SOLO_1_VEZ, img_i, lower_select, upper_select, 
                                       #aca se ve raro por que hay enter
                                       P_plotear_img, P_plotear_skeleto, P_plotear_Secuencia, P_plotear_resolucion_baja, P_plotear_PosDeseadas_pixels, P_plotear_PosDeseadas_m, 
                                       Imprimir_home, Imprimir_trayecto, Imprimir_final,
                                       Imprimir_Errores, Imprimir_Ganancias, Imprimir_AccionControl
                                       )
    
####MainCamara_DrawBot2D




def main():

    print("Selecciona un modo:")
    print("0) Calibrar ppr (Desarrollador)")
    print("1) Calibrar angulo (Desarrollador)")
    print("2) probar conexión motores (Desarrollador)")
    print("3) Modo Libre (Desarrollador)")
    print("4) Posicionar en angulos (Desarrollador)")
    print("5) Modo codigo custom (Desarrollador)")
    print("Modos drawbot:")
    print("6] Modo Imagen")
    print("7] Camara drawbot")
    print("8] SALIR")

    while True:
        try:
            MODO = int(input("Ingresa un numero para acceder a un modo: "))
            break#termina while de que no hubo error
        except ValueError:
            print("Ingresa valores validos porfa")
        ####
    ####
    

    #si selecciono algo de estos, activa modo con contra si es que hay
    if (MODO == 0 or MODO == 1 or MODO == 2 or MODO == 3 or MODO == 4 or MODO == 5):
        if CodeProteccion.contrasena() == False:
            return #se sale del código
        ####
    ##modos

    print("-------------------------------------------")
    if MODO==0: #CALIBRAR PPR
        CodeMotores.Main_ppr() #dev modo
    elif MODO == 1: #CALIBRAR ANGULO
        CodeMotores.Main_calibracion() #dev modo
    elif MODO == 2: #PROBAR CONEXIONES
        CodeMotores.Main_ProbarMotores() #dev modo
    elif MODO == 3: #MODO LIBRE
        CodeMotores.MainLibre() #dev modo
    elif MODO == 4: #MODO posicionar
        CodeMotores.Main_Set_Grados() #dev modo
    elif MODO == 5: #Modo custom codigo
        CodePruebas.Main_Custom() #Dev modo

    ###MODOS YA PARA PROBAR EL ROBOT
    elif MODO == 5: #MODO IMAGEN
        MainImagen() #Modo de cargar imagen
    elif MODO == 6: #CAMARA DRAWBOT
        MainCamara_DrawBot2D()
    elif MODO == 7: #SALIRSE
        print("SALIENDO...")
    ####


    CodeMotores.cerrar_encoder()
    print("Finalizado")
####

main()

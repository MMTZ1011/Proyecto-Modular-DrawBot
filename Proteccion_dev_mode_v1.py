# CODIGO PARA LA RASPBERRY PI 
from configuracion_proyecto import contrasena_dev_mode, Proteger_con_contra



#pone una capa de seguridad para que ningun wey que pruebe el
# programa el dia de la exposicion acceda a las cosas de configuracion importantes
# como la calibracion de ppr, poner angulo 0
# entre otras cosas que no queremos que desconfiguren


def contrasena():
    if Proteger_con_contra == True:
        while True:
            try:
                texto = int(input("Ingresa contraseña para acceder: "))
                if isinstance(texto, str):
                    break
            except ValueError:
                print("Error: no se ingreso una cadena de texto")
            ####
        ####
        cadena_mini = texto.lower()
        if cadena_mini == contrasena_dev_mode:
            return True #se transforma en True
        else:
            print("contraseña incorrecta, saliendo de ejecución")
            return False #no da acceso
        ###if de contra

    else:
        return True #no hay proteccion
    #### de contra
    
#####
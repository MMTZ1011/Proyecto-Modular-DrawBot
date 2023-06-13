







######################CONFIGURACION PARA MOTORES

#Configuracion para motorpuenteH_para_2_v3
tsample= 0.005 #Tiempo para fors y whiles z
min_vel_saturacion = 6 #minimo velocidad
max_vel_saturacion = 100 #maximo velocidad

Ppr_Calibra = 20  #No editar almenos que sepas
################################################################

#Motor 1 (PUENTE H):
ENA = 18 #13#13 #PWM
IN1 = 14 #3#19
IN2 = 15 #4#26
# Motor 1 (ENCODER):
Enco_CA = 17
Enco_CB = 27
#Pulsos para este motor:
ppr_1 = 690 #690 esta perfecto
#calibracion:
A_vel_calibra = 15
A_ppr_calibra = Ppr_Calibra 
#Controlador para set_Angulo_new:
A_Kp_set_angle = 0.7


#Motor 2 (PUENTE H):
ENB = 13
IN3 = 5
IN4 = 6
# Motor 2 (ENCODER):
Enco_CC = 23
Enco_CD = 22
#Pulsos para este motor:
ppr_2 = 640 #este puede ser distinto
#calibracion:
B_vel_calibra = 15
B_ppr_calibra = Ppr_Calibra
#Controlador para set_Angulo_new:
B_Kp_set_angle = 0.3

#Para controlador de set angle para pos iniciales:
tolerancia_error = 3 #esta en degrados


import numpy as np
import math
import matplotlib.pyplot as plt
import time













'''
q: vector de dos elementos que representa las coordenadas angulares del brazo robot.
v: matriz de dos filas y n columnas que representa la trayectoria deseada a seguir por el brazo robot. Cada columna de v es una posición deseada del extremo del brazo robot en coordenadas cartesianas.
w: matriz de dos filas y tres columnas que representa las ganancias neuronales del controlador. Cada fila representa las ganancias correspondientes a un eslabón del brazo robot y cada columna representa una ganancia específica.
eta: matriz de dos filas y tres columnas que representa las tasas de aprendizaje para las ganancias del controlador. Cada fila representa las tasas correspondientes a un eslabón del brazo robot y cada columna representa una tasa específica.
alpha: factor de regulación para las ganancias neuronales del controlador.
dt: tiempo transcurrido entre cada iteración del bucle.
'''


def C_Posicionamiento(P_plotear, pos_inicio, a, q, w, eta, alpha, dt, rango_minimo):

    
    # V solo es un vector
    e_sum = 0
    # Listas vacías para almacenar la información en cada iteración del bucle
    theta_plot = [[],# lista de posiciones angulares
                  []] 
    q_plot = [[], # lista de posiciones cartesianas
              []] 
    qp_plot = [[], # lista de velocidades angulares
               []] 
    tau_plot = [[], # lista de las entradas en cada instante
                []] 
    e_plot = [[], # lista de errores en cada instante
              []] 
    w_1 = [[],[],[]] # lista de ganancias de la eslabón 1
    w_2 = [[],[],[]] # lista de ganancias de la eslabón 2

    q_inicial = []
    tiempo_0 =  0
    tiempo_1 =  1

    
    #plt.pause(0.1)
    # FUNCIONES:
    def J(q):  # Jacobiano t
        return np.array([[-a[0]*np.sin(q[0])-a[1]*np.sin(q[0]+q[1]), -a[1]*np.sin(q[0]+q[1])],
                         [a[0]*np.cos(q[0])+a[1]*np.cos(q[0]+q[1]), a[1]*np.cos(q[0]+q[1])]]).T
    def pos(q):  # Cinematica
        return np.array([a[0]*np.cos(q[0])+a[1]*np.cos(q[0]+q[1]),
                         a[0]*np.sin(q[0])+a[1]*np.sin(q[0]+q[1])])

    q_inicial = pos(q)
    tiempo_0 = time.time()

    v = pos_inicio.reshape(2,1)
    #print(v)

    #Calcula esto la primera vez:
    x_e = pos(q)  # Obtiene la posición actual (x, y) del extremo del brazo a partir de las coordenadas angulares (q)
    e = v - x_e  # Calcula el error como la diferencia entre la posición deseada (v) y la posición actual (x_e)

    while math.sqrt(e[0]**2 + e[1]**2) > rango_minimo:
        #print("Error 2do:", (math.sqrt(e[0]**2 + e[1]**2)) )

        x_e = pos(q)  # Obtiene la posición actual (x, y) del extremo del brazo a partir de las coordenadas angulares (q)
        e = v - x_e  # Calcula el error como la diferencia entre la posición deseada (v) y la posición actual (x_e)

        e_old = e  # Guarda el valor anterior del error
        e_sum = e_sum + e*dt  # Calcula la suma acumulada de los errores multiplicados por el tiempo transcurrido (dt)

        # Calculo de entrada
        tau = np.zeros(2)
        tau[0] = w[0,0]*e[0] + w[0,1]*e_sum[0] + w[0,2]*(e[0]-e_old[0])/dt
        tau[1] = w[1,0]*e[1] + w[1,1]*e_sum[1] + w[1,2]*(e[1]-e_old[1])/dt

        # Calculo de ganancia neuronal
        w[0,:] = w[0,:] + eta[0,:]*(e[0]*tau[0] - alpha*w[0,:]*tau[0]**2) #Pesos lineales
        w[1,:] = w[1,:] + eta[1,:]*(e[1]*tau[1] - alpha*w[1,:]*tau[1]**2) #Pesos angulares

        # Acotamiento inferior para que w nunca tenga algún número negativo
        for k in range(3):
            if w[0,k] < 0:
                w[0,k] = 0
            if w[1,k] < 0:
                w[1,k] = 0

        #   Resuelve
        qp = np.transpose( np.dot(J(q), np.transpose(tau)  )  )
        q = q + qp*dt # Nueva pos segundos_recorte_laser


        ##### Aca guarda los datos que obtuvo para plotear después:
        #print(q)
        theta_plot[0].append(q[0]) # pos angular x
        theta_plot[1].append(q[1]) # pos angular y

        qp_plot[0].append(qp[0]) # vel angular q puntito x
        qp_plot[1].append(qp[1]) # vel angular q puntito y

        q_plot[0].append(x_e[0]) # pos trayecto x
        q_plot[1].append(x_e[1]) # pos trayecto y
        
        tau_plot[0].append(tau[0]) # entrada x
        tau_plot[1].append(tau[1]) # entrada y

        e_plot[0].append(e[0]) # error x
        e_plot[1].append(e[1]) # error y
        
        w_1[0].append(w[0,0]) # Ganancia Kp esl 1 
        w_1[1].append(w[0,1]) # Ganancia Ki esl 1 
        w_1[2].append(w[0,2]) # Ganancia Kd esl 1 

        w_2[0].append(w[1,0]) # Ganancia Kp esl 2
        w_2[1].append(w[1,1]) # Ganancia Ki esl 2 
        w_2[2].append(w[1,2]) # Ganancia Kd esl 2 
        #w_2.append(w[1,:]) # ganancias esl 2

        ## aca grafica      
        #fig.canvas.draw()
        #fig.canvas.flush_events()
        
        ##end de while
    ##end del for
    tiempo_1 = time.time()

    ##hace unos arreglos exclusivos para python para que no salga algo de array
    theta_plot[0] = [elem.tolist()[0] for elem in theta_plot[0]]
    theta_plot[1] = [elem.tolist()[0] for elem in theta_plot[1]]

    qp_plot[0] = [elem.tolist()[0] for elem in qp_plot[0]]
    qp_plot[1] = [elem.tolist()[0] for elem in qp_plot[1]]

    q_plot[0] = [elem.tolist()[0] for elem in q_plot[0]]
    q_plot[1] = [elem.tolist()[0] for elem in q_plot[1]]
    
    # tau_plot Esta perfecto tal cual esta no requiere extraer el elemento list

    e_plot[0] = [elem.tolist()[0] for elem in e_plot[0]]
    e_plot[1] = [elem.tolist()[0] for elem in e_plot[1]]



    segundos_totales = tiempo_1 - tiempo_0 # para ver cuanto tiempo en segundos le tomo hacer esto
    linspace = np.linspace(0, segundos_totales, len(theta_plot[0]), dtype="float")
    # Desactivar modo interactivo y mostrar imagen final
    #plt.show()  # Muestra la imagen final

    #Lo que regresa
    return theta_plot, qp_plot, q_plot, tau_plot, e_plot, w_1, w_2, q_inicial, segundos_totales, linspace
    #print("Terminó de recorrer trayectorias la neurona")
###





#Esta es la que usa para replicar el dibujo.
def C_Trayectoria(P_plotear, v, a, q, w, eta, alpha, dt, rango_minimo):
    
    
    #v: pos deseadas lista
    #a: longitud de eslabones
    #q: angulos pos home al final
    #w: el w tipico
    #eta: capacidad de cambiar


    e_sum = 0
    # Listas vacías para almacenar la información en cada iteración del bucle
    theta_plot = [[],# lista de posiciones angulares
                  []] 
    q_plot = [[], # lista de posiciones cartesianas
              []] 
    qp_plot = [[], # lista de velocidades angulares
               []] 
    tau_plot = [[], # lista de las entradas en cada instante
                []] 
    e_plot = [[], # lista de errores en cada instante
              []] 
    w_1 = [[],[],[]] # lista de ganancias de la eslabón 1
    w_2 = [[],[],[]] # lista de ganancias de la eslabón 2

    q_inicial = []
    tiempo_0 =  0
    tiempo_1 =  1

    
    #plt.pause(0.1)
    # FUNCIONES:
    def J(q):  # Jacobiano t
        return np.array([[-a[0]*np.sin(q[0])-a[1]*np.sin(q[0]+q[1]), -a[1]*np.sin(q[0]+q[1])],
                         [a[0]*np.cos(q[0])+a[1]*np.cos(q[0]+q[1]), a[1]*np.cos(q[0]+q[1])]]).T
    def pos(q):  # Cinematica direecta
        return np.array([a[0]*np.cos(q[0])+a[1]*np.cos(q[0]+q[1]),
                         a[0]*np.sin(q[0])+a[1]*np.sin(q[0]+q[1])])

    q_inicial = pos(q)
    tiempo_0 = time.time()

    
    for i in range(1, len(v[0])): #Empieza desde 1
        #print('i:',i)

        #Calcula esto la primera vez:
        x_e = pos(q)  # Obtiene la posición actual (x, y) del extremo del brazo a partir de las coordenadas angulares (q)
        e = v[:,i].reshape(2,1) - x_e  # Calcula el error como la diferencia entre la posición deseada (v) y la posición actual (x_e)


        #while math.sqrt(e[0]**2 + e[1]**2) > rango_minimo:
        #for i in range(5): #cuantas veces repite

        #print("p_deseado:", i+1,"-", "Error 2do:", (math.sqrt(e[0]**2 + e[1]**2)) )

        x_e = pos(q)  # Obtiene la posición actual (x, y) del extremo del brazo a partir de las coordenadas angulares (q)
        e = v[:,i].reshape(2,1) - x_e  # Calcula el error como la diferencia entre la posición deseada (v) y la posición actual (x_e)

        e_old = e  # Guarda el valor anterior del error
        e_sum = e_sum + e*dt  # Calcula la suma acumulada de los errores multiplicados por el tiempo transcurrido (dt)

        # Calculo de entrada
        tau = np.zeros(2)
        tau[0] = w[0,0]*e[0] + w[0,1]*e_sum[0] + w[0,2]*(e[0]-e_old[0])/dt
        tau[1] = w[1,0]*e[1] + w[1,1]*e_sum[1] + w[1,2]*(e[1]-e_old[1])/dt

        # Calculo de ganancia neuronal
        w[0,:] = w[0,:] + eta[0,:]*(e[0]*tau[0] - alpha*w[0,:]*tau[0]**2) #Pesos lineales
        w[1,:] = w[1,:] + eta[1,:]*(e[1]*tau[1] - alpha*w[1,:]*tau[1]**2) #Pesos angulares

        # Acotamiento inferior para que w nunca tenga algún número negativo
        for k in range(3):
            if w[0,k] < 0:
                w[0,k] = 0
            if w[1,k] < 0:
                w[1,k] = 0


        #   Resuelve
        qp = np.transpose( np.dot(J(q), np.transpose(tau)  )  )
        q = q + qp*dt # Nueva pos segundos_recorte_laser


        ##### Aca guarda los datos que obtuvo para plotear después:
        #print(q)
        theta_plot[0].append(q[0]) # pos angular x
        theta_plot[1].append(q[1]) # pos angular y

        qp_plot[0].append(qp[0]) # vel angular q puntito x
        qp_plot[1].append(qp[1]) # vel angular q puntito y

        q_plot[0].append(x_e[0]) # pos trayecto x
        q_plot[1].append(x_e[1]) # pos trayecto y
        
        
        tau_plot[0].append(tau[0]) # entrada x
        tau_plot[1].append(tau[1]) # entrada y

        e_plot[0].append(e[0]) # error x
        e_plot[1].append(e[1]) # error y
        
        w_1[0].append(w[0,0]) # Ganancia Kp esl 1 
        w_1[1].append(w[0,1]) # Ganancia Ki esl 1 
        w_1[2].append(w[0,2]) # Ganancia Kd esl 1 

        w_2[0].append(w[1,0]) # Ganancia Kp esl 2
        w_2[1].append(w[1,1]) # Ganancia Ki esl 2 
        w_2[2].append(w[1,2]) # Ganancia Kd esl 2 
        #w_2.append(w[1,:]) # ganancias esl 2


        ## aca grafica      
        #fig.canvas.draw()
        #fig.canvas.flush_events()
        


        ##end de while
    ##end del for
    tiempo_1 = time.time()

    ##hace unos arreglos exclusivos para python para que no salga algo de array
    theta_plot[0] = [elem.tolist()[0] for elem in theta_plot[0]]
    theta_plot[1] = [elem.tolist()[0] for elem in theta_plot[1]]

    qp_plot[0] = [elem.tolist()[0] for elem in qp_plot[0]]
    qp_plot[1] = [elem.tolist()[0] for elem in qp_plot[1]]

    q_plot[0] = [elem.tolist()[0] for elem in q_plot[0]]
    q_plot[1] = [elem.tolist()[0] for elem in q_plot[1]]
    
    # tau_plot Esta perfecto tal cual esta no requiere extraer el elemento list
    #tau_plot[0] = [elem.tolist()[0] for elem in tau_plot[0]]
    #tau_plot[1] = [elem.tolist()[0] for elem in tau_plot[1]]

    e_plot[0] = [elem.tolist()[0] for elem in e_plot[0]]
    e_plot[1] = [elem.tolist()[0] for elem in e_plot[1]]

    #w_1 = [elem.tolist() for elem in w_1]


    segundos_totales = tiempo_1 - tiempo_0 # para ver cuanto tiempo en segundos le tomo hacer esto
    linspace = np.linspace(0, segundos_totales, len(theta_plot[0]), dtype="float")
    # Desactivar modo interactivo y mostrar imagen final
    #plt.show()  # Muestra la imagen final

    #Lo que regresa
    return theta_plot, qp_plot, q_plot, tau_plot, e_plot, w_1, w_2, q_inicial, segundos_totales, linspace
    #print("Terminó de recorrer trayectorias la neurona")
###
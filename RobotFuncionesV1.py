
import numpy as np



def pos(q,a):  # Cinematica direecta(q=angulos, a=eslabones)
    return np.array([a[0]*np.cos(q[0])+a[1]*np.cos(q[0]+q[1]) ,
                     a[0]*np.sin(q[0])+a[1]*np.sin(q[0]+q[1]) ])



import numpy as np

import quantum as qu


def super_dense_coding(a,b):
    q = qu.QuantumState(2,np.array([1/np.sqrt(2),0,0,1/np.sqrt(2)]),True)
 
    if a==1:
        q.apply_operation_to_qubit(qu.sza,0)
    if b==1:
        q.apply_operation_to_qubit(qu.szb,0)
     
    q.apply_operation(qu.cnot)
    q.apply_operation_to_qubit(qu.hadamard,0)
    return q.measure()

super_dense_coding(0,0)
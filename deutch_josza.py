import numpy as np

import quantum as qu

np.set_printoptions(precision=2,suppress=True)

def U(n, f):
    """Generate an oracle matrix based on the given function mapping."""
    # INSPIRED BY https://github.com/meownoid/quantum-python/blob/master/quantum.py
    
    num_qubits = n + 1
    U = np.zeros((2**num_qubits, 2**num_qubits)) # Start with a matrix of zeroes.

    # Quantum state looks like IN-IN-...-IN-ANCILLA
    for input_state in range(2**num_qubits): # For each possible input
        input_string = input_state >> 1 # remove ANCILLA
        output_qubit = (input_state & 1) ^ (f[input_string]) # remove IN, XOR with f(IN)
        output_state = (input_string << 1) + output_qubit # the full state, with new OUT
        U[input_state, output_state] = 1 # set that part of U to 1

    return U


def deutch_josza(f,n):
    sq = qu.QuantumState(1,np.array([1,0]),False)
    ancilla = qu.QuantumState(1,np.array([0,1]),False)
    qubits = []
    Uf = qu.QuantumOperation(U(n,f))
    for i in range(n-1):
        currQ = qu.QuantumState(1,np.matrix([1,0]),False)
        qubits.append(currQ)

    for q in qubits:
        sq =  qu.QuantumState.superpose_qubits(sq,q)
    sq =  qu.QuantumState.superpose_qubits(sq,ancilla)

    sq.apply_operation(qu.hadamard,whole=False)
    sq.apply_operation(Uf)

    sq.apply_operation(qu.hadamard, whole=False)
 
    measurement = sq.measure_partial(0)

    if(measurement[0]==0):
        return "balanced"
    
    return "constant"
  


deutch_josza(Uf1,2)
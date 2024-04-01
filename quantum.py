import numpy as np


def is_unitary(m):
    return np.allclose(np.eye(len(m)), m.dot(m.T.conj()))

class QuantumOperation:
    def __init__(self, operation_matrix):
        if not is_unitary(operation_matrix):
            raise Exception("Operations must be unitary")
        self.operation_matrix = operation_matrix

class QuantumState:
    def __init__(self, qubits_number, state, is_entangled):
        self.state = state
        self.qubits_number = qubits_number
        self.is_entangled = is_entangled
        
    def apply_operation(self,o:QuantumOperation,whole=True):
        self.state = self.state.flatten()
        if whole:
            self.state = np.dot(o.operation_matrix, self.state.T)
        else:
            op = QuantumOperation(o.operation_matrix)
            for i in range(0,self.qubits_number-1):
                op.operation_matrix = np.kron(op.operation_matrix,o.operation_matrix)
            self.state = np.dot(op.operation_matrix,self.state.T)
        self.state = self.state.flatten()

    def apply_operation_to_qubit(self,o:QuantumOperation,qubit:int):
        self.state = self.state.flatten()

        op = QuantumOperation(o.operation_matrix)
        for i in range(0,self.qubits_number-1):
            if i==qubit+1:
                op.operation_matrix = np.kron(op.operation_matrix,o.operation_matrix)
            else:
                op.operation_matrix = np.kron(op.operation_matrix,np.eye(2))

        self.state = np.dot(op.operation_matrix,self.state.T)
        self.state = self.state.flatten()

    def measure(self):
        s = [0] * len(self.state)
        for i in range( len(self.state)):
            s[i] = np.round(np.abs(np.power(self.state[i],2)))
        return s


    def measure_partial(self,q_index:int):
        s = self.measure()
        sp = [0] *2 
        for index, value in enumerate(s):
            # Convert the index to binary and get the bit at the qubit_index
 
            bit = (index >> (self.qubits_number -1 - q_index)) & 1

            # Add the square of the value to the corresponding element in the measurement array
            sp[bit] += value
        return sp
    
    @staticmethod
    def entangle_qubits(q1,q2):
        q = QuantumState(2, np.kron(q1.state,q2.state),True)
        q.apply_operation(hadamard)
        q.apply_operation(cnot,entangled=False)
        return q
    
    @staticmethod
    def superpose_qubits(q1,q2):
        q = QuantumState(q1.qubits_number+q2.qubits_number, np.array(np.kron(q1.state,q2.state)),True)
        q.state = q.state.flatten()
        return q



sza = QuantumOperation(np.array([ [1,0], [0,-1]]))
szb = QuantumOperation(np.array([ [0,1], [1,0]]))
cnot =  QuantumOperation(np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]]))
hadamard = QuantumOperation(np.array([[1/np.sqrt(2),1/np.sqrt(2)], [ 1/np.sqrt(2), -1/np.sqrt(2)] ]))


import numpy as np

import quantum as qu

q1 = qu.QuantumState(2,[1/2,0,-1j/2,1/np.sqrt(2)],False)
q = qu.QuantumState(3,[1/2,0,0,0,1/2,1/2,0,-1/2],False)


print(q1.measure())
print(q1.measure_partial(0))
print(q1.measure_partial(1))
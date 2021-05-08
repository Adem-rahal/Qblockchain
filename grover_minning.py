from qiskit.quantum_info import Operator
from qiskit import QuantumCircuit
import numpy as np
import matplotlib.pyplot as plt
import random

'''Here we are looking to build a minning algorithm that would give the 
advantage to quantum computers in our new blockchain. For this we implement a
Toy example using grover's algorithm on 6 qubit to find the solution to a hash 
problem to solve the PoW (proof of work) validation method on a blockchain.
We use a toy Hash exemple too to encrypt the entries with 2^6 possible 
encryption.
Note that this algorithm could also be used to attack current blockchains such 
as bitcoins, to "mine" quicker than the other miners.'''

#k is the targeted value that we want to equal or be under than (x <= k)
k=3

#The hash function is here to test the code it will be improved later
def hash_6(x):
    return x+1

def phase_oracle(n, k, name = 'Oracle'):
    
    # create a quantum circuit on n qubits
    qc = QuantumCircuit(n, name=name)
    oracle_matrix = np.identity(2**n)
    marked_elements_counter = 0
    #we distinguish the diffuser
    if k == -1:
        oracle_matrix[0,0] = -1
    
    else:
    #add the -1 phase to elements that's satisfy the mining challenge H(x) <= k
        
        for i in range(2**n):
            if hash_6(i) <= k:
                oracle_matrix[i, i] = -1
                marked_elements_counter+=1

    #convert your matrix (called oracle_matrix) into an operator
    qc.unitary(Operator(oracle_matrix), range(n))

    return [qc,marked_elements_counter]

def diffuser(n):
    
    # create a quantum circuit on n qubits
    qc = QuantumCircuit(n, name='Diffuser')
    
    # apply hadamard gates to all qubits
    qc.h(range(n))
    # call the phase oracle applied to the zero state
    qc.append(phase_oracle(n,-1)[0], range(n))
    # apply hadamard gates to all qubits
    qc.h(range(n))

    return qc

def Grover(n, k):
    
    # Create a quantum circuit on n qubits
    qc = QuantumCircuit(n, n)
    
    # Determine r using the number of marked elements
    r = int(np.floor(np.pi/4*np.sqrt(2**n/phase_oracle(n, k)[1])))
    print(f'{n} qubits, elements {phase_oracle(n, k)[1]} marked, {r} rounds')
    
    # step 1: apply Hadamard gates on all qubits
    qc.h(range(n))
    
    # step 2: apply r rounds of the phase oracle and the diffuser
    for _ in range(r):
        qc.append(phase_oracle(n, k)[0], range(n))
        qc.append(diffuser(n), range(n))
        
    # step 3: measure all qubits
    qc.measure(range(n), range(n))
 
    return qc

mycircuit = Grover(6, k)
mycircuit.draw()


from qiskit import Aer, execute
simulator = Aer.get_backend('qasm_simulator')
counts = execute(mycircuit, backend=simulator, shots=1000).result().get_counts(mycircuit)
from qiskit.visualization import plot_histogram
plot_histogram(counts)
plt.show()

'''We can conclude seing the results here that we have more than 99% of chance
of getting one of the right answers with this algorithm '''
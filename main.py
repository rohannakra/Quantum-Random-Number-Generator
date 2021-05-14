# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# #### imports

# %%
from qiskit import QuantumCircuit, assemble, Aer, execute
from qiskit.visualization import plot_bloch_multivector
from qiskit_textbook.tools import array_to_latex

# %% [markdown]
# #### create quantum circuit

# %%
# Get # of qubits for quantum circuit
def get_qubits():
    n = int(input('Chose how many qubits to include in the quantum circuit (limit: 5) -> '))
    
    if n > 6:
        get_qubits()
    else:
        return n

n_qubits = get_qubits()


qc = QuantumCircuit(n_qubits, n_qubits)

for i in range(n_qubits):
    qc.h(i)

qc.measure(range(n_qubits), range(n_qubits))

qobj = assemble(qc)

qc.draw(output='mpl')

# %% [markdown]
# #### run on simulator

# %%
simulator = Aer.get_backend('qasm_simulator')

result = execute(qc, simulator, shots=1, memory=True).result()
state = result.get_memory(qc)[0]

print('state ->', state)

statevectors = [
    [1, 0],
    [0, 1]
]

for i, qubit_state in enumerate(state):
    qc.initialize(statevectors[int(qubit_state)], i)

qc.draw()

qobj = assemble(qc)

# NOTE: The reason why we re-initialize the state as the result of the simulation
#       is so that we can represent that state on a bloch sphere.

simulator = Aer.get_backend('statevector_simulator')

job = simulator.run(qobj)
statevector = job.result().get_statevector()

plot_bloch_multivector(statevector)

# %% [markdown]
# #### convert state to decimal

# %%
def convert(state):

    decimal, exponent  = (0, 1)

    for bit in state:
        decimal += int(bit) * 2 ** -exponent
        exponent += 1
    
    # NOTE: In the above for loop, we are converting the state to a number between 0 and 1.

    return decimal

print("random number", convert(state))

# %% [markdown]
# #### visualize the statevector without bloch sphere

# %%
array_to_latex(statevector, pretext="statevector = ")

# NOTE: The statevector is the tensor product of the combined states of all the qubits.



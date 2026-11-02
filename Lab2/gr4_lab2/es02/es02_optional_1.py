from qiskit import QuantumCircuit, QuantumRegister
from qiskit.providers.basic_provider import BasicProvider

# Takahashi adder (https://arxiv.org/abs/0910.2530)
names = ["a0", "a1", "b0", "b1", "z"]

qc = QuantumCircuit(*[QuantumRegister(1, name) for name in names])

# inputs: A = 01, B = 11
qc.x(0)
qc.x(2)
qc.x(3)

qc.cx(1, 3)
qc.cx(1, 4)
qc.ccx(2, 0, 1)
qc.ccx(3, 1, 4)
qc.cx(1, 3)
qc.ccx(2, 0, 1)
qc.cx(0, 2)
qc.cx(1, 3)

print(qc.draw())

# Basic simulation
qc.measure_all()

backend = BasicProvider().get_backend("basic_simulator")
result = backend.run(qc).result()

print(result.get_counts())

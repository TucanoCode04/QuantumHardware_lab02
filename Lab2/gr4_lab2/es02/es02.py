from qiskit import QuantumCircuit, QuantumRegister

names = ["a0", "a1", "b0", "b1", "s0", "c1", "s1", "s2"]

qc = QuantumCircuit(*[QuantumRegister(1, name) for name in names])

# inputs: A = 01 (a1=0, a0=1), B = 11 (b1=1, b0=1)
qc.x(0)  # a0 = 1
qc.x(2)  # b0 = 1
qc.x(3)  # b1 = 1

# s0 = a0 xor b0
qc.cx(0, 4)
qc.cx(2, 4)

# c1 = a0 and b0
qc.ccx(0, 2, 5)

# s1 = c1 xor a1 xor b1
qc.cx(5, 6)
qc.cx(1, 6)
qc.cx(3, 6)

# s2 = a1*b1 xor a1*c1 xor b1*c1
qc.ccx(1, 3, 7)
qc.ccx(1, 5, 7)
qc.ccx(3, 5, 7)

print(qc.draw(plot_barriers=False))

from qiskit.providers.basic_provider import BasicProvider

# Basic simulation
qc.measure_all()

backend = BasicProvider().get_backend("basic_simulator")
result = backend.run(qc).result()

print(result.get_counts())

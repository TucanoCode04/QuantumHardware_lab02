from qiskit import QuantumCircuit, QuantumRegister, transpile
from qiskit.providers.basic_provider import BasicProvider

names = ["a0", "a1", "b0", "b1", "c0", "c1", "ab", "ac", "out"]

qc = QuantumCircuit(*[QuantumRegister(1, name) for name in names])

qc.h([0, 1, 2, 3, 4, 5])
qc.x(8)
qc.h(8)

for rotation in range(6):
    qc.barrier()
    # Oracle
    qc.x(2)
    qc.mcx([0, 1, 2, 3], 6)
    qc.x(2)
    qc.x(0)
    qc.mcx([0, 1, 2, 3], 6)
    qc.x(0)
    qc.x([0, 4, 5])
    qc.mcx([0, 1, 4, 5], 7)
    qc.x([0, 4, 5])
    qc.x([0, 1, 4])
    qc.mcx([0, 1, 4, 5], 7)
    qc.x([0, 1, 4])
    qc.cx(2, 4)
    qc.cx(3, 5)

    qc.mcx([4, 5, 6, 7], 8)

    # Uncompute
    qc.cx(3, 5)
    qc.cx(2, 4)
    qc.x([0, 1, 4])
    qc.mcx([0, 1, 4, 5], 7)
    qc.x([0, 1, 4])
    qc.x([0, 4, 5])
    qc.mcx([0, 1, 4, 5], 7)
    qc.x([0, 4, 5])
    qc.x(0)
    qc.mcx([0, 1, 2, 3], 6)
    qc.x(0)
    qc.x(2)
    qc.mcx([0, 1, 2, 3], 6)
    qc.x(2)

    qc.barrier()
    # Diffuser
    qc.h([0, 1, 2, 3, 4, 5])
    qc.x([0, 1, 2, 3, 4, 5])
    qc.h(5)
    qc.mcx([0, 1, 2, 3, 4], 5)
    qc.h(5)
    qc.x([0, 1, 2, 3, 4, 5])
    qc.h([0, 1, 2, 3, 4, 5])

qc.barrier()
qc.h(8)
qc.x(8)
qc.measure_all()

# Basic simulation
backend = BasicProvider().get_backend("basic_simulator")
result = backend.run(transpile(qc, backend)).result()

print(result.get_counts())

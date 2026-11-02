from qiskit import QuantumCircuit, QuantumRegister, transpile
from qiskit.providers.basic_provider import BasicProvider

names = ["a0", "a1", "b0", "b1", "c0", "c1",
         "ab0", "ab1", "bc0", "bc1", "bc2", "bc3", "bc", "ac0", "ac1", "out"]

qc = QuantumCircuit(*[QuantumRegister(1, name) for name in names])

qc.h([0, 1, 2, 3, 4, 5])
qc.x(15)
qc.h(15)

for rotation in range(6):
    qc.barrier()
    # Oracle
    qc.x(2)
    qc.mcx([0, 1, 2, 3], 6)
    qc.x(2)
    qc.x(0)
    qc.mcx([0, 1, 2, 3], 7)
    qc.x(0)
    qc.ccx(2, 4, 8)
    qc.x([2, 4])
    qc.ccx(2, 4, 8)
    qc.x([2, 4])
    qc.ccx(3, 5, 9)
    qc.x([3, 4, 5])
    qc.mcx([3, 4, 5], 10)
    qc.x([3, 4, 5])
    qc.x([2, 3, 5])
    qc.mcx([2, 3, 5], 11)
    qc.x([2, 3, 5])
    qc.x([8, 9, 10, 11])
    qc.mcx([8, 9, 10, 11], 12)
    qc.x([8, 9, 10, 11])
    qc.x([0, 4, 5])
    qc.mcx([0, 1, 4, 5], 13)
    qc.x([0, 4, 5])
    qc.x([0, 1, 4])
    qc.mcx([0, 1, 4, 5], 14)
    qc.x([0, 1, 4])
    qc.cx(6, 7)
    qc.cx(13, 14)

    qc.mcx([7, 12, 14], 15)

    # Uncompute
    qc.cx(13, 14)
    qc.cx(6, 7)
    qc.x([0, 1, 4])
    qc.mcx([0, 1, 4, 5], 14)
    qc.x([0, 1, 4])
    qc.x([0, 4, 5])
    qc.mcx([0, 1, 4, 5], 13)
    qc.x([0, 4, 5])
    qc.x([8, 9, 10, 11])
    qc.mcx([8, 9, 10, 11], 12)
    qc.x([8, 9, 10, 11])
    qc.x([2, 3, 5])
    qc.mcx([2, 3, 5], 11)
    qc.x([2, 3, 5])
    qc.x([3, 4, 5])
    qc.mcx([3, 4, 5], 10)
    qc.x([3, 4, 5])
    qc.ccx(3, 5, 9)
    qc.x([2, 4])
    qc.ccx(2, 4, 8)
    qc.x([2, 4])
    qc.ccx(2, 4, 8)
    qc.x(0)
    qc.mcx([0, 1, 2, 3], 7)
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
qc.h(15)
qc.x(15)
qc.measure_all()

# Basic simulation
backend = BasicProvider().get_backend("basic_simulator")
result = backend.run(transpile(qc, backend)).result()

print(result.get_counts())

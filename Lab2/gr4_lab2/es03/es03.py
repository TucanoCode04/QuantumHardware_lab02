from qiskit import QuantumCircuit, QuantumRegister, transpile
from qiskit.providers.basic_provider import BasicProvider

names = ["a1", "a0", "b1", "b0", "s0", "s1", "s2"]

qc = QuantumCircuit(*[QuantumRegister(1, name) for name in names])

qc.h([0, 1, 2, 3])
qc.x(6)
qc.h(6)

qc.barrier()
# Oracle
qc.x(0)
qc.mcx([0, 1, 2, 3], 4)
qc.x(0)
qc.x(2)
qc.mcx([0, 1, 2, 3], 5)
qc.x(2)
qc.x([4, 5])
qc.ccx(4, 5, 6)
qc.x([4, 5])
qc.x(6)
qc.x(2)
qc.mcx([0, 1, 2, 3], 5)
qc.x(2)
qc.x(0)
qc.mcx([0, 1, 2, 3], 4)
qc.x(0)

qc.barrier()
# Diffuser
qc.h([0, 1, 2, 3])
qc.x([0, 1, 2, 3])
qc.h(3)
qc.mcx([0, 1, 2], 3)
qc.h(3)
qc.x([0, 1, 2, 3])
qc.h([0, 1, 2, 3])

qc.barrier()
# Oracle
qc.x(0)
qc.mcx([0, 1, 2, 3], 4)
qc.x(0)
qc.x(2)
qc.mcx([0, 1, 2, 3], 5)
qc.x(2)
qc.x([4, 5])
qc.ccx(4, 5, 6)
qc.x([4, 5])
qc.x(6)
qc.x(2)
qc.mcx([0, 1, 2, 3], 5)
qc.x(2)
qc.x(0)
qc.mcx([0, 1, 2, 3], 4)
qc.x(0)

qc.barrier()
# Diffuser
qc.h([0, 1, 2, 3])
qc.x([0, 1, 2, 3])
qc.h(3)
qc.mcx([0, 1, 2], 3)
qc.h(3)
qc.x([0, 1, 2, 3])
qc.h([0, 1, 2, 3])

qc.barrier()
qc.h(6)
qc.x(6)
qc.measure_all()

print(qc.draw(plot_barriers=False, fold=-1))

# Basic simulation
backend = BasicProvider().get_backend("basic_simulator")
result = backend.run(transpile(qc, backend)).result()

print(result.get_counts())

# Optional 3.1: only 3 ancillas (s0, s1, s2), so this also solves it

from qiskit import QuantumCircuit

qc = QuantumCircuit(2)

qc.h(0)
qc.h(1)
qc.cz(0, 1)
qc.h(0)
qc.h(1)
qc.x(0)
qc.x(1)
qc.cz(0, 1)
qc.x(0)
qc.x(1)
qc.h(0)
qc.h(1)

print(qc.draw())

from qiskit.quantum_info import Statevector

# Statevector simulation
statevector = Statevector(qc)
print(statevector)

from qiskit.providers.basic_provider import BasicProvider

# Basic simulation
qc.measure_all()

backend = BasicProvider().get_backend("basic_simulator")
result = backend.run(qc).result()

print(result.get_counts())

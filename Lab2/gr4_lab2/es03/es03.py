from math import asin, sin, sqrt, pi

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit.providers.basic_provider import BasicProvider

# Conditions: a + b = 4, a != b  ->  solutions (a, b) = (1, 3), (3, 1)
# Wire order as in the quirk circuit (es03.html): a = a1 a0, b = b1 b0 (MSB first)
names = ["a1", "a0", "b1", "b0", "s0", "s1", "s2"]
inputs = [0, 1, 2, 3]


def mcx_pattern(qc, controls, pattern, target):
    # X on target when the controls match pattern ("1" = filled dot, "0" = empty dot)
    zeros = [q for q, p in zip(controls, pattern) if p == "0"]
    if zeros:
        qc.x(zeros)
    qc.mcx(controls, target)
    if zeros:
        qc.x(zeros)


def oracle(qc):
    # s0: a = 01, b = 11
    mcx_pattern(qc, inputs, "0111", 4)
    # s1: a = 11, b = 01
    mcx_pattern(qc, inputs, "1101", 5)

    # s2 = s0 OR s1 (s2 is in |->, so the flip becomes a phase)
    mcx_pattern(qc, [4, 5], "00", 6)
    qc.x(6)

    # uncompute s0, s1
    mcx_pattern(qc, inputs, "1101", 5)
    mcx_pattern(qc, inputs, "0111", 4)


def diffuser(qc, qubits):
    qc.h(qubits)
    qc.x(qubits)
    qc.h(qubits[-1])
    qc.mcx(qubits[:-1], qubits[-1])
    qc.h(qubits[-1])
    qc.x(qubits)
    qc.h(qubits)


# Number of Grover rotations: N = 16 states, M = 2 solutions
N, M = 2 ** len(inputs), 2
theta = asin(sqrt(M / N))
rotations = round(pi / (4 * theta) - 1 / 2)
print(f"Grover rotations: {rotations} (success probability {sin((2 * rotations + 1) * theta) ** 2:.3f})")

c = ClassicalRegister(len(inputs), "c")
qc = QuantumCircuit(*[QuantumRegister(1, name) for name in names], c)

qc.h(inputs)
qc.x(6)
qc.h(6)

for _ in range(rotations):
    qc.barrier()
    oracle(qc)
    qc.barrier()
    diffuser(qc, inputs)

qc.barrier()
qc.measure(inputs, c)

print(qc.draw(plot_barriers=False, fold=-1))

# Basic simulation
backend = BasicProvider().get_backend("basic_simulator")
result = backend.run(transpile(qc, backend)).result()

counts = result.get_counts()
print(counts)

# Bitstrings are printed as c3 c2 c1 c0 = b0 b1 a0 a1
for key, n in sorted(counts.items(), key=lambda kv: -kv[1]):
    bits = key[::-1]
    a, b = int(bits[0:2], 2), int(bits[2:4], 2)
    print(f"a = {a}, b = {b}: {n}")

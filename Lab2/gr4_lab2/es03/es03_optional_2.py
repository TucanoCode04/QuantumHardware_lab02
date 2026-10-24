from math import asin, sin, sqrt, pi

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit.providers.basic_provider import BasicProvider

# Conditions: a + b = 5, b + c = 3, a + c = 2, a != b != c  ->  solution (a, b, c) = (2, 3, 0)
# Wire order as in the quirk circuit (es03_optional_2.html): x0 is the LSB of x
names = ["a0", "a1", "b0", "b1", "c0", "c1",
         "ab0", "ab1", "bc0", "bc1", "bc2", "bc3", "bc", "ac0", "ac1", "out"]
inputs = [0, 1, 2, 3, 4, 5]


def mcx_pattern(qc, controls, pattern, target):
    # X on target when the controls match pattern ("1" = filled dot, "0" = empty dot)
    zeros = [q for q, p in zip(controls, pattern) if p == "0"]
    if zeros:
        qc.x(zeros)
    qc.mcx(controls, target)
    if zeros:
        qc.x(zeros)


def conditions():
    qc = QuantumCircuit(len(names))

    # a + b = 5: (a, b) = (3, 2) -> ab0, (2, 3) -> ab1
    mcx_pattern(qc, [0, 1, 2, 3], "1101", 6)
    mcx_pattern(qc, [0, 1, 2, 3], "0111", 7)

    # b + c = 3: bc = NOR(bc0, bc1, bc2, bc3)
    # bc0 = (b0 == c0)
    mcx_pattern(qc, [2, 4], "11", 8)
    mcx_pattern(qc, [2, 4], "00", 8)
    # bc1 = b1 and c1
    mcx_pattern(qc, [3, 5], "11", 9)
    # bc2 = (b1 = 0, c = 0)
    mcx_pattern(qc, [3, 4, 5], "000", 10)
    # bc3 = (b = 0, c1 = 0)
    mcx_pattern(qc, [2, 3, 5], "000", 11)
    mcx_pattern(qc, [8, 9, 10, 11], "0000", 12)

    # a + c = 2 with a != c: (a, c) = (2, 0) -> ac0, (0, 2) -> ac1
    mcx_pattern(qc, [0, 1, 4, 5], "0100", 13)
    mcx_pattern(qc, [0, 1, 4, 5], "0001", 14)

    # The two cases of each sum are mutually exclusive: OR = XOR
    qc.cx(6, 7)    # ab1 = a + b = 5
    qc.cx(13, 14)  # ac1 = a + c = 2

    return qc


def oracle(qc):
    cond = conditions()
    qc.compose(cond, inplace=True)
    # out = (a + b = 5) AND (b + c = 3) AND (a + c = 2), out is in |->
    qc.mcx([7, 12, 14], 15)
    qc.compose(cond.inverse(), inplace=True)


def diffuser(qc, qubits):
    qc.h(qubits)
    qc.x(qubits)
    qc.h(qubits[-1])
    qc.mcx(qubits[:-1], qubits[-1])
    qc.h(qubits[-1])
    qc.x(qubits)
    qc.h(qubits)


# Number of Grover rotations: N = 64 states, M = 1 solution
N, M = 2 ** len(inputs), 1
theta = asin(sqrt(M / N))
rotations = round(pi / (4 * theta) - 1 / 2)
print(f"Grover rotations: {rotations} (success probability {sin((2 * rotations + 1) * theta) ** 2:.3f})")

c = ClassicalRegister(len(inputs), "c")
qc = QuantumCircuit(*[QuantumRegister(1, name) for name in names], c)

qc.h(inputs)
qc.x(15)
qc.h(15)

for _ in range(rotations):
    qc.barrier()
    oracle(qc)
    qc.barrier()
    diffuser(qc, inputs)

qc.barrier()
qc.measure(inputs, c)

# Basic simulation
backend = BasicProvider().get_backend("basic_simulator")
result = backend.run(transpile(qc, backend)).result()

counts = result.get_counts()
print(counts)

# Bitstrings are printed as c5 .. c0 = c1 c0 b1 b0 a1 a0
for key, n in sorted(counts.items(), key=lambda kv: -kv[1])[:5]:
    a, b, cc = int(key[4:6], 2), int(key[2:4], 2), int(key[0:2], 2)
    print(f"a = {a}, b = {b}, c = {cc}: {n}")

"""Shor's algorithm: factor 15 using quantum period finding.

The quantum part finds the period r of a^x mod N. Once you know r, the
factors fall out of a classical gcd. This is the algorithm that breaks RSA
-- at a scale far beyond today's hardware.

Run it standalone:  python -m workshop.examples.shor
"""

import argparse
from fractions import Fraction
from math import gcd

import numpy as np
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister

from .._cli import runner_or_exit
from ..session import get_runner

TITLE = "Shor's algorithm: factor 15"

#: Counting qubits. 3 is enough to resolve the period when N=15.
N_COUNT = 3


def c_amod15(a, power):
    """Controlled multiplication by a^power mod 15, as a gate.

    Hard-coded for N=15: each valid `a` permutes the four work qubits in a
    known way, so the modular arithmetic reduces to a pattern of swaps.
    """
    U = QuantumCircuit(4)
    for _ in range(power):
        if a in [2, 13]:
            U.swap(2, 3)
            U.swap(1, 2)
            U.swap(0, 1)
        if a in [7, 8]:
            U.swap(0, 1)
            U.swap(1, 2)
            U.swap(2, 3)
        if a in [4, 11]:
            U.swap(1, 3)
            U.swap(0, 2)
        if a in [7, 11, 13]:
            for q in range(4):
                U.x(q)
    g = U.to_gate()
    g.name = f'{a}^{power} mod 15'
    return g.control()


def iqft(n):
    """Inverse quantum Fourier transform on n qubits, as a gate.

    This is what turns the period hidden in the phases into something a
    measurement can actually read out.
    """
    qc = QuantumCircuit(n)
    for q in range(n // 2):
        qc.swap(q, n - 1 - q)
    for j in range(n):
        for m in range(j):
            qc.cp(-np.pi / 2 ** (j - m), m, j)
        qc.h(j)
    g = qc.to_gate()
    g.name = 'IQFT'
    return g


def build_circuit(a=7, n_count=N_COUNT):
    """The period-finding circuit: counting register + work register."""
    qc = QuantumCircuit(
        QuantumRegister(n_count, 'count'),
        QuantumRegister(4, 'work'),
        ClassicalRegister(n_count, 'meas'),
    )
    for q in range(n_count):
        qc.h(q)
    qc.x(n_count)  # work register starts at |1>
    for q in range(n_count):
        qc.append(c_amod15(a, 2 ** q), [q] + list(range(n_count, n_count + 4)))
    qc.append(iqft(n_count), range(n_count))
    qc.measure(range(n_count), range(n_count))
    return qc


def factors_from_counts(counts, N=15, a=7, n_count=N_COUNT):
    """Classical post-processing: measured phases -> period -> factors."""
    factors = set()
    for bits in sorted(counts, key=counts.get, reverse=True):
        phase = int(bits, 2) / 2 ** n_count
        r = Fraction(phase).limit_denominator(N).denominator
        if r % 2 == 0:
            for f in (gcd(a ** (r // 2) - 1, N), gcd(a ** (r // 2) + 1, N)):
                if f not in (1, N):
                    factors.add(f)
    return sorted(factors)


def run(runner=None, N=15, a=7, shots=1024):
    """Factor N with Shor's algorithm, printing what was measured.

    Uses the backend from the setup cell unless you pass one.
    """
    runner = runner or get_runner()
    counts = runner.run(build_circuit(a=a), shots=shots)
    print('Measured phases (raw counts):', counts)

    factors = factors_from_counts(counts, N=N, a=a)
    if factors:
        print(f'Factors of {N} found: {factors}')
    else:
        print('No non-trivial factor this time (noise/luck) - run again!')
    return factors


def main(argv=None):
    parser = argparse.ArgumentParser(description=TITLE)
    parser.add_argument('-N', type=int, default=15,
                        help='number to factor (the circuit is hard-coded for 15)')
    parser.add_argument('-a', type=int, default=7,
                        help='base for the modular exponentiation (default: 7)')
    parser.add_argument('--shots', type=int, default=1024,
                        help='how many measurements to take (default: 1024)')
    args = parser.parse_args(argv)
    run(runner_or_exit(), N=args.N, a=args.a, shots=args.shots)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

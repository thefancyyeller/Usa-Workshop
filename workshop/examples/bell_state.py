"""Bell state: two entangled qubits.

A Hadamard on the first qubit and a CNOT onto the second entangles them.
Measuring gives (almost) only 00 and 11 -- never 01 or 10. The qubits agree
every time, even though each one on its own is a 50/50 coin flip.

Run it standalone:  python -m workshop.examples.bell_state
"""

import argparse

from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister

from .._cli import runner_or_exit

TITLE = 'Bell state: entangled qubits'


def build_circuit():
    """Two qubits, entangled, both measured."""
    qc = QuantumCircuit(QuantumRegister(2), ClassicalRegister(2, 'meas'))
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])
    return qc


def run(runner, shots=1024):
    """Prepare and measure a Bell pair, printing the outcome counts."""
    counts = runner.run(build_circuit(), shots=shots)
    print('Counts:', counts)
    return counts


def main(argv=None):
    parser = argparse.ArgumentParser(description=TITLE)
    parser.add_argument('--shots', type=int, default=1024,
                        help='how many measurements to take (default: 1024)')
    args = parser.parse_args(argv)
    run(runner_or_exit(), shots=args.shots)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

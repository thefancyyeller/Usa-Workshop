"""Hello quantum: five coin flips.

One qubit is put into a 50/50 superposition with a Hadamard gate, then
measured. Each measurement collapses it to 0 or 1, at random.

Run it standalone:  python -m workshop.examples.coin_flips
"""

import argparse

from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister

from .._cli import runner_or_exit

TITLE = 'Hello quantum: five 50/50 qubit measurements'


def build_circuit():
    """One qubit, one Hadamard, one measurement."""
    qc = QuantumCircuit(QuantumRegister(1), ClassicalRegister(1, 'meas'))
    qc.h(0)
    qc.measure(0, 0)
    return qc


def run(runner, flips=5):
    """Flip the quantum coin `flips` times, printing each result."""
    # Note: on real hardware each loop iteration is a separate queued job.
    results = []
    for i in range(flips):
        counts = runner.run(build_circuit(), shots=1)
        outcome = list(counts)[0]
        results.append(outcome)
        print(f'Run {i + 1}: measured {outcome}')
    return results


def main(argv=None):
    parser = argparse.ArgumentParser(description=TITLE)
    parser.add_argument('--flips', type=int, default=5,
                        help='how many times to flip the coin (default: 5)')
    args = parser.parse_args(argv)
    run(runner_or_exit(), flips=args.flips)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

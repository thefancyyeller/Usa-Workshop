"""IBM Quantum Workshop.

The notebook's setup cell chooses where circuits run:

    from workshop import setup
    setup(USE_SIMULATOR, API_KEY, CRN)

after which the example cells build their own circuits and run them:

    from workshop import run_circuit
    counts = run_circuit(qc, shots=1024)
"""

from .runner import ConfigError, Runner, make_runner
from .session import get_runner, run_circuit, setup

__all__ = ['ConfigError', 'Runner', 'make_runner', 'get_runner', 'run_circuit', 'setup']

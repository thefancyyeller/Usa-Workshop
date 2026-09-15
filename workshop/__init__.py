"""IBM Quantum Workshop.

In the notebook, one setup cell picks the backend:

    from workshop import setup
    setup()

after which every example runs with no arguments:

    from workshop.examples import bell_state
    bell_state.run()

Each example is also runnable on its own from a terminal:

    python -m workshop.examples.bell_state
"""

from .runner import ConfigError, Runner, make_runner, runner_from_env
from .session import connect, get_runner, setup, use_simulator

__all__ = [
    'ConfigError', 'Runner', 'make_runner', 'runner_from_env',
    'connect', 'get_runner', 'setup', 'use_simulator',
]

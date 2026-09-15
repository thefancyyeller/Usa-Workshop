"""IBM Quantum Workshop.

Typical notebook use:

    from workshop import make_runner
    from workshop.examples import bell_state

    runner = make_runner(USE_SIMULATOR, API_KEY, CRN)
    bell_state.run(runner)

Each example is also runnable on its own from a terminal:

    python -m workshop.examples.bell_state
"""

from .runner import ConfigError, Runner, make_runner, runner_from_env

__all__ = ['ConfigError', 'Runner', 'make_runner', 'runner_from_env']

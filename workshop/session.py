"""The backend chosen in the notebook's setup cell.

The setup cell sets a few variables and calls setup(). That validates the
credentials and connects, so by the time you reach the examples you either
have a working backend or you have already seen what is wrong.

The connected backend is remembered here, which is why the examples can be
called with no arguments.
"""

from .runner import ConfigError, make_runner

_active = None


def get_runner():
    """The backend chosen in the setup cell."""
    if _active is None:
        raise RuntimeError(
            'No backend yet. Fill in the setup cell at the top of the '
            'notebook and run it.')
    return _active


def run_circuit(qc, shots=1024):
    """Run a circuit on the backend chosen in the setup cell."""
    return get_runner().run(qc, shots=shots)


def _activate(runner):
    global _active
    _active = runner
    return runner


def setup(use_simulator=True, api_key='', crn=''):
    """Choose where the examples run. Called from the notebook's setup cell.

    use_simulator=True  -> local simulator, no credentials needed
    use_simulator=False -> your IBM Quantum instance, using api_key and crn

    On bad credentials this prints what is wrong and leaves no active
    backend, so the examples say to fix the setup cell rather than quietly
    running somewhere you did not intend.
    """
    global _active
    _active = None
    try:
        _activate(make_runner(use_simulator, api_key, crn))
    except ConfigError as exc:
        # make_runner has already printed the specific problems.
        print(exc)

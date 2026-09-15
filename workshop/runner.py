"""Backend selection and circuit execution.

One place that knows how to talk to either the local simulator or real IBM
Quantum hardware, so the notebook's example cells don't have to care which
is in use.
"""

import logging
import warnings
from contextlib import contextmanager

from qiskit import transpile
from qiskit.transpiler import generate_preset_pass_manager

API_KEY_LENGTH = 44

#: Loggers that chat at WARNING level during a perfectly normal connection.
_NOISY_LOGGERS = ('qiskit', 'qiskit_ibm_runtime', 'qiskit_aer')


@contextmanager
def _quiet_setup():
    """Hide Qiskit's informational noise while connecting.

    Connecting with a token logs "Loading account with the given token" at
    WARNING level. Jupyter paints stderr red, so a normal connection looks
    like a failure. Errors still come through -- only WARNING and below are
    held back, and only for the duration of the connection.
    """
    saved = [(logging.getLogger(name), logging.getLogger(name).level)
             for name in _NOISY_LOGGERS]
    for logger, _ in saved:
        logger.setLevel(logging.ERROR)
    try:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', DeprecationWarning)
            warnings.simplefilter('ignore', UserWarning)
            yield
    finally:
        for logger, level in saved:
            logger.setLevel(level)


class ConfigError(RuntimeError):
    """Raised when the API key / CRN are missing or malformed."""


class Runner:
    """Runs circuits on whichever backend was selected.

    Don't build this directly -- use make_runner() or runner_from_env().
    """

    def __init__(self, backend, sampler_cls, use_simulator):
        self.backend = backend
        self.use_simulator = use_simulator
        self._sampler_cls = sampler_cls

    @property
    def description(self):
        if self.use_simulator:
            return 'local simulator'
        return f'{self.backend.name} ({self.backend.num_qubits} qubits)'

    def run(self, qc, shots=1024):
        """Transpile the circuit for this backend, run it, return counts."""
        if self.use_simulator:
            tqc = transpile(qc, self.backend)
            result = self._sampler_cls().run([tqc], shots=shots).result()
        else:
            pm = generate_preset_pass_manager(optimization_level=1, backend=self.backend)
            tqc = pm.run(qc)
            result = self._sampler_cls(mode=self.backend).run([tqc], shots=shots).result()
        return result[0].data.meas.get_counts()


def _check_credentials(api_key, crn):
    """Catch the common copy-paste mistakes before we try to connect."""
    problems = []

    if not api_key:
        problems.append('API_KEY is empty. Paste it into the SETUP cell.')
    elif len(api_key) != API_KEY_LENGTH:
        problems.append(f'API_KEY should be {API_KEY_LENGTH} characters (yours is '
                        f'{len(api_key)}). Copy it again from the dashboard.')

    if not crn:
        problems.append('CRN is empty. Paste it into the SETUP cell.')
    elif not crn.startswith('crn:'):
        problems.append('CRN should start with "crn:". Copy it from the Instances '
                        'page (hover the CRN, click copy).')

    if problems:
        for p in problems:
            print('PROBLEM:', p)
        raise ConfigError('Fix the problems above, then run this again.')


def _explain_connection_failure(error):
    """Turn a raw IBM Cloud error into something a beginner can act on."""
    msg = str(error)
    print('Could not connect. The error was:\n ', msg, '\n')
    low = msg.lower()

    if '401' in low or 'unauthorized' in low or ('invalid' in low and 'token' in low):
        print('HINT: Your API key looks wrong or was revoked. Create a new one on the dashboard.')
    elif 'crn' in low or 'instance' in low or 'not found' in low or '404' in low:
        print('HINT: Your CRN looks wrong, or the instance is in a different region.')
        print('      Open instances live in us-east: check the region switcher in the site header.')
    elif 'connection' in low or 'timeout' in low or 'resolve' in low:
        print('HINT: Network problem reaching IBM Cloud. Check your internet and retry.')
    else:
        print('HINT: Double-check both values. If it persists, create a fresh API key.')


def make_runner(use_simulator=True, api_key='', crn='', quiet=False):
    """Build a Runner for the local simulator or for real hardware.

    use_simulator=True  -> local Aer simulator, no credentials needed
    use_simulator=False -> least-busy real device on your IBM Quantum instance
    """
    if use_simulator:
        with _quiet_setup():
            from qiskit_aer import AerSimulator
            from qiskit_aer.primitives import SamplerV2 as Sampler

            runner = Runner(AerSimulator(), Sampler, use_simulator=True)
        if not quiet:
            print('Ready: local simulator')
        return runner

    api_key, crn = api_key.strip(), crn.strip()
    _check_credentials(api_key, crn)

    from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler

    try:
        with _quiet_setup():
            service = QiskitRuntimeService(
                channel='ibm_quantum_platform',
                token=api_key,
                instance=crn,
            )
            backend = service.least_busy(operational=True, simulator=False)
    except Exception as e:
        _explain_connection_failure(e)
        raise ConfigError('Fix the issue above, then try again.') from e

    runner = Runner(backend, Sampler, use_simulator=False)
    if not quiet:
        print('Connected. Running on real hardware:', runner.description)
    return runner

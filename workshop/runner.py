"""Backend selection and circuit execution.

One place that knows how to talk to either the local simulator or real IBM
Quantum hardware, so the example modules don't have to care which is in use.
"""

import os

from qiskit import transpile
from qiskit.transpiler import generate_preset_pass_manager

API_KEY_LENGTH = 44


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
        problems.append('API_KEY is empty. Set it in the CONFIG cell, or the '
                        'IBM_QUANTUM_API_KEY environment variable.')
    elif len(api_key) != API_KEY_LENGTH:
        problems.append(f'API_KEY should be {API_KEY_LENGTH} characters (yours is '
                        f'{len(api_key)}). Copy it again from the dashboard.')

    if not crn:
        problems.append('CRN is empty. Set it in the CONFIG cell, or the '
                        'IBM_QUANTUM_CRN environment variable.')
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


def runner_from_env(quiet=False):
    """Build a Runner from environment variables.

    Used when an example module is run as a script. Defaults to the simulator;
    set USE_SIMULATOR=false to reach for real hardware.

        USE_SIMULATOR        'false'/'0'/'no' to use real hardware (default: true)
        IBM_QUANTUM_API_KEY  your 44-character API key
        IBM_QUANTUM_CRN      your instance CRN
    """
    flag = os.environ.get('USE_SIMULATOR', 'true').strip().lower()
    use_simulator = flag not in ('false', '0', 'no')
    return make_runner(
        use_simulator=use_simulator,
        api_key=os.environ.get('IBM_QUANTUM_API_KEY', ''),
        crn=os.environ.get('IBM_QUANTUM_CRN', ''),
        quiet=quiet,
    )

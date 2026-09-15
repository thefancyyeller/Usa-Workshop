"""The workshop examples, one module each.

Every example module exposes the same three things:

    TITLE            a one-line description
    build_circuit()  the circuit, so you can draw or inspect it
    run(runner)      build it, run it, print the results

and can be run directly:  python -m workshop.examples.<name>

Submodules are imported lazily. Importing them here instead would make
`python -m workshop.examples.<name>` warn about a double import.
"""

import importlib

#: Example module names, in the order the workshop presents them.
NAMES = ('coin_flips', 'bell_state', 'shor')


def load(name):
    """Import one example module by its short name."""
    if name not in NAMES:
        raise KeyError(f'unknown example {name!r}; choose from {", ".join(NAMES)}')
    return importlib.import_module(f'{__name__}.{name}')


def load_all():
    """Import every example module, in presentation order."""
    return [load(name) for name in NAMES]


def __getattr__(name):
    """Allow `from workshop.examples import shor` style access without
    importing every example up front."""
    if name in NAMES:
        return load(name)
    raise AttributeError(f'module {__name__!r} has no attribute {name!r}')


__all__ = ['NAMES', 'load', 'load_all']

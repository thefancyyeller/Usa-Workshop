"""Run the examples from a terminal:

    python -m workshop              # list the examples
    python -m workshop bell_state   # run one
    python -m workshop --all        # run every example in order

Individual modules work too, and take their own options:

    python -m workshop.examples.shor --shots 2048
"""

import argparse

from ._cli import runner_or_exit
from .examples import NAMES, load, load_all


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog='python -m workshop',
        description='Run an IBM Quantum Workshop example.',
    )
    parser.add_argument('example', nargs='?', choices=NAMES, help='which example to run')
    parser.add_argument('--all', action='store_true', help='run every example in order')
    args = parser.parse_args(argv)

    if not args.example and not args.all:
        print('Examples:')
        for module in load_all():
            print(f'  {module.__name__.rsplit(".", 1)[-1]:<12} {module.TITLE}')
        print('\nRun one with:  python -m workshop <name>')
        return 0

    modules = load_all() if args.all else [load(args.example)]
    runner = runner_or_exit()
    for module in modules:
        print(f'\n=== {module.TITLE} ===')
        module.run(runner)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

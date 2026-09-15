"""Small helpers shared by the example modules' command-line entry points."""

from .runner import ConfigError, runner_from_env


def runner_or_exit():
    """Build a Runner from the environment, or print the problem and exit 1."""
    try:
        return runner_from_env()
    except ConfigError as exc:
        print(exc)
        raise SystemExit(1)

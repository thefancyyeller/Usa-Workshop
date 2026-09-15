"""The one setup step the notebook needs.

Renders a small form: pick the simulator or real hardware, enter credentials
if needed, click Connect. Credentials are validated at that point, so by the
time you reach the examples you either have a working backend or you have
already seen what is wrong.

The connected backend is remembered here, which is why the examples can be
called with no arguments.
"""

import io
from contextlib import redirect_stdout

from .runner import ConfigError, make_runner

_active = None


def get_runner():
    """The backend chosen in the setup cell."""
    if _active is None:
        raise RuntimeError(
            'No backend yet. Run the SETUP cell at the top of the notebook '
            '(and click Connect if you picked real hardware).')
    return _active


def _activate(runner):
    global _active
    _active = runner
    return runner


def use_simulator(quiet=False):
    """Switch to the local simulator."""
    return _activate(make_runner(use_simulator=True, quiet=quiet))


def connect(api_key, crn, quiet=False):
    """Switch to real hardware, validating the credentials first."""
    return _activate(make_runner(False, api_key, crn, quiet=quiet))


def _setup_without_widgets():
    """Fallback when ipywidgets isn't available: simulator, plus instructions."""
    print('(ipywidgets not available, so the picker cannot be shown)')
    print()
    runner = use_simulator()
    print()
    print('To use real hardware instead, run this in a new cell:')
    print('    from workshop import connect')
    print('    connect("<YOUR API KEY>", "<YOUR CRN>")')
    return runner


def setup():
    """Show the backend picker. Starts on the simulator, ready to go."""
    try:
        import ipywidgets as w
        from IPython.display import display
    except ImportError:
        return _setup_without_widgets()

    label_style = {'description_width': 'initial'}
    wide = w.Layout(width='min(100%, 34rem)')

    choice = w.RadioButtons(
        options=[('Local simulator — no account needed', 'sim'),
                 ('IBM Quantum — real hardware', 'hw')],
        value='sim',
        description='Run on:',
        style=label_style,
        layout=wide,
    )
    api_key = w.Password(description='API key:', placeholder='44-character key from your dashboard',
                         style=label_style, layout=wide)
    crn = w.Text(description='CRN:', placeholder='crn:v1:bluemix:...',
                 style=label_style, layout=wide)
    credentials = w.VBox([api_key, crn])
    credentials.layout.display = 'none'

    button = w.Button(description='Connect', button_style='primary', icon='play')
    status = w.Output()

    def show(text):
        """Replace the status area with `text`.

        Assigning to `outputs` rather than using `with status:` — the context
        manager routes output through the kernel's display channel, which is
        unreliable for output produced inside a button callback.
        """
        status.outputs = ()
        if text:
            status.append_stdout(text)

    def do_connect(_=None):
        # make_runner prints the specific problems it finds, so capture those
        # and put them in the status area instead of the cell output.
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            try:
                if choice.value == 'sim':
                    use_simulator(quiet=True)
                    print('Ready: local simulator')
                else:
                    runner = connect(api_key.value, crn.value, quiet=True)
                    print('Connected. Running on real hardware:', runner.description)
                print('You can now run the examples below.')
            except ConfigError as exc:
                print(exc)
            except Exception as exc:  # noqa: BLE001 - surface anything unexpected
                print('Unexpected error:', exc)
        show(buffer.getvalue())

    def on_choice(change):
        if change['new'] == 'hw':
            credentials.layout.display = 'flex'
            show('Enter your API key and CRN, then click Connect.\n')
        else:
            credentials.layout.display = 'none'
            do_connect()

    choice.observe(on_choice, names='value')
    button.on_click(do_connect)

    display(w.VBox([choice, credentials, button, status]))
    do_connect()  # the simulator is the default, so be ready immediately

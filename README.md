# IBM Quantum Workshop

Click the button below to launch your own private copy of this workshop.
No account or installation needed — just your IBM Quantum API key and CRN.

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/thefancyyeller/Usa-Workshop/HEAD?labpath=workshop.ipynb)

**Note:** Your session is temporary and private. It shuts down after ~10 minutes
of inactivity, and nothing you type is saved to this repository or visible to others.

## What's in here

```
workshop.ipynb    the workshop — setup cell, then three exercises
workshop/
  session.py      remembers the backend the setup cell chose
  runner.py       connects and runs circuits
requirements.txt  pinned Python packages
runtime.txt       Python version for Binder
```

The circuits live in the notebook itself, where attendees can see and edit them.
The `workshop/` package only handles the plumbing — picking a backend, validating
credentials, and running a circuit on whichever one is active:

```python
from workshop import run_circuit
counts = run_circuit(qc, shots=1024)
```

## The attendee flow

One setup cell, then everything else just runs:

1. Edit the variables at the top of the **SETUP** cell:

   ```python
   USE_SIMULATOR = True   # False to use your real IBM Quantum instance
   API_KEY = ""           # only needed when USE_SIMULATOR = False
   CRN = ""
   ```

2. Run that cell. For the simulator there is nothing to fill in at all.
3. Credentials are validated right there. A wrong-length key or a malformed CRN
   is reported in that cell, not three cells later — and a failed setup leaves no
   active backend, so the examples never quietly run somewhere you did not intend.
4. Run the exercises. Each one draws its circuit, runs it, and prints the results.

To switch backends, change the variables and run the setup cell again.

## The exercises

1. **Tilting a qubit** — an `ry` gate sets how likely a `1` is. Attendees pick the
   probability, see five single measurements come out differently, then measure the
   same circuit 2000 times and watch the bias they asked for appear.
2. **Entanglement** — a Bell pair: only `00` and `11`, never `01` or `10`.
3. **Shor's algorithm** — factoring 15 by quantum period finding.

Each example is a self-contained module with the same shape:

| Name | What it is |
| --- | --- |
| `TITLE` | one-line description |
| `build_circuit()` | the circuit, so you can draw or inspect it |
| `run()` | build it, run it, print the results |

The notebook is a thin wrapper over these — the setup cell chooses a backend, then
each cell calls `run()` on one example. Edits to the files under `workshop/` are
picked up by the notebook automatically (it enables `autoreload`), so attendees
can open a module, change a gate, and re-run the cell.

## For the presenter

1. **Pre-build the image.** Click the badge once ~30–60 min before the event.
   The first build takes several minutes; after that, launches take ~30s.
   Every push to this repo invalidates the cache, so pre-build *after* your
   last commit, not before.
2. **Share the link.** Give attendees the badge URL (or a shortened version):

   ```
   https://mybinder.org/v2/gh/thefancyyeller/Usa-Workshop/HEAD?labpath=workshop.ipynb
   ```

3. **Have a backup.** mybinder.org is a free, best-effort service and can be
   slow or at capacity. If it is down, attendees can run the notebook locally:

   ```bash
   pip install -r requirements.txt
   jupyter lab workshop.ipynb
   ```

## How the Binder environment is defined

Binder builds the image from two files in the repo root:

| File | Purpose |
| --- | --- |
| `requirements.txt` | Python packages, pinned so every attendee gets the same versions |
| `runtime.txt` | Python version (`python-3.11`) — Qiskit 2.x requires 3.10+ |

If you change either file, pre-build again before the event.

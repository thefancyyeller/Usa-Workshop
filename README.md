# IBM Quantum Workshop

A three-exercise introduction to Qiskit that runs in the browser with nothing to
install. Exercises run on a local simulator by default, or on real IBM Quantum
hardware given an API key and CRN.

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/thefancyyeller/Usa-Workshop/HEAD?labpath=workshop.ipynb)

**Note:** Binder sessions are temporary and private. They shut down after about ten
minutes of inactivity, and nothing typed into the notebook is saved to this
repository or visible to anyone else.

## What's in here

```
workshop.ipynb    setup cell, then three exercises
workshop/
  session.py      holds the backend the setup cell chose
  runner.py       connects and runs circuits
requirements.txt  pinned Python packages
runtime.txt       Python version for Binder
```

The circuits are written out in the notebook, so they can be read and edited there.
The `workshop/` package handles only the backend: selecting it, validating
credentials, and running a circuit against whichever one is active.

```python
from workshop import run_circuit
counts = run_circuit(qc, shots=1024)
```

## Running it

1. Edit the variables at the top of the SETUP cell:

   ```python
   USE_SIMULATOR = True   # False to use your real IBM Quantum instance
   API_KEY = ""           # only needed when USE_SIMULATOR = False
   CRN = ""
   ```

2. Run that cell. The simulator needs no credentials.
3. Credentials are checked as the cell runs, so a wrong-length key or a malformed
   CRN is reported there. A failed setup leaves no active backend, and the
   exercises say so rather than falling back to a previous one.
4. Run the exercises. Each draws its circuit, runs it and prints the results.

To change backend, edit the variables and run the setup cell again.

## The exercises

1. **Rotating a qubit.** An `ry` gate sets the probability of measuring a `1`, and
   that probability is a variable at the top of the cell. Five single-shot
   measurements are printed, then the same circuit is measured 2000 times and
   plotted.
2. **Entanglement.** A Bell pair: `00` and `11` only, never `01` or `10`.
3. **Shor's algorithm.** Factoring 15 by period finding.

## For the presenter

1. **Pre-build the image.** Open the badge link 30 to 60 minutes before the event.
   The first build takes several minutes; later launches take about 30 seconds.
   Every push invalidates the cache, so pre-build after your last commit.
2. **Share the link.** The badge URL, or a shortened version of it:

   ```
   https://mybinder.org/v2/gh/thefancyyeller/Usa-Workshop/HEAD?labpath=workshop.ipynb
   ```

3. **Have a fallback.** mybinder.org is free and best-effort, so it can be slow or
   at capacity. To run locally instead:

   ```bash
   pip install -r requirements.txt
   jupyter lab workshop.ipynb
   ```

## The Binder environment

Binder builds the image from two files in the repo root:

| File | Purpose |
| --- | --- |
| `requirements.txt` | Python packages, pinned so every attendee gets the same versions |
| `runtime.txt` | Python version (`python-3.11`). Qiskit 2.x requires 3.10 or later. |

Changing either one means pre-building again before the event.

# IBM Quantum Workshop

Click the button below to launch your own private copy of this workshop.
No account or installation needed — just your IBM Quantum API key and CRN.

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/thefancyyeller/Usa-Workshop/HEAD?labpath=workshop.ipynb)

**Note:** Your session is temporary and private. It shuts down after ~10 minutes
of inactivity, and nothing you type is saved to this repository or visible to others.

## What's in here

```
workshop.ipynb              the notebook attendees run
workshop/
  runner.py                 picks the backend (simulator or real hardware)
  examples/
    coin_flips.py           Example 1 — one qubit in superposition
    bell_state.py           Example 2 — two entangled qubits
    shor.py                 Example 3 — factoring 15
requirements.txt            pinned Python packages
runtime.txt                 Python version for Binder
```

Each example is a self-contained module with the same shape:

| Name | What it is |
| --- | --- |
| `TITLE` | one-line description |
| `build_circuit()` | the circuit, so you can draw or inspect it |
| `run(runner)` | build it, run it, print the results |

The notebook is a thin wrapper over these — it sets up a `runner`, then calls
`run()` on whichever example you want. Edits to the files under `workshop/` are
picked up by the notebook automatically (it enables `autoreload`), so attendees
can open a module, change a gate, and re-run the cell.

## Running from a terminal

The examples don't need the notebook:

```bash
python -m workshop                              # list the examples
python -m workshop bell_state                   # run one
python -m workshop --all                        # run all three
python -m workshop.examples.shor --shots 2048   # per-example options
```

These default to the local simulator. For real hardware:

```bash
export USE_SIMULATOR=false
export IBM_QUANTUM_API_KEY=...          # 44-character key from your dashboard
export IBM_QUANTUM_CRN=crn:v1:bluemix...
```

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

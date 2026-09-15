# IBM Quantum Workshop

Click the button below to launch your own private copy of this workshop.
No account or installation needed — just your IBM Quantum API key and CRN.

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/thefancyyeller/Usa-Workshop/HEAD?labpath=workshop.ipynb)

**Note:** Your session is temporary and private. It shuts down after ~10 minutes
of inactivity, and nothing you type is saved to this repository or visible to others.

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

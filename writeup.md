# Write-up — toy integrity study (QSec preparation)

Author: Khaoula EL MAJDOULI, Ph.D. candidate, UH2C / ESTC  
Repo: https://github.com/khaoula-elmajdouli/qsec-hybrid-pipeline-notes

## Threat model

A classical client trains an MLP, stores weights, and later scores new rows.
The same pattern exists in hybrid quantum workflows: an artifact is written,
moved, and reloaded before a backend run. Assets: training table, pickle file,
query interface, held-out metrics.

Adversary can overwrite the artifact, query the scorer, or contribute a few
training labels. Adversary cannot edit a clean evaluation set kept offline.

## Experiments

| ID | Vulnerability | Evidence the script prints | Mitigation implemented |
|---|---|---|---|
| T1 | Saved weights overwritten | Blind load accuracy drops; SHA-256 changes | `load_if_trusted()` refuses mismatch |
| T2 | Model extracted from labels only | Surrogate accuracy on the real test set | Measured; operational fix = query budget |
| T3 | 5% training labels flipped | Retrained model loses held-out accuracy | Frozen test set not visible to contributor |

## How to reproduce

```bash
pip install -r requirements.txt
python src/run_experiments.py
```

`outputs/summary.txt` stores the numbers. Seeds are fixed (`SEED = 42`).

## Scope

This is not a quantum-device exploit. It is a complete, local argument about
integrity, extraction, and poisoning — the three QSec themes I can study
honestly with the ML tools I already use for hydrogen-storage materials.

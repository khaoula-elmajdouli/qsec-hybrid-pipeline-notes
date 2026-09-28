# Hybrid pipeline integrity notes (QSec preparation)

**Author:** Khaoula EL MAJDOULI  
Ph.D. candidate in Physics, ESTC — Université Hassan II de Casablanca (UH2C), Morocco  
Thesis: AI-based predictive study of novel materials for hydrogen storage  

This repository is a small, reproducible study of **model and data integrity** in a classical ML pipeline. It is preparation for the [CSAW 2026 Quantum Security Challenge (QSec)](https://csaw.io/competition/quantum-security-challenge), which focuses on securing hybrid quantum–classical workflows (job/result integrity, adversarial inputs, model extraction, federated aggregation).

It is **not** a claim of prior quantum-hardware, Qiskit, or CTF experience.

## Why this maps to QSec

| Toy experiment here | QSec theme |
|---|---|
| Tamper with a saved model file | Cloud-job / result integrity; backdoored artifacts |
| Reconstruct a model from queries | Model extraction |
| Poison a small fraction of training rows | Adversarial inputs; poisoned aggregation |
| SHA-256 of the model file + held-out eval | Practical mitigation and reproducibility |

Same workflow I use in materials screening: train an ANN, freeze artifacts, evaluate, write down what broke.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python src/run_experiments.py
```

Expected output: metrics printed for the clean model, three attacks, and two mitigations. Artifacts land in `outputs/`.

## Repository layout

```
src/run_experiments.py   # all experiments, one file
src/threat_model.md      # threat model and mitigations
notebooks/01_overview.md # same story in notebook-style notes
requirements.txt
```

## What is intentionally out of scope

- No jobs on a real QPU or cloud quantum service
- No attacks against third-party infrastructure
- No unpublished flags or copied CTF write-ups

## License

MIT

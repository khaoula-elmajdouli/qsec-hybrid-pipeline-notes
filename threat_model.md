# Threat model (toy hybrid ML pipeline)

## System under study

A researcher trains a small ANN (or MLP) on tabular data, saves the weights, and later reloads them to score new samples. In a quantum / QML setting the same pattern appears: a classical client builds a circuit or a hybrid model, a compiler/runtime stores an artifact, a cloud backend executes it, and a classical script reads the result.

Assets: training data, saved model file, query API, evaluation metrics.

## Assumptions

- The training laptop is trusted at train time.
- The saved artifact may travel through shared storage or email.
- An adversary can read or overwrite the file, query a scoring endpoint, or contribute a few training rows (federated / multi-student lab setting).
- The adversary cannot break the OS of a clean machine that checks a hash before load.

## Three threats exercised in `run_experiments.py`

### T1 — Artifact integrity (weight tampering)

- **Action:** Flip a subset of saved parameters after training.
- **Impact:** Accuracy collapses or a silent backdoor appears while the file name stays the same.
- **QSec analogue:** Tampered compiler output, swapped job payload, poisoned checkpoint in a multi-tenant store.
- **Mitigation shown:** SHA-256 of the serialized model; refuse to load if the hash drifts.

### T2 — Model extraction

- **Action:** Query the clean model on a grid of inputs and train a surrogate.
- **Impact:** A stand-in model that copies behaviour without stealing the file.
- **QSec analogue:** Extraction of a QML model exposed as a cloud scoring API.
- **Mitigation shown:** This demo only measures the leak. Operational controls (rate limits, output rounding, watermarking) belong in a later iteration.

### T3 — Data poisoning

- **Action:** Flip labels on a small fraction of the training set and retrain.
- **Impact:** Held-out accuracy drops; the pipeline still “trains successfully”.
- **QSec analogue:** Poisoned clients in quantum federated learning; adversarial inputs at aggregation time.
- **Mitigation shown:** Keep a clean held-out set that attackers do not touch; compare against a baseline.

## Evidence standard (what QSec asks for)

For each experiment the script prints: setup, metric before/after, and a one-line mitigation. That is the same skeleton as a QSec write-up: threat model, vulnerability, exploit path, evidence, recommended fix.

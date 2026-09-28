#!/usr/bin/env python3
"""Toy integrity experiments for a small MLP pipeline.

Maps to QSec themes (artifact integrity, model extraction, poisoned training)
without using a quantum device.
"""

from __future__ import annotations

import hashlib
import pickle
from pathlib import Path

import numpy as np
from sklearn.datasets import make_classification
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)
SEED = 42


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def train_mlp(X, y, seed=SEED) -> MLPClassifier:
    clf = MLPClassifier(
        hidden_layer_sizes=(32,),
        max_iter=400,
        random_state=seed,
        verbose=False,
    )
    clf.fit(X, y)
    return clf


def dump_model(model, path: Path) -> bytes:
    blob = pickle.dumps(model)
    path.write_bytes(blob)
    return blob


def main() -> None:
    rng = np.random.default_rng(SEED)
    X, y = make_classification(
        n_samples=800,
        n_features=20,
        n_informative=8,
        n_redundant=4,
        random_state=SEED,
    )
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=SEED, stratify=y
    )

    print("=== Clean baseline ===")
    model = train_mlp(X_train, y_train)
    acc_clean = accuracy_score(y_test, model.predict(X_test))
    model_path = OUT / "model.pkl"
    blob = dump_model(model, model_path)
    digest = sha256_bytes(blob)
    (OUT / "model.sha256").write_text(digest + "\n")
    print(f"test accuracy: {acc_clean:.3f}")
    print(f"sha256:        {digest}")

    print("\n=== T1 Weight tampering ===")
    tampered = pickle.loads(blob)
    for i, coef in enumerate(tampered.coefs_):
        noise = rng.normal(0, 1.5, size=coef.shape)
        tampered.coefs_[i] = coef + noise
    acc_t1 = accuracy_score(y_test, tampered.predict(X_test))
    tampered_blob = pickle.dumps(tampered)
    tampered_digest = sha256_bytes(tampered_blob)
    print(f"accuracy after tamper: {acc_t1:.3f}")
    print(f"hash match:            {tampered_digest == digest}")
    print("mitigation: refuse load if sha256(file) != recorded digest")

    print("\n=== T2 Query-based extraction ===")
    X_query, _ = make_classification(
        n_samples=600,
        n_features=20,
        n_informative=8,
        n_redundant=4,
        random_state=0,
    )
    y_query = model.predict(X_query)
    surrogate = train_mlp(X_query, y_query, seed=0)
    acc_surrogate_on_teacher = accuracy_score(y_test, surrogate.predict(X_test))
    print(f"surrogate accuracy on real test set: {acc_surrogate_on_teacher:.3f}")
    print("mitigation (operational): rate-limit queries; do not expose raw scores")

    print("\n=== T3 Label poisoning ===")
    y_poison = y_train.copy()
    n_flip = max(1, int(0.05 * len(y_poison)))
    idx = rng.choice(len(y_poison), size=n_flip, replace=False)
    y_poison[idx] = 1 - y_poison[idx]
    poisoned = train_mlp(X_train, y_poison, seed=7)
    acc_t3 = accuracy_score(y_test, poisoned.predict(X_test))
    print(f"flipped labels:     {n_flip}/{len(y_poison)}")
    print(f"accuracy poisoned:  {acc_t3:.3f}")
    print("mitigation: keep a clean held-out set the contributor cannot edit")

    summary = OUT / "summary.txt"
    summary.write_text(
        "\n".join(
            [
                f"clean_accuracy={acc_clean:.4f}",
                f"tampered_accuracy={acc_t1:.4f}",
                f"hash_match={tampered_digest == digest}",
                f"surrogate_accuracy={acc_surrogate_on_teacher:.4f}",
                f"poisoned_accuracy={acc_t3:.4f}",
                f"sha256={digest}",
                "",
            ]
        )
    )
    print(f"\nWrote {summary}")


if __name__ == "__main__":
    main()

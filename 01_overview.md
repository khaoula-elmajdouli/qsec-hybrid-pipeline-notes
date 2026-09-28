# Overview notes

Run `python src/run_experiments.py` first. This page is the narrative.

## Clean baseline

Synthetic binary classification (20 features). MLP with one hidden layer. Fixed seed. Accuracy on a held-out test set is the reference number.

## Attack 1 — tamper the saved model

The trained weights are pickled, then a fraction of parameters is overwritten. Reloading the file is enough to destroy utility. Mitigation: store `sha256(model bytes)` next to the file and refuse a mismatch.

## Attack 2 — steal by asking questions

A surrogate MLP is trained only on labels returned by the clean model. If the query budget is large, the surrogate approaches the original accuracy. This is the integrity problem of an exposed scoring API, including a future QML endpoint.

## Attack 3 — poison a few labels

Five percent of training labels are flipped. Training still converges. Test accuracy falls. Mitigation: a frozen evaluation set and a recorded baseline.

## Link to hydrogen-storage work

The ANN pattern is the same one used for materials screening in the Ph.D.: collect table → preprocess → train → evaluate → write a short report. Here the “material property” is replaced by a security property of the artifact itself.

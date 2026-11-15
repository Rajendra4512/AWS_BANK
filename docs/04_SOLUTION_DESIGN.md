# Solution design

## End-to-end model lifecycle
1. Ingest: deterministic synthetic features amount, hour, velocity, merchant_risk, geo_distance. Public Kaggle credit-card dataset may be integrated later only after verifying license, mapping, and feature quality; anonymized PCA features do not match the current synthetic schema.
2. Validate: Pydantic enforces input bounds. Production requires schema versioning, null checks, data leakage tests and time-based splitting.
3. Train: standardized LogisticRegression with class balancing; stratified train/test split. Baseline seed 42; candidate artifact created.
4. Evaluate: precision, recall, F1, PR-AUC and fraud prevalence. Decision threshold 0.5 is illustrative, not business-optimal.
5. Register: candidate metadata stored in SQLite; optional MLflow metric logging. Versioned joblib file written.
6. Approve: admin explicitly promotes; old active version archived. Future dual-control maker/checker and approval evidence.
7. Serve: FastAPI loads active artifact and returns score and version; persistence stores the scored features (synthetic only).
8. Monitor: PSI on amount with fixed baseline bins and configurable alert threshold. Alert triggers **review**, not blind retraining.
9. Retrain: admin starts new candidate. A production trigger requires confirmed drift, fresh labels, minimum samples, and validation gate.
10. Roll back: promote earlier artifact; audit version change and confirm scoring behavior.

## Distinguish drift types
Covariate drift: input distribution changes; label not needed. Concept drift: relation between inputs and fraud changes; needs outcome labels. Prediction drift: scores change. Performance drift: precision/recall decline on labeled recent data. Current implementation only supports amount covariate PSI.

## Governance gates
Training data lineage → baseline/challenger comparison → cost-based threshold → independent validation → approval → staged release → monitoring → rollback. Never use auto-promotion on PSI alone. In a bank, decisions require model risk management and traceable human accountability.

## MLflow integration plan
Base container excludes MLflow to stay light. Optional `requirements-mlflow.txt` enables experiment logging via `AWS_BANK_ENABLE_MLFLOW=true` and local file URI. For real model registry: configure managed MLflow tracking server, experiment IDs, artifacts in S3, registry stages/aliases, RBAC, signed artifacts and rollback records. Existing local model version table remains authoritative for MVP; do not label it native MLflow registry.

## Evidently integration plan
Optional `requirements-evidently.txt` is a dependency starting point, not working adapter. Add drift report service with reference/current Pandas frames, chosen column mapping, reports persisted as artifacts, summary stored in DB and UI link. Gate via feature flag and memory test. Pin/test exact Evidently API version before enabling.

# MLflow experiment lifecycle

Training happens in app/main.py train(). It fits a scaled logistic regression baseline, calculates precision, recall, F1 and PR-AUC and stores a joblib artifact. Optional mlflow_log records run parameters and metrics to local MLflow tracking. The SQLite models table is a separate lightweight registry, NOT the MLflow Model Registry. To migrate: deploy a dedicated MLflow tracking server with artifact store and registry backend, register versions, attach validation evidence, and map approval events to aliases. Test candidate/active/rollback consistency before enabling automated promotion.

## Interview walkthrough

1. State the business problem and risk.
2. Trace the request from UI to API to persistence.
3. Explain baseline selection and alternatives.
4. Show the failure path and human approval.
5. Explain the production gap and validation plan.

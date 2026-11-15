# Learning Lab curriculum and authoring standard

## Each lesson must include
Problem statement → business example → simple explanation → technical theory → why this model/library was selected → alternatives and tradeoffs → architecture diagram → step-by-step request/data flow → actual source file/function → run-it-yourself exercise → expected output → failure modes → production controls → interview Q&A → references and further reading. Admin edits persist in SQLite. The source-grounded course map and capstone are in `docs/23_LEARNING_LAB_COURSE.md`; the database lessons remain editable starter content and do not claim completion of every exercise.

## Curriculum (planned lesson depth)
1. Fraud domain: imbalanced labels, delayed outcomes, cost of false alerts, leakage.
2. Feature engineering: time windows, velocity, categorical encoding, privacy.
3. Model selection: LogisticRegression vs RandomForest vs XGBoost vs neural nets; cost and explainability.
4. Training lifecycle: train/validation/test, stratification vs temporal splits, cross-validation.
5. Evaluation: confusion matrix, precision/recall, PR-AUC, calibration, cost matrix, threshold.
6. MLflow: experiment/run/artifact/parameter/metric, model registry and aliases.
7. Drift: PSI, KS, JS divergence, Evidently, concept drift, delayed labels.
8. Retraining: trigger policy, labels, champion/challenger, canary, rollback.
9. Governance: approval, model cards, audit, validation, regulatory controls.
10. AWS: ECR, ECS, ALB, RDS, S3, CloudWatch, Bedrock and IAM boundaries.
11. LLMOps: gateway, prompt/version registry, evaluation, grounding, LLM-as-judge caveats.
12. Agentic HITL: durable state, checkpoints, approval, resume and idempotency.
13. Incident exercises: false positive spike, drift alert, corrupted artifact, rollback.

## Concrete teaching example
When amount PSI crosses threshold: inspect `drift_check()` in `app/main.py`; understand why the reference distribution is generated with seed 42 and current with seed 99; review histogram quantile bins in `psi()`; compare shift=0 and shift=0.8; explain why alert ≠ model failure; propose a label-based backtest; train candidate and explicitly promote after review. Show what would differ at a bank with Kafka streams, feature store and independent validation.

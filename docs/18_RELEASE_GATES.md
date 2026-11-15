# Release gates and definition of done

## Functional
- Every visible action calls a real authenticated API and shows a result/error.
- Separate normal user and admin permissions, test 401/403, role enforcement and maker-checker.
- Synthetic dataset and credit/AML rules must never be presented as production banking decisions.
- Train → candidate → compare metrics → promote → score → detect drift → roll back, with evidence.
- Credit index is a heuristic, NOT probability of default. AML alerts are synthetic rules, NOT sanctions screening.
- Offline LLM answers and keyword evaluations are NOT foundation model inference or LLM-as-judge.

## Nonfunctional
- Test resident memory and CPU under 1 GB container cap with representative load, report peak RSS and OOM events.
- Scan dependencies and images; no embedded keys, no external network dependency for local operation.
- Verify fresh install, restart persistence, concurrency and backup/restore.
- Perform CSRF, session rotation, rate-limit, authorization, audit tampering and model artifact integrity testing before exposure beyond localhost.

## AWS production release blockers
- External SSO/MFA, CSRF defense, session hardening, WAF, ALB TLS, managed DB, S3 artifacts, secrets management, KMS, IAM, logging, alarms, DR, autoscaling and cloud cost budgets.
- Real Bedrock adapter with IAM and explicit provider allowlisting; LangGraph checkpoints, human approval and tool policy.
- MLflow tracking server/model registry and Evidently report adapter; verify artifact immutability and version lineage.
- Model validation, fairness assessment, regulatory and security review. This starter is not bank-certified.

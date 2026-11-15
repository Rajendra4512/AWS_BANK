# AML alert lifecycle

AML screening here uses simple transparent rules: large transfers, velocity, geography and customer tenure. Real AML requires customer due diligence, watchlists, sanctions controls, transaction monitoring, typology coverage, analyst casework, evidence preservation, and suspicious activity reporting governed by jurisdiction. POST /api/aml/screen creates a case; GET /api/cases lists; POST /api/cases/{id}/review requires a different admin identity from the requester. Compare deterministic rules to anomaly detection and supervised detection, and discuss alert fatigue and false positives.

## Interview walkthrough

1. State the business problem and risk.
2. Trace the request from UI to API to persistence.
3. Explain baseline selection and alternatives.
4. Show the failure path and human approval.
5. Explain the production gap and validation plan.

# Credit risk design

Credit models estimate probability of default (PD), loss given default (LGD), and exposure at default (EAD). This build implements a transparent risk index only, not a calibrated PD. Explain why labels, observation windows, rejected applicants, fairness, calibration, and out-of-time validation matter. Trace POST /api/credit/assess to app/domains.py credit(). In production: governed feature pipeline, independent validation, calibration, adverse-action explanations, periodic monitoring, and documented policy thresholds.

## Interview walkthrough

1. State the business problem and risk.
2. Trace the request from UI to API to persistence.
3. Explain baseline selection and alternatives.
4. Show the failure path and human approval.
5. Explain the production gap and validation plan.

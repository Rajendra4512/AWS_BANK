# Bank-grade deployment and risk controls

Separate educational controls from production claims. Current local app uses SQLite, session cookies, one-process CPU inference, local model artifacts, and a 1 GB memory cap. Production requires managed relational storage, object storage, strong IAM and SSO, CSRF protection, network isolation, secrets rotation, immutable audit, supply chain scanning, incident playbooks, backups, HA, regulatory review, encryption, capacity testing and a real CI/CD release gate. Never deploy the local starter as an internet-facing regulated bank service.

## Interview walkthrough

1. State the business problem and risk.
2. Trace the request from UI to API to persistence.
3. Explain baseline selection and alternatives.
4. Show the failure path and human approval.
5. Explain the production gap and validation plan.

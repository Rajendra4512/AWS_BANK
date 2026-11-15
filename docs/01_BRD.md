# Business requirements document (BRD)

## Business problem
Banking ML models degrade as behavior changes. Technical leaders must track training evidence, measure drift, control promotion, document approvals, and recover from bad deployments. Many demos stop at notebook accuracy and never demonstrate the operational lifecycle.

## Product vision
AWS_BANK provides a working, local-first operations console with a migration path to AWS, and a code-linked learning lab for AI TPM and architecture interviews. It must be understandable to new engineers while retaining realistic operational governance.

## Stakeholders
Model developer (trains candidate), model risk officer (reviews evidence), operator (monitors), tenant administrator (access and lifecycle), learner (studies workflows), platform/SRE (deploys). MVP collapses model developer and approver into admin; **this is a documented control gap**.

## Objectives and success measures
- A fresh installation can train, register, approve, score, monitor and roll back without internet or proprietary data.
- All privileged changes generate audit events.
- Normal users cannot call privileged endpoints or see the admin console.
- Local deployment stays within configured 1 GB memory during normal use; verify peak training memory on target hardware.
- A new learner can trace every workflow to an API and implementation.

## Out of scope for MVP
Real customer transactions, live payment network integrations, regulated credit decisions, automated deployment without human approval, production-grade model risk compliance, multi-tenant data isolation, cloud deployment already completed, and actual LLM agent execution.

## Key risks
Class imbalance, label delay, concept vs covariate drift confusion, synthetic-real gap, model artifact trust, privileged account compromise, memory pressure, AWS cost, data residency and retention. Owners: ML lead for statistical risks, security lead for access, SRE for infrastructure.

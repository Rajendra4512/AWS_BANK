# Agentic workflow and human-in-the-loop

A real LangGraph-style workflow has explicit state, nodes, edges, checkpoint persistence, retry policy, and human interrupts. This application implements a simple persistent maker-checker case review, not a LangGraph agent. Study POST /api/cases/{id}/review and the separate requester/reviewer guard. Production agents must use allowlisted tools, scoped credentials, idempotency keys, durable checkpoints, expiry, escalation and rollback; high-risk external actions must not execute until approved.

## Interview walkthrough

1. State the business problem and risk.
2. Trace the request from UI to API to persistence.
3. Explain baseline selection and alternatives.
4. Show the failure path and human approval.
5. Explain the production gap and validation plan.

# LLMOps gateway, grounding and evaluation

The gateway uses curated offline responses: POST /api/llm/query. It is NOT an LLM and does not call Bedrock. The local implementation exposes validated runtime settings, prompt versioning and request telemetry; POST /api/admin/evals/run also executes bounded ML, RAG, agent/HITL and security checks, but is NOT an LLM-as-judge evaluation. Production gateway architecture still requires IAM auth, secret rotation, input/output filtering, PII handling, external grounding controls and approved provider adapters. Bedrock is model inference; ECS hosts the API. Add external adapters only after approval and integration testing.

## Interview walkthrough

1. State the business problem and risk.
2. Trace the request from UI to API to persistence.
3. Explain baseline selection and alternatives.
4. Show the failure path and human approval.
5. Explain the production gap and validation plan.

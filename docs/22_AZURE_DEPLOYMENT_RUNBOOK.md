# Azure deployment runbook — provisioned design, NOT executed

## Target architecture

ACR immutable image → Azure Container Apps in an internal environment → HTTPS ingress/WAF boundary → Azure Database for PostgreSQL Flexible Server. Store model artifacts in encrypted Blob Storage, secrets in Key Vault, identities through Managed Identity/Entra ID, and telemetry in Azure Monitor/Application Insights. Azure OpenAI or another approved provider is optional inference only; it is not the FastAPI host.

## Required placeholders

```text
AZURE_SUBSCRIPTION_ID=<approved subscription>
AZURE_RESOURCE_GROUP=<approved resource group>
AZURE_REGION=<approved region>
ACR_NAME=<globally unique registry>
CONTAINER_APP_ENV=<managed environment>
CONTAINER_APP_NAME=<service name>
POSTGRES_SERVER=<private database server>
BLOB_ACCOUNT=<encrypted artifact account>
KEY_VAULT=<secret store>
MANAGED_IDENTITY=<runtime identity>
```

Keep values in the approved deployment system; never commit credentials, connection strings or production URLs.

## Preconditions

1. Obtain subscription, region, cost, residency and deployment approval with MFA and a restricted federated deployment identity.
2. Complete SQLite-to-PostgreSQL migration design, additive backfill checks, rollback and restore rehearsal before creating more than one application replica.
3. Add the configurable Blob artifact adapter and checksum/signature validation. Local `/srv/artifacts` is not a production artifact store.
4. Review Managed Identity permissions for ACR pull, Blob prefix access, Key Vault secret read, PostgreSQL connectivity and Monitor telemetry. Deny broad Contributor access to the runtime identity.
5. Review IaC plan for private networking, ingress, firewall rules, PostgreSQL, Blob encryption, Key Vault, diagnostic settings, budgets and alerts. Do not apply without approval.

## Release sequence (examples only; not executed)

1. Run compile, focused financial-integrity tests, full CI tests, Auto Evals, security checks and container health verification.
2. Build and scan the immutable image, push to ACR with a content-addressed release tag, and record the digest.
3. Apply the reviewed database migration as a controlled job; record checksums and a restore checkpoint.
4. Deploy one revision with internal ingress and `/api/health` readiness/liveness probes. Keep the previous revision available for rollback.
5. Verify synthetic login/RBAC, transfer idempotency and ownership, statements, audit events, model quality-gate blocking, RAG citations/abstention and resource limits.
6. Shift traffic only after error rate, latency, memory, replica health and audit checks pass.

## Rollback and recovery

- Route traffic back to the previous Container Apps revision and retain the failed revision/logs for investigation.
- Revert only reviewed reversible database migrations; restore PostgreSQL from tested point-in-time/snapshot procedures if needed.
- Restore model artifacts by version/checksum from Blob Storage and revalidate evaluation evidence before scoring.
- Preserve Monitor, audit and deployment evidence; do not delete incident resources before retention review.

## Security, cost and cleanup

Enforce HTTPS, Entra/SSO/MFA, secure cookies, CSRF strategy, private PostgreSQL access, Key Vault rotation, encryption, diagnostic retention, WAF policy and least privilege. Set Azure Budgets before provisioning and estimate Container Apps replicas, PostgreSQL tier, registry, Blob, Monitor logs, networking and optional model-inference tokens. Cleanup must be an approved change that retains required backups/logs and confirms no orphaned public IPs, disks, registries or storage accounts.

No Azure resources, credentials or cloud commands were used for this repository validation.

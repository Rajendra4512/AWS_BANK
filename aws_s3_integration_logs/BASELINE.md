# Floci S3 artifact storage baseline — 2026-11-16

- Repository: `AWS_BANK_git_sync`.
- Branch: `feature/floci-s3-artifact-storage`.
- Preconditions: elevated read-only Git check confirmed `## feature/floci-s3-artifact-storage...origin/main`, pre-existing `M requirements.txt`, and untracked `wheel-verification/`.
- Preserved pre-existing changes: `requirements.txt` adds `boto3==1.44.3`; `wheel-verification/` contains the offline dependency wheels.
- Relevant baseline: `ArtifactStore` was local-only; `main.py` and `domains.py` already called `ArtifactStore(ART)` / `ArtifactStore(Path(...))`, providing the shared configuration seam.
- Safety: original `AWS_BANK` directory was not edited; no Docker command started or restarted a container; no cloud resource or real credential was used.

# CI baseline — 2026-11-16

- Worktree: `C:\Users\raj45\OneDrive\Desktop\AWS_BANK_project\AWS_BANK_git_sync`.
- Branch: `feature/floci-s3-artifact-storage`.
- Remote: `https://github.com/Rajendra4512/AWS_BANK.git`.
- Existing changes preserved; no commit, push, merge, deployment, or original `AWS_BANK` directory access.
- Workflow inventory: `.github/workflows/ci.yml` only.
- Workflow gates: dependency install, compile, PowerShell security scan, pip check, banking test, full pytest, Compose config, offline Docker build.
- `gh` version 2.103.3 is installed, but `gh auth status` reports no GitHub login and no `GH_TOKEN` is available; remote run logs could not be retrieved.
- Existing Docker resources were inspected only; `aws-bank-app` and Floci remained running and unchanged.

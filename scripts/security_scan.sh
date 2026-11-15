#!/usr/bin/env bash
set -euo pipefail

# Bounded source scan. Secrets are injected through the environment; this gate
# deliberately excludes .env, generated logs, artifacts and documentation.
if rg -n --hidden --glob 'app/**' --glob 'compose.yaml' --glob '.github/**' --glob 'scripts/**' \
  -e 'AKIA[0-9A-Z]{16}' \
  -e '-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----' \
  -e '(AWS_SECRET_ACCESS_KEY|AWS_SESSION_TOKEN)\s*=\s*["'"'][^"'"']+["'"']' .; then
  echo 'SECURITY_SCAN_FAIL: embedded credential pattern found' >&2
  exit 1
fi

echo 'SECURITY_SCAN_PASS: no high-risk embedded credential patterns found'

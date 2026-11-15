#!/usr/bin/env sh
set -eu
[ -f .env ] || { echo 'Create .env first'; exit 1; }
if command -v pwsh >/dev/null 2>&1; then pwsh -NoProfile -File scripts/security_scan.ps1; else sh scripts/security_scan.sh; fi
python -m pip check
docker compose -p aws_bank config --quiet
docker compose -p aws_bank up --build -d aws-bank
curl -fsS http://127.0.0.1:7005/api/health
curl -fsS http://127.0.0.1:7005/api/ready

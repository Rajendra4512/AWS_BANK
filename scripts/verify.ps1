$ErrorActionPreference = 'Stop'
Write-Host 'AWS_BANK safe preflight'
if (-not (Test-Path '.env')) { throw 'Copy .env.example to .env and set secrets' }
pwsh -NoProfile -File scripts/security_scan.ps1
if ($LASTEXITCODE -ne 0) { throw 'Security scan failed' }
python -m pip check
if ($LASTEXITCODE -ne 0) { throw 'Dependency check failed' }
docker compose -p aws_bank config --quiet
if ($LASTEXITCODE -ne 0) { throw 'Compose validation failed' }
Write-Host 'No other containers will be modified by this script.'
docker compose -p aws_bank up --build -d aws-bank
if ($LASTEXITCODE -ne 0) { throw 'Build/start failed' }
Invoke-RestMethod http://localhost:7005/api/health
Invoke-RestMethod http://localhost:7005/api/ready
Write-Host 'Review logs: docker compose -p aws_bank logs --tail=100 aws-bank'

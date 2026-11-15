$ErrorActionPreference = 'Stop'

# Bounded source scan. Secrets are injected through the environment; this gate
# deliberately excludes .env, generated logs, artifacts and documentation.
$hits = & rg -n --hidden --glob 'app/**' --glob 'compose.yaml' --glob '.github/**' --glob 'scripts/**' `
  -e 'AKIA[0-9A-Z]{16}' `
  -e '-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----' `
  -e 'AWS_SECRET_ACCESS_KEY\s*=' `
  -e 'AWS_SESSION_TOKEN\s*=' . 2>$null
if ($LASTEXITCODE -eq 0 -and $hits) {
  throw 'SECURITY_SCAN_FAIL: embedded credential pattern found'
}
Write-Output 'SECURITY_SCAN_PASS: no high-risk embedded credential patterns found'

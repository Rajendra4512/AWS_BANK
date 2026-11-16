# Stage 19: READ-ONLY AWS preflight and local plan generation. NO APPLY.
# Note: Terraform plan may acquire a transient remote backend state lock.
$ErrorActionPreference = 'Stop'
$Repo = 'C:\Users\raj45\OneDrive\Desktop\AWS_BANK_project\AWS_BANK_git_sync'
$Infra = Join-Path $Repo 'infra\aws'
$LogDir = Join-Path $Repo 'deployment_logs\stage19_preflight'
$ExpectedAccount = '213473482400'
$Region = 'ap-southeast-2'
if (!(Test-Path $Infra)) { throw "Missing Terraform directory: $Infra" }
New-Item -ItemType Directory -Path $LogDir -Force | Out-Null
$report = New-Object 'System.Collections.Generic.List[string]'
function Check-Exit([string]$Name) { if ($LASTEXITCODE -ne 0) { throw "$Name failed (exit $LASTEXITCODE)" } }
function Record([string]$Message) { $report.Add($Message); Write-Host $Message }
Set-Location $Repo
Record 'Stage 19 preflight — NO APPLY'
$IdentityJson = aws sts get-caller-identity --region $Region --output json
Check-Exit 'AWS identity'
$Identity = $IdentityJson | ConvertFrom-Json
if ([string]$Identity.Account -ne $ExpectedAccount) { throw "Unexpected account $($Identity.Account); STOP" }
Record "Account: $($Identity.Account); region explicitly set: $Region"
$GitBranch = git branch --show-current
Check-Exit 'Git branch'
Record "Git branch: $GitBranch"
$GitStatus = git status --porcelain
Check-Exit 'Git status'
Record "Git working tree entries: $(@($GitStatus).Count) (inspect locally; not printed)"
Set-Location $Infra
terraform fmt -check -recursive
Check-Exit 'Terraform formatting'
terraform validate
Check-Exit 'Terraform validation'
Record 'Terraform formatting and validation: PASS'
# A fresh normal-refresh plan is generated locally. NO terraform apply is run.
$PlanPath = Join-Path $LogDir 'terraform_stage19_review.tfplan'
terraform plan -input=false -out="$PlanPath"
Check-Exit 'Terraform refreshed plan'
$PlanJson = terraform show -json "$PlanPath"
Check-Exit 'Plan inspection'
$Plan = $PlanJson | ConvertFrom-Json
$changes = @($Plan.resource_changes | Where-Object { $_.change.actions -ne $null })
$create = @($changes | Where-Object { $_.change.actions -contains 'create' }).Count
$update = @($changes | Where-Object { $_.change.actions -contains 'update' }).Count
$delete = @($changes | Where-Object { $_.change.actions -contains 'delete' }).Count
Record "Plan: create=$create update=$update delete=$delete"
$hash = (Get-FileHash -LiteralPath $PlanPath -Algorithm SHA256).Hash
Record "Plan SHA256: $hash"
Record "Plan path (SENSITIVE; DO NOT COMMIT): $PlanPath"
Record 'Terraform apply: NOT EXECUTED'
if ($update -gt 0 -or $delete -gt 0 -or $create -ne 22) {
  Record 'DECISION: HOLD — differs from Stage 18 baseline; inspect before approval'
} else {
  Record 'DECISION: PLAN REVIEW REQUIRED — not approval to deploy'
}
$ReportPath = Join-Path $LogDir 'STAGE19_PREFLIGHT.txt'
$report | Set-Content -LiteralPath $ReportPath -Encoding UTF8
Write-Host "Report: $ReportPath"

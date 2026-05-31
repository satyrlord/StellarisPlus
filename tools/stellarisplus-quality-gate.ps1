[CmdletBinding()]
param(
	[string]$ModRoot = "."
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Parent $PSScriptRoot
$resolvedModRoot = (Resolve-Path -LiteralPath $ModRoot).Path
$failed = $false

Push-Location $repoRoot
try {
	Write-Host "Running Paradox validator..." -ForegroundColor Cyan
	& uv run .cursor/skills/stellaris-code-review/scripts/pdx_validate.py $resolvedModRoot
	if ($LASTEXITCODE -ne 0) {
		$failed = $true
	}

	Write-Host "Running Pyright..." -ForegroundColor Cyan
	& uvx --from pyright pyright --project pyrightconfig.json
	if ($LASTEXITCODE -ne 0) {
		$failed = $true
	}

	Write-Host "Running markdownlint..." -ForegroundColor Cyan
	& npx --yes markdownlint-cli2
	if ($LASTEXITCODE -ne 0) {
		$failed = $true
	}
}
finally {
	Pop-Location
}

if ($failed) {
	exit 1
}

exit 0
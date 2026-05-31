[CmdletBinding()]
param(
	[switch]$DryRun,
	[switch]$Check,
	[string]$CreditsPath = "credits.md"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Parent $PSScriptRoot
$scriptPath = Join-Path $PSScriptRoot 'stellarisplus-refresh-credits-dates.py'
$args = @($scriptPath, '--credits', $CreditsPath)
if ($DryRun) {
	$args += '--dry-run'
}
if ($Check) {
	$args += '--check'
}

Push-Location $repoRoot
try {
	if (Get-Command uv -ErrorAction SilentlyContinue) {
		& uv run @args
	}
	else {
		& python @args
	}
	exit $LASTEXITCODE
}
finally {
	Pop-Location
}

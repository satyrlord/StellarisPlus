[CmdletBinding()]
param(
	# Path to the Stellaris logs folder
	[string]$SourceLogsDir = "$env:USERPROFILE\Documents\Paradox Interactive\Stellaris\logs",

	# Path to the workspace inbox folder
	[string]$InboxDir,

	# Also copy exception.txt if present
	[switch]$IncludeException,

	# If set, do not launch Stellaris; only collect logs
	[switch]$NoLaunch
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$scriptDir = if ($PSScriptRoot) { $PSScriptRoot } elseif ($PSCommandPath) { Split-Path -Parent $PSCommandPath } else { $null }

if ([string]::IsNullOrWhiteSpace($InboxDir)) {
	$repoRoot = if ($scriptDir) { Split-Path -Parent $scriptDir } else { $null }
	if (-not $repoRoot) {
		throw 'Unable to resolve workspace root to compute InboxDir.'
	}
	$InboxDir = Join-Path $repoRoot 'help\_logs_inbox'
}

$logFiles = @(
	'debug.log',
	'error.log',
	'game.log',
	'setup.log',
	'system.log',
	'time.log'
)
if ($IncludeException) { $logFiles += 'exception.txt' }

$clipboardText = 'I have tested that your latest fix works as intended and copied the new logs to _logs_inbox. Analyze the logs the _log_inbox and check for any problems'

function Set-SystemClipboardText {
	param([Parameter(Mandatory=$true)][string]$Text)
	try {
		Set-Clipboard -Value $Text
		return $true
	} catch {
		# Fallback for shells without Set-Clipboard
		try {
			$Text | & clip.exe
			return $true
		} catch {
			return $false
		}
	}
}

# Ensure inbox exists
if (-not (Test-Path -LiteralPath $InboxDir)) {
	New-Item -ItemType Directory -Path $InboxDir -Force | Out-Null
}

Write-Host "Inbox:  $InboxDir" -ForegroundColor DarkCyan
Write-Host "Source: $SourceLogsDir" -ForegroundColor DarkCyan

# 1) Delete all logs from _logs_inbox
Get-ChildItem -LiteralPath $InboxDir -File -ErrorAction SilentlyContinue |
	Remove-Item -Force -ErrorAction SilentlyContinue

# 2) Launch sptest -Wait
if (-not $NoLaunch) {
	$testScript = Join-Path $scriptDir 'stellarisplus-test.ps1'
	if (-not (Test-Path -LiteralPath $testScript)) {
		throw "Missing test launcher script: $testScript"
	}

	Write-Host 'Launching test session (wait until exit)...' -ForegroundColor Cyan
	& $testScript -Wait
}

# 3) Copy new logs from Stellaris logs folder to _logs_inbox
if (-not (Test-Path -LiteralPath $SourceLogsDir)) {
	throw "Source logs directory not found: $SourceLogsDir"
}

foreach ($name in $logFiles) {
	$src = Join-Path $SourceLogsDir $name
	$dst = Join-Path $InboxDir $name
	if (Test-Path -LiteralPath $src) {
		Copy-Item -LiteralPath $src -Destination $dst -Force -ErrorAction SilentlyContinue
	}
}

# 4) Copy the requested text to clipboard
$clipboardOk = Set-SystemClipboardText -Text $clipboardText
if ($clipboardOk) {
	Write-Host 'Clipboard updated with confirmation text.' -ForegroundColor Green
} else {
	Write-Warning 'Failed to set clipboard text (Set-Clipboard and clip.exe both unavailable).'
}

Write-Host 'Collected logs:' -ForegroundColor Cyan
Get-ChildItem -LiteralPath $InboxDir -File |
	Sort-Object Name |
	Select-Object Name,Length,LastWriteTime |
	Format-Table -AutoSize

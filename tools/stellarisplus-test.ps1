[CmdletBinding()]
param(
	# Optional explicit path to stellaris.exe
	[string]$StellarisExe,

	# Disable -skiplauncher (default behavior is to use -skiplauncher)
	[switch]$NoSkipLauncher,

	# Wait for the game process to exit (useful if you want logs right after)
	[switch]$Wait,

	# Return the process object
	[switch]$PassThru
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Resolve-SteamPath {
	$steamReg = (Get-ItemProperty -Path 'HKCU:\Software\Valve\Steam' -ErrorAction SilentlyContinue).SteamPath
	if ($steamReg) {
		$steamReg = $steamReg -replace '/', '\\'
		$steamExe = Join-Path $steamReg 'steam.exe'
		if (Test-Path -LiteralPath $steamExe) { return $steamReg }
	}

	$default = 'C:\Program Files (x86)\Steam'
	if (Test-Path -LiteralPath (Join-Path $default 'steam.exe')) { return $default }

	return $null
}

function Resolve-StellarisExe {
	param([string]$ExplicitExe)

	if ($ExplicitExe) {
		if (Test-Path -LiteralPath $ExplicitExe) { return (Resolve-Path -LiteralPath $ExplicitExe).Path }
		throw "Stellaris exe not found at: $ExplicitExe"
	}

	# Common default path
	$defaultExe = 'C:\Program Files (x86)\Steam\steamapps\common\Stellaris\stellaris.exe'
	if (Test-Path -LiteralPath $defaultExe) { return $defaultExe }

	# Try to locate via SteamPath + libraryfolders.vdf
	$steamPath = Resolve-SteamPath
	if (-not $steamPath) { return $null }

	$libraryVdf = Join-Path $steamPath 'steamapps\libraryfolders.vdf'
	if (-not (Test-Path -LiteralPath $libraryVdf)) { return $null }

	# Minimal VDF parsing: find all quoted paths.
	$paths = @()
	foreach ($line in Get-Content -LiteralPath $libraryVdf -ErrorAction SilentlyContinue) {
		if ($line -match '"path"\s+"(?<p>[^"]+)"') {
			$paths += ($Matches.p -replace '/', '\\')
		}
	}
	$paths = $paths | Where-Object { $_ } | Select-Object -Unique
	
	foreach ($lib in $paths) {
		$candidate = Join-Path $lib 'steamapps\common\Stellaris\stellaris.exe'
		if (Test-Path -LiteralPath $candidate) { return $candidate }
	}

	return $null
}

$exe = Resolve-StellarisExe -ExplicitExe $StellarisExe
if (-not $exe) {
	throw 'Could not locate stellaris.exe. Pass -StellarisExe "C:\\Path\\To\\stellaris.exe".'
}

$workDir = Split-Path -Parent $exe
$launchArgs = @()
if (-not $NoSkipLauncher) { $launchArgs += '-skiplauncher' }

Write-Host "Launching Stellaris: $exe" -ForegroundColor Cyan
Write-Host "Working dir:       $workDir" -ForegroundColor DarkCyan
Write-Host "Args:             $($launchArgs -join ' ')" -ForegroundColor DarkCyan

$startParams = @{ FilePath = $exe; WorkingDirectory = $workDir }
if ($launchArgs.Count -gt 0) { $startParams.ArgumentList = $launchArgs }
if ($Wait) { $startParams.Wait = $true }
if ($PassThru) { $startParams.PassThru = $true }

Start-Process @startParams

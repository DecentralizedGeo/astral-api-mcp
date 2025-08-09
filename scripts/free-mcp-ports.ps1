# PowerShell script to free MCP Inspector ports defined in .env-mcp-inspector
# Usage: pwsh -File scripts/free-mcp-ports.ps1 [optional path to .env file]

param(
  [string]$EnvFilePath
)

if (-not $EnvFilePath) {
  $EnvFilePath = Join-Path (Join-Path $PSScriptRoot "..") ".env-mcp-inspector"
}

function Read-DotEnv {
  param([string]$Path)
  if (-not (Test-Path -LiteralPath $Path)) {
    throw ".env file not found at $Path"
  }
  $vars = @{}
  Get-Content -LiteralPath $Path | ForEach-Object {
    $line = $_.Trim()
    if ([string]::IsNullOrWhiteSpace($line) -or $line.StartsWith('#')) { return }
    $kv = $line -split '=', 2
    if ($kv.Count -eq 2) {
      $key = $kv[0].Trim()
      $val = $kv[1].Trim()
      if ($val.StartsWith('"') -and $val.EndsWith('"')) { $val = $val.Substring(1, $val.Length-2) }
      if ($val.StartsWith("'") -and $val.EndsWith("'")) { $val = $val.Substring(1, $val.Length-2) }
      $vars[$key] = $val
    }
  }
  return $vars
}

function Get-ListeningPids {
  param([int]$Port)
  $pids = @()
  try {
    $conns = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction Stop
    if ($conns) {
      $pids = $conns | Where-Object { $_.OwningProcess } | Select-Object -ExpandProperty OwningProcess -Unique
    }
  } catch {
    # Fallback to netstat parsing
    $netstatMatches = netstat -aon | Select-String -Pattern "LISTENING" | Where-Object { $_ -match ":$Port\b" }
    foreach ($m in $netstatMatches) {
      $parts = ($m.ToString() -replace ' +', ' ').Trim().Split(' ')
      if ($parts.Length -ge 5) {
        $procId = $parts[-1]
        if ($procId -match '^\d+$') { $pids += [int]$procId }
      }
    }
    $pids = $pids | Select-Object -Unique
  }
  return $pids
}

function Stop-Pids {
  param([int[]]$Pids)
  foreach ($procId in $Pids) {
    try {
      $proc = Get-Process -Id $procId -ErrorAction Stop
      Write-Host ("Killing PID {0} ({1})" -f $procId, $proc.ProcessName)
      Stop-Process -Id $procId -Force -ErrorAction Stop
    } catch {
      try {
        taskkill /PID $procId /F | Out-Null
        Write-Host ("Killed PID {0} via taskkill" -f $procId)
      } catch {
        Write-Warning ("Failed to kill PID {0}: {1}" -f $procId, $_.Exception.Message)
      }
    }
  }
}

try {
  $envVars = Read-DotEnv -Path $EnvFilePath
} catch {
  Write-Error $_.Exception.Message
  exit 1
}

$ports = @()
if ($envVars.ContainsKey('CLIENT_PORT')) { $ports += [int]$envVars['CLIENT_PORT'] }
if ($envVars.ContainsKey('SERVER_PORT')) { $ports += [int]$envVars['SERVER_PORT'] }
$ports = $ports | Sort-Object -Unique

if ($ports.Count -eq 0) {
  Write-Error "No CLIENT_PORT or SERVER_PORT found in $EnvFilePath"
  exit 1
}

Write-Host "Checking ports: $($ports -join ', ') from $EnvFilePath"
foreach ($port in $ports) {
  $pids = @(Get-ListeningPids -Port $port)
  if ($pids.Count -gt 0) {
    Write-Host "Port $port is in use by PIDs: $($pids -join ', ')"
    Stop-Pids -Pids $pids
  } else {
    Write-Host "Port $port is free."
  }
}

Write-Host "Done. If some processes persist, try running this script as Administrator."

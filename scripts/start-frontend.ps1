param(
    [int]$Port = 8081,
    [int]$BackendPort = 8080,
    [string]$NginxPath = 'D:\nginx-1.22.0-web\nginx.exe'
)
$ErrorActionPreference = 'Stop'
if (-not (Test-Path -LiteralPath $NginxPath)) { throw 'Nginx executable not found. Supply -NginxPath.' }
$projectRoot = Split-Path $PSScriptRoot -Parent
# Keep Nginx runtime paths ASCII on Windows; the project remains in its original folder.
$runtime = Join-Path $env:TEMP 'learning-analysis-nginx'
$public = Join-Path $runtime 'public'
New-Item -ItemType Directory -Path (Join-Path $runtime 'logs') -Force | Out-Null
New-Item -ItemType Directory -Path (Join-Path $runtime 'temp') -Force | Out-Null
if (Test-Path -LiteralPath $public) {
    $link = Get-Item -LiteralPath $public -Force
    if ($link.LinkType -ne 'Junction' -or $link.Target -ne (Join-Path $projectRoot 'frontend')) { throw 'Nginx runtime public path belongs to another project.' }
} else {
    New-Item -ItemType Junction -Path $public -Target (Join-Path $projectRoot 'frontend') | Out-Null
}
$config = [System.IO.File]::ReadAllText((Join-Path $projectRoot 'deploy/nginx.conf'))
$config = $config.Replace('__WEB_PORT__', "$Port").Replace('__BACKEND_PORT__', "$BackendPort")
[System.IO.File]::WriteAllText((Join-Path $runtime 'nginx.conf'), $config, [System.Text.UTF8Encoding]::new($false))
$prefix = $runtime.Replace('\','/') + '/'
& $NginxPath -p $prefix -c nginx.conf -t
if ($LASTEXITCODE -ne 0) { throw 'Nginx configuration check failed.' }
$pidFile = Join-Path $runtime 'logs/nginx.pid'
$existingPid = 0
if (Test-Path $pidFile) { [int]::TryParse([string](Get-Content $pidFile), [ref]$existingPid) | Out-Null }
if ($existingPid -gt 0) {
    $existingProcess = Get-Process -Id $existingPid -ErrorAction SilentlyContinue
    if ($existingProcess -and $existingProcess.ProcessName -eq 'nginx') {
        & $NginxPath -p $prefix -c nginx.conf -s reload
    } else { throw 'A stale Nginx PID file exists; check this project runtime before restarting.' }
} else {
    Start-Process -FilePath $NginxPath -ArgumentList @('-p', $prefix, '-c', 'nginx.conf') -WorkingDirectory $runtime -WindowStyle Hidden
}
Write-Output "Local URL: http://127.0.0.1:$Port"
Write-Output "Nginx runtime: $runtime"

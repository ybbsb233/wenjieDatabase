param([string]$NginxPath = 'D:\nginx-1.22.0-web\nginx.exe')
$ErrorActionPreference = 'Stop'
& (Join-Path $PSScriptRoot 'stop-frontend.ps1') -NginxPath $NginxPath
$pidFile = Join-Path (Join-Path $env:TEMP 'learning-analysis-nginx') 'backend.pid'
if (Test-Path -LiteralPath $pidFile) {
    $backendId = [int](Get-Content $pidFile)
    $process = Get-CimInstance Win32_Process -Filter "ProcessId = $backendId" -ErrorAction SilentlyContinue
    if ($process -and $process.CommandLine -like '*learning-analysis-1.0.0.jar*') { Stop-Process -Id $backendId }
    elseif ($process) { throw 'PID now belongs to another process; refusing to stop it.' }
    Remove-Item -LiteralPath $pidFile
}
Write-Output 'Project services stopped. MySQL and other projects were not stopped.'

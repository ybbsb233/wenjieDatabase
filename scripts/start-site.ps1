param(
    [int]$Port = 8081,
    [int]$BackendPort = 8080,
    [string]$NginxPath = 'D:\nginx-1.22.0-web\nginx.exe'
)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
$runtime = Join-Path $env:TEMP 'learning-analysis-nginx'
$backendRoot = Join-Path $projectRoot 'backend'
$jarPath = Join-Path $backendRoot 'target/learning-analysis-1.0.0.jar'
if (-not (Test-Path -LiteralPath $jarPath)) { throw 'Build first: mvn -f backend/pom.xml package' }
New-Item -ItemType Directory -Path $runtime -Force | Out-Null
$backendPidFile = Join-Path $runtime 'backend.pid'
if (Test-Path -LiteralPath $backendPidFile) {
    $oldProcess = Get-CimInstance Win32_Process -Filter "ProcessId = $([int](Get-Content $backendPidFile))" -ErrorAction SilentlyContinue
    if ($oldProcess -and $oldProcess.CommandLine -like '*learning-analysis-1.0.0.jar*') { throw 'This project backend is already running. Use stop-site.ps1 before restarting.' }
}
if (Get-NetTCPConnection -LocalPort $BackendPort -State Listen -ErrorAction SilentlyContinue) { throw "Port $BackendPort is already in use." }
if (-not $env:DB_PASSWORD) {
    $securePassword = Read-Host 'MySQL password' -AsSecureString
    $env:DB_PASSWORD = [System.Net.NetworkCredential]::new('', $securePassword).Password
}
if (-not $env:JWT_SECRET) {
    $bytes = New-Object byte[] 48
    $generator = [System.Security.Cryptography.RandomNumberGenerator]::Create()
    $generator.GetBytes($bytes); $generator.Dispose()
    $env:JWT_SECRET = [Convert]::ToBase64String($bytes)
}
if (-not $env:ADMIN_INITIAL_PASSWORD) {
    $secureAdmin = Read-Host 'Initial administrator password (ignored if admin already exists)' -AsSecureString
    $env:ADMIN_INITIAL_PASSWORD = [System.Net.NetworkCredential]::new('', $secureAdmin).Password
}
$env:SERVER_PORT = "$BackendPort"
$javaCommand = (Get-Command java).Source
$process = Start-Process -FilePath $javaCommand -ArgumentList @('-Duser.timezone=Asia/Shanghai','-jar','target/learning-analysis-1.0.0.jar') -WorkingDirectory $backendRoot -WindowStyle Hidden -RedirectStandardOutput (Join-Path $runtime 'backend-output.log') -RedirectStandardError (Join-Path $runtime 'backend-error.log') -PassThru
[System.IO.File]::WriteAllText($backendPidFile, "$($process.Id)")
try {
    $ready = $false
    for ($attempt = 0; $attempt -lt 30; $attempt++) {
        if ($process.HasExited) { throw 'Backend startup failed. Inspect backend-output.log in the runtime directory.' }
        try {
            $response = Invoke-WebRequest -Uri "http://127.0.0.1:$BackendPort/api/auth/me" -UseBasicParsing -TimeoutSec 1 -ErrorAction Stop
        } catch {
            if ($_.Exception.Response -and [int]$_.Exception.Response.StatusCode -eq 401) { $ready = $true; break }
        }
        Start-Sleep -Milliseconds 500
    }
    if (-not $ready) { throw 'Backend readiness check timed out.' }
    & (Join-Path $PSScriptRoot 'start-frontend.ps1') -Port $Port -BackendPort $BackendPort -NginxPath $NginxPath
    Write-Output "Website started: http://127.0.0.1:$Port/login.html"
} catch {
    if (-not $process.HasExited) { Stop-Process -Id $process.Id }
    if (Test-Path $backendPidFile) { Remove-Item -LiteralPath $backendPidFile }
    throw
}

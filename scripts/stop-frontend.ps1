param([string]$NginxPath = 'D:\nginx-1.22.0-web\nginx.exe')
$ErrorActionPreference = 'Stop'
$runtime = Join-Path $env:TEMP 'learning-analysis-nginx'
$pidFile = Join-Path $runtime 'logs/nginx.pid'
if (-not (Test-Path -LiteralPath $pidFile)) { Write-Output 'This project Nginx is not running.'; exit }
$prefix = $runtime.Replace('\','/') + '/'
& $NginxPath -p $prefix -c nginx.conf -s quit
if ($LASTEXITCODE -ne 0) { throw 'Could not stop the project Nginx instance.' }

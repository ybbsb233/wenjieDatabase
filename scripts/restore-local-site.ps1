$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
Set-Location -LiteralPath $projectRoot
$securePassword = Read-Host 'MySQL password for this computer' -AsSecureString
$env:MYSQL_PWD = [System.Net.NetworkCredential]::new('', $securePassword).Password
$env:DB_PASSWORD = $env:MYSQL_PWD
try {
    @'
import os, subprocess
from pathlib import Path

root = Path.cwd()
base = ['mysql', '--host=127.0.0.1', '--user=' + os.environ.get('DB_USERNAME', 'root'), '--default-character-set=utf8mb4', '--batch', '--skip-column-names']
def run(sql, database=None):
    return subprocess.check_output(base + ([database] if database else []), input=sql, env=os.environ)

backup = root / '.local/backups/before-remaining-students.sql'
updates = root / '.local/backups/remaining_students_seed.sql'
assert backup.is_file() and updates.is_file(), 'Required backup files are missing'
exists = run(b"SELECT COUNT(*) FROM information_schema.schemata WHERE schema_name='learning_analysis';").strip()
if exists != b'0':
    raise SystemExit('Database already exists. Stopping to preserve existing data; no restore was performed.')
run(b'CREATE DATABASE learning_analysis CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;')
run(backup.read_bytes(), 'learning_analysis')
run(updates.read_bytes(), 'learning_analysis')
counts = run(b"SELECT (SELECT COUNT(*) FROM app_user WHERE role='STUDENT'),(SELECT COUNT(*) FROM question q JOIN chapter c ON c.id=q.chapter_id WHERE c.is_current=1),(SELECT COUNT(*) FROM practice WHERE archived=0 AND status='SUBMITTED'),(SELECT COUNT(*) FROM practice_item i JOIN practice p ON p.id=i.practice_id WHERE p.archived=0 AND p.status='SUBMITTED');", 'learning_analysis').strip()
assert counts == b'20\t500\t500\t10000', 'Unexpected restored counts: ' + counts.decode()
print('Restore verified: 20 students, 500 questions, 500 practices, 10000 answers.')
'@ | python -
    if ($LASTEXITCODE -ne 0) { throw 'Database restore failed. Website was not started.' }
    $env:ADMIN_INITIAL_PASSWORD = 'unused-existing-admin'
    & (Join-Path $PSScriptRoot 'start-site.ps1')
} finally {
    Remove-Item Env:MYSQL_PWD -ErrorAction SilentlyContinue
    Remove-Item Env:DB_PASSWORD -ErrorAction SilentlyContinue
}

# LoabPron :: um comando para tudo (Windows / PowerShell).
#   powershell -ExecutionPolicy Bypass -File .\play.ps1
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if (Get-Command uv -ErrorAction SilentlyContinue) {
    Write-Host "preparando o corpo (uv)..." -ForegroundColor DarkGray
    uv sync --quiet --no-dev
} else {
    if (-not (Test-Path ".venv\Scripts\python.exe")) {
        Write-Host "preparando o corpo (venv)..." -ForegroundColor DarkGray
        py -3 -m venv .venv
    }
    & .venv\Scripts\python.exe -m pip install --quiet --disable-pip-version-check -r requirements.txt
}

if (-not (Get-Command ollama -ErrorAction SilentlyContinue)) {
    Write-Host "o ollama nao existe nesta maquina. ele da voz ao oraculo (gemma, local, ~1.6 GB)." -ForegroundColor DarkRed
    $ans = Read-Host "instalar agora com 'winget install Ollama.Ollama'? [s/N]"
    if ($ans -match '^[sSyY]$') { winget install --id Ollama.Ollama -e }
}

& .venv\Scripts\python.exe run.py @args

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "[1/4] Sanal ortam oluşturuluyor..."
    py -3 -m venv .venv
}

$python = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
Write-Host "[2/4] pip güncelleniyor..."
& $python -m pip install --upgrade pip
Write-Host "[3/4] Proje ve bağımlılıklar kuruluyor..."
& $python -m pip install -e ".[dev]"
Write-Host "[4/4] Import kontrolü yapılıyor..."
& $python -c "import trading_rag_assistant; print('OK: trading_rag_assistant paketi hazır')"

if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host ".env oluşturuldu. Ollama kullanacaksanız varsayılan ayarlar hazırdır."
}
Write-Host "Kurulum tamamlandı. Uygulamayı BASLAT_WINDOWS.bat ile açabilirsiniz."

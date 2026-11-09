@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Sanal ortam bulunamadi. Once KURULUM_WINDOWS.ps1 dosyasini calistirin.
  pause
  exit /b 1
)
echo.
echo 100 soruluk Ollama kaniti baslatiliyor.
echo Bu surum evaluation icin ayri Chroma klasorunu sifirdan olusturur; ilk calismada collection bulunamadi hatasi vermez.
echo 4 ornek belge ve proje kapsam notlari her kosudan once yeniden indekslenir; bos veya eski indeks kullanilmaz.
echo Tamamlanan sorular checkpoint olarak kaydedilir; runtime_error vakalari sonraki kosuda yeniden denenir.
echo.
".venv\Scripts\python.exe" scripts\run_live_evaluation.py --provider ollama --output output\live_evaluation_ollama_v147 --top-k 5
pause

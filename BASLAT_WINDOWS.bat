@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Sanal ortam bulunamadi. Once KURULUM_WINDOWS.ps1 dosyasini PowerShell ile calistirin.
  pause
  exit /b 1
)
".venv\Scripts\python.exe" -m streamlit run app.py
pause

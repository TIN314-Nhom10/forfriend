@echo off
cd /d "%~dp0backend"
if exist "%~dp0.venv\Scripts\python.exe" (
    "%~dp0.venv\Scripts\python.exe" -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
) else (
    python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
)

@echo off
cd /d "%~dp0frontend"

if exist "%~dp0.venv\Scripts\python.exe" (
    set "PYTHON_EXE=%~dp0.venv\Scripts\python.exe"
    set "REFLEX_EXE=%~dp0.venv\Scripts\reflex.exe"
) else (
    set "PYTHON_EXE=python"
    set "REFLEX_EXE=reflex"
)

REM Patch react-router Bun restart bug on Windows
"%PYTHON_EXE%" patch_react_router.py

REM Start Reflex frontend
"%REFLEX_EXE%" run

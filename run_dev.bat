@echo off
setlocal

title ForFriend Launcher
echo ===================================================================
echo     FORFRIEND - Study Buddy Platform (COURSE PROJECT DEMO)
echo          100%% Pure Python Stack - Zero External Services
echo ===================================================================

cd /d "%~dp0"

REM Find Python executable
if exist "%~dp0.venv\Scripts\python.exe" (
    set "PYTHON_EXE=%~dp0.venv\Scripts\python.exe"
    echo [INFO] Using virtualenv: .venv
) else (
    set "PYTHON_EXE=python"
    echo [INFO] Using system python
)

REM Initialize SQLite database if not exists
if not exist "%~dp0backend\forfriend.db" (
    echo [INFO] Initializing SQLite database and seeding categories...
    pushd "%~dp0backend"
    "%PYTHON_EXE%" -m app.init_db
    popd
    echo [INFO] Database initialized.
)

echo.
echo [1/2] Starting Backend FastAPI (Port 8000)...
start "ForFriend Backend [Port 8000]" cmd /k "%~dp0run_backend.bat"

echo [INFO] Waiting 3 seconds for backend to start...
timeout /t 3 /nobreak >nul

echo [2/2] Starting Frontend Reflex (Port 3000)...
echo [INFO] Applying react-router patch for Bun/Windows...
start "ForFriend Frontend [Port 3000]" cmd /k "%~dp0run_frontend.bat"

echo.
echo ===================================================================
echo  ForFriend is running:
echo    - Local Access (This PC):    http://localhost:3000
echo    - LAN Access (Other Device): http://192.168.1.122:3000
echo    - API Docs (Swagger):        http://localhost:8000/docs
echo    - Health Check:              http://localhost:8000/health
echo    - SQLite DB file:            backend\forfriend.db
echo.
echo  Demo Accounts:
echo    - FTU Student:  nguyenvana@ftu.edu.vn / Password123!
echo    - NEU Student:  tranthib@neu.edu.vn  / Password123!
echo ===================================================================
echo.
pause

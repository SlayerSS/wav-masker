@echo off
setlocal EnableExtensions
chcp 65001 >nul 2>&1
cd /d "%~dp0"

set "PY=%~dp0.venv\Scripts\python.exe"
set "PIP=%~dp0.venv\Scripts\pip.exe"

echo ========================================
echo   WAV Masker
echo ========================================
echo.

if not exist "%PY%" (
    echo Creating virtual environment...
    where python >nul 2>&1
    if errorlevel 1 (
        echo ERROR: Python not found. Install from https://www.python.org/
        echo Enable "Add Python to PATH" during install.
        goto :fail
    )
    python -m venv "%~dp0.venv"
    if errorlevel 1 (
        echo ERROR: Failed to create .venv
        goto :fail
    )
)

echo Checking dependencies...
"%PY%" -c "import numpy, scipy" >nul 2>&1
if errorlevel 1 (
    echo Installing numpy and scipy - wait a few minutes...
    "%PIP%" install --default-timeout=120 -r "%~dp0requirements.txt"
    if errorlevel 1 (
        echo.
        echo ERROR: pip install failed. Check internet and run:
        echo   "%PIP%" install -r requirements.txt
        goto :fail
    )
)

echo Starting application...
"%PY%" "%~dp0app_gui.py"
if errorlevel 1 (
    echo.
    echo Application exited with an error.
    goto :fail
)
endlocal
exit /b 0

:fail
echo.
pause
endlocal
exit /b 1

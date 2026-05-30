@echo off
setlocal EnableExtensions
chcp 65001 >nul 2>&1
cd /d "%~dp0"

set "PY=%~dp0.venv\Scripts\python.exe"
set "PIP=%~dp0.venv\Scripts\pip.exe"
set "PIP_TIMEOUT=180"
set "PIP_RETRIES=15"

echo ========================================
echo   Build WAV Masker standalone
echo ========================================
echo.

if not exist "%PY%" (
    echo Creating virtual environment...
    where python >nul 2>&1
    if errorlevel 1 (
        echo ERROR: Python not found.
        goto :fail
    )
    python -m venv "%~dp0.venv"
    if errorlevel 1 goto :fail
)

echo Checking numpy and scipy...
"%PY%" -c "import numpy, scipy" >nul 2>&1
if errorlevel 1 (
    echo Installing requirements.txt...
    call :pip_install -r "%~dp0requirements.txt"
    if errorlevel 1 goto :fail_pip
)

echo Checking PyInstaller...
"%PY%" -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller - wait, large download...
    call :pip_install "pyinstaller>=6.0"
    if errorlevel 1 goto :fail_pip
) else (
    echo PyInstaller already installed.
)

echo.
echo Close WAV Masker.exe if it is running, then press any key...
pause >nul

echo Building - may take 5-15 minutes...
set "OUTDIR=%~dp0release"
if exist "%OUTDIR%\WAV Masker" (
    rmdir /S /Q "%OUTDIR%\WAV Masker" 2>nul
)
"%PY%" -m PyInstaller "%~dp0wav_masker.spec" --noconfirm --distpath "%OUTDIR%" --workpath "%~dp0build"
if errorlevel 1 goto :fail

set "OUT=%OUTDIR%\WAV Masker"
if exist "%~dp0ffmpeg.exe" (
    echo Copying ffmpeg.exe...
    copy /Y "%~dp0ffmpeg.exe" "%OUT%\ffmpeg.exe" >nul
) else (
    echo Note: put ffmpeg.exe next to WAV Masker.exe or use system PATH.
)

echo Syncing to dist\WAV Masker ...
if exist "%~dp0dist\WAV Masker" (
    rmdir /S /Q "%~dp0dist\WAV Masker" 2>nul
)
if not exist "%~dp0dist" mkdir "%~dp0dist"
xcopy /E /I /Y /Q "%OUT%" "%~dp0dist\WAV Masker\" >nul
if errorlevel 1 (
    echo Warning: could not copy to dist - use release\WAV Masker instead.
) else (
    echo dist\WAV Masker updated.
)

echo.
echo ========================================
echo   Done
echo ========================================
echo   Folder: %OUT%
echo   Run:    "%OUT%\WAV Masker.exe"
echo.
explorer "%OUT%"
goto :end

REM --- pip: PyPI, then mirror ---
:pip_install
"%PIP%" install --default-timeout=%PIP_TIMEOUT% --retries=%PIP_RETRIES% %*
if not errorlevel 1 exit /b 0
echo.
echo PyPI timeout. Trying mirror...
"%PIP%" install --default-timeout=%PIP_TIMEOUT% --retries=%PIP_RETRIES% ^
    -i https://pypi.tuna.tsinghua.edu.cn/simple ^
    --trusted-host pypi.tuna.tsinghua.edu.cn %*
if not errorlevel 1 exit /b 0
echo.
echo Mirror failed. Trying Aliyun...
"%PIP%" install --default-timeout=%PIP_TIMEOUT% --retries=%PIP_RETRIES% ^
    -i https://mirrors.aliyun.com/pypi/simple/ ^
    --trusted-host mirrors.aliyun.com %*
exit /b %errorlevel%

:fail_pip
echo.
echo ========================================
echo   Cannot download packages
echo ========================================
echo   Check internet / VPN / firewall.
echo.
echo   Install manually:
echo   "%PIP%" install --default-timeout=180 -r requirements.txt
echo   "%PIP%" install --default-timeout=180 pyinstaller
echo.
echo   Then run build.bat again.
goto :fail

:fail
echo.
echo BUILD FAILED
pause
exit /b 1

:end
pause
endlocal

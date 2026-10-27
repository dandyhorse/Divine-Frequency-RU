@echo off
setlocal
set "GAME=C:\Steam\steamapps\common\Divine Frequency"
set "ROOT=%~dp0.."

if not exist "%GAME%\DivineFrequency.exe" (
    echo Game not found: %GAME%\DivineFrequency.exe
    pause
    exit /b 1
)

if not exist "%ROOT%\test\dfconfig-original.ini" (
    echo Original test config not found: %ROOT%\test\dfconfig-original.ini
    pause
    exit /b 1
)

"%GAME%\DivineFrequency.exe" -config "%ROOT%\test\dfconfig-original.ini"

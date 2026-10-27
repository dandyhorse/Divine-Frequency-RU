@echo off
setlocal
set "GAME=C:\Steam\steamapps\common\Divine Frequency"
set "ROOT=%~dp0.."

if not exist "%GAME%\DivineFrequency.exe" (
    echo Game not found: %GAME%\DivineFrequency.exe
    pause
    exit /b 1
)

if not exist "%ROOT%\dist\DF_RU.pk3" (
    echo Translation not found: %ROOT%\dist\DF_RU.pk3
    echo Run tools\build_pk3.py first.
    pause
    exit /b 1
)

if not exist "%ROOT%\test\dfconfig-test.ini" (
    copy "%USERPROFILE%\Documents\My Games\Divine Frequency\dfconfig.ini" "%ROOT%\test\dfconfig-test.ini" >nul
)

"%GAME%\DivineFrequency.exe" -file "%ROOT%\dist\DF_RU.pk3" -config "%ROOT%\test\dfconfig-test.ini"

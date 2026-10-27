@echo off
setlocal
set "HERE=%~dp0"
set "GAME=%~1"

if not defined GAME (
    for /f "usebackq delims=" %%I in (`powershell -NoProfile -ExecutionPolicy Bypass -File "%HERE%find_game.ps1"`) do set "GAME=%%I"
)
if defined GAME if exist "%GAME%\DivineFrequency.exe" goto found

echo.
echo Divine Frequency was not found automatically.
echo Enter the full path to the game folder.
echo.
set /p "GAME=Game folder: "

:found
if "%GAME%"=="" goto fail
set "GAME=%GAME:"=%"
for %%I in ("%GAME%") do set "GAME=%%~fI"
if not exist "%GAME%\DivineFrequency.exe" goto fail

if not exist "%GAME%\skins\DF_RU.wad" (
    echo DF_RU.wad is not installed in this game folder.
    echo.
    pause
    exit /b 0
)

del /Q "%GAME%\skins\DF_RU.wad"
if errorlevel 1 goto fail
if exist "%GAME%\skins\DF_RU.wad" goto fail

rem Remove the skins folder only if it is empty.
rmdir "%GAME%\skins" 2>nul

echo.
echo DF_RU.wad removed.
echo The original game is unchanged.
echo.
pause
exit /b 0

:fail
echo.
echo Uninstall failed: game folder not found or file could not be removed.
echo Close the game and try again.
echo.
pause
exit /b 1

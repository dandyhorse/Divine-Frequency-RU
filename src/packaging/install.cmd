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
echo Example: C:\Steam\steamapps\common\Divine Frequency
echo.
set /p "GAME=Game folder: "

:found
if "%GAME%"=="" goto fail
set "GAME=%GAME:"=%"
for %%I in ("%GAME%") do set "GAME=%%~fI"
if not exist "%GAME%\DivineFrequency.exe" goto fail
if not exist "%GAME%\DFSDSA.ipk3" goto fail
echo "%GAME%" | findstr /I /C:"Divine Frequency Demo" >nul
if not errorlevel 1 goto demo

if not exist "%GAME%\skins" (
    mkdir "%GAME%\skins"
    if errorlevel 1 goto fail
)

if exist "%GAME%\skins\DF_RU.wad" (
    echo Updating existing DF_RU.wad...
) else (
    echo Installing DF_RU.wad...
)
copy /Y "%HERE%DF_RU.wad" "%GAME%\skins\DF_RU.wad" >nul
if errorlevel 1 goto fail

echo.
echo Done.
echo Translation: %GAME%\skins\DF_RU.wad
echo Start the game normally (Steam or the original shortcut).
echo.
pause
exit /b 0

:fail
echo.
echo Installation failed: game folder not found or file copy error.
echo Expected DivineFrequency.exe and DFSDSA.ipk3 in the selected folder.
echo.
pause
exit /b 1

:demo
echo.
echo This patch is for the full version of Divine Frequency.
echo The Demo uses different game data and is not supported.
echo Select the full game folder, not "Divine Frequency Demo".
echo.
pause
exit /b 1

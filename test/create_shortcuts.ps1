$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot
$game = 'C:\Steam\steamapps\common\Divine Frequency'
$exe = Join-Path $game 'DivineFrequency.exe'
$desktop = [Environment]::GetFolderPath('Desktop')

if (-not (Test-Path -LiteralPath $exe)) {
    throw "Game executable not found: $exe"
}
if (-not (Test-Path -LiteralPath (Join-Path $root 'dist\DF_RU.pk3'))) {
    throw "Translation PK3 not found. Build it first."
}

$shell = New-Object -ComObject WScript.Shell

$ru = $shell.CreateShortcut((Join-Path $desktop 'Divine Frequency (RU).lnk'))
$ru.TargetPath = $exe
$ru.Arguments = "-file `"$root\dist\DF_RU.pk3`" -config `"$root\test\dfconfig-test.ini`""
$ru.WorkingDirectory = $game
$ru.IconLocation = "$exe,0"
$ru.Description = 'Divine Frequency - русский перевод (DF_RU.pk3)'
$ru.Save()

$original = $shell.CreateShortcut((Join-Path $desktop 'Divine Frequency (Original).lnk'))
$original.TargetPath = $exe
$original.Arguments = "-config `"$root\test\dfconfig-original.ini`""
$original.WorkingDirectory = $game
$original.IconLocation = "$exe,0"
$original.Description = 'Divine Frequency - оригинал (English)'
$original.Save()

Write-Host "Created:"
Write-Host "  $(Join-Path $desktop 'Divine Frequency (RU).lnk')"
Write-Host "  $(Join-Path $desktop 'Divine Frequency (Original).lnk')"

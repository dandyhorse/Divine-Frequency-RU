param(
    [string]$ExplicitPath = ""
)

$ErrorActionPreference = "SilentlyContinue"
$GameDirName = "Divine Frequency"
$Found = $null

function Test-GameDir([string]$Path) {
    if ([string]::IsNullOrWhiteSpace($Path)) { return $false }
    $Path = $Path.Trim().Trim('"')
    if (-not (Test-Path -LiteralPath $Path -PathType Container)) { return $false }
    return (Test-Path -LiteralPath (Join-Path $Path "DivineFrequency.exe") -PathType Leaf) -and
           (Test-Path -LiteralPath (Join-Path $Path "DFSDSA.ipk3") -PathType Leaf)
}

function Add-Candidate([string]$Path) {
    if ($script:Found) { return }
    if (Test-GameDir $Path) {
        $script:Found = (Resolve-Path -LiteralPath $Path).Path
    }
}

if ($ExplicitPath) {
    $ExplicitPath = $ExplicitPath.Trim().Trim('"')
    if (Test-Path -LiteralPath $ExplicitPath -PathType Leaf) {
        $ExplicitPath = Split-Path -Parent $ExplicitPath
    }
    Add-Candidate $ExplicitPath
}

# Common default locations.
$defaults = @()
foreach ($base in @(${env:ProgramFiles(x86)}, $env:ProgramFiles)) {
    if ($base) { $defaults += (Join-Path $base "Steam\steamapps\common\$GameDirName") }
}
$defaults += "C:\Steam\steamapps\common\$GameDirName"
$defaults += "D:\Steam\steamapps\common\$GameDirName"
$defaults += "D:\SteamLibrary\steamapps\common\$GameDirName"
$defaults += "E:\SteamLibrary\steamapps\common\$GameDirName"
foreach ($p in $defaults) { Add-Candidate $p }

$steamRoots = @()

# Steam install path from the registry.
$registryPaths = @(
    "HKCU:\Software\Valve\Steam",
    "HKLM:\SOFTWARE\WOW6432Node\Valve\Steam",
    "HKLM:\SOFTWARE\Valve\Steam"
)
foreach ($reg in $registryPaths) {
    $item = Get-ItemProperty -Path $reg -ErrorAction SilentlyContinue
    if ($item) {
        if ($item.SteamPath) { $steamRoots += $item.SteamPath }
        if ($item.InstallPath) { $steamRoots += $item.InstallPath }
    }
}

$steamRoots = $steamRoots | Where-Object { $_ } | Select-Object -Unique
foreach ($root in $steamRoots) {
    $root = $root.Trim().Trim('"').Replace("/", "\")
    Add-Candidate (Join-Path $root "steamapps\common\$GameDirName")
}

# Every Steam library listed in libraryfolders.vdf.
$libraries = @()
foreach ($root in $steamRoots) {
    $root = $root.Trim().Trim('"').Replace("/", "\")
    $vdf = Join-Path $root "steamapps\libraryfolders.vdf"
    if (-not (Test-Path -LiteralPath $vdf -PathType Leaf)) { continue }
    $text = Get-Content -LiteralPath $vdf -Raw
    foreach ($m in [regex]::Matches($text, '"path"\s+"([^"]+)"')) {
        $libraries += $m.Groups[1].Value.Replace("\\", "\")
    }
    foreach ($m in [regex]::Matches($text, '"\d+"\s+"([A-Za-z]:\\[^"]+)"')) {
        $libraries += $m.Groups[1].Value.Replace("\\", "\")
    }
}
$libraries = $libraries | Where-Object { $_ } | Select-Object -Unique
foreach ($lib in $libraries) {
    Add-Candidate (Join-Path $lib "steamapps\common\$GameDirName")
    if ($script:Found) { break }
}

# Fallback: scan app manifests for a renamed game folder.
if (-not $script:Found) {
    foreach ($lib in $libraries) {
        $apps = Join-Path $lib "steamapps"
        if (-not (Test-Path -LiteralPath $apps -PathType Container)) { continue }
        foreach ($manifest in Get-ChildItem -LiteralPath $apps -Filter "appmanifest_*.acf" -File -ErrorAction SilentlyContinue) {
            $text = Get-Content -LiteralPath $manifest.FullName -Raw
            if ($text -notmatch '"name"\s+"[^"]*Divine Frequency[^"]*"') { continue }
            $m = [regex]::Match($text, '"installdir"\s+"([^"]+)"')
            if ($m.Success) {
                Add-Candidate (Join-Path $apps ("common\" + $m.Groups[1].Value.Replace("\\", "\")))
            }
            if ($script:Found) { break }
        }
        if ($script:Found) { break }
    }
}

if ($script:Found) {
    Write-Output $script:Found
    exit 0
}
exit 1

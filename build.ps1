param(
    [switch]$SkipTests,
    [switch]$SkipInstaller
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -LiteralPath $ProjectRoot

python -m pip install -r requirements-dev.txt
if (-not $SkipTests) {
    python -m pytest -q
}

python -m PyInstaller --noconfirm --clean ShroudDesigner.spec

if (-not $SkipInstaller) {
    $CompilerCandidates = @(
        "${env:ProgramFiles(x86)}\Inno Setup 6\ISCC.exe",
        "$env:ProgramFiles\Inno Setup 6\ISCC.exe",
        "$env:LOCALAPPDATA\Programs\Inno Setup 6\ISCC.exe"
    )
    $InnoCompiler = $CompilerCandidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
    if (-not $InnoCompiler) {
        throw "Inno Setup 6 was not found. Install it with: winget install JRSoftware.InnoSetup"
    }
    & $InnoCompiler "installer\ShroudDesigner.iss"
}

Write-Host "Build complete."
Write-Host "Application: dist\ShroudDesigner\ShroudDesigner.exe"
if (-not $SkipInstaller) {
    Write-Host "Installer: dist\ShroudDesigner-0.2-Setup.exe"
}

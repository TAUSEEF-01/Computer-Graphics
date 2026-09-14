# Run from any working directory without activating the virtual environment.
$taskPython = Join-Path (Split-Path -Parent $PSScriptRoot) '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $taskPython)) {
    throw 'Python environment is missing. Follow the setup steps in Lab1/README.md.'
}
& $taskPython (Join-Path $PSScriptRoot 'pixel_plotter.py') @args
exit $LASTEXITCODE

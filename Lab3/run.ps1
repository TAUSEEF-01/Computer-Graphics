# Run Lab 3 from any working directory without activating the environment.
$taskPython = Join-Path (Split-Path -Parent $PSScriptRoot) '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $taskPython)) {
    throw 'Python environment is missing. Follow the setup steps in Lab3/README.md.'
}
& $taskPython (Join-Path $PSScriptRoot 'dda_error_rays.py') @args
exit $LASTEXITCODE

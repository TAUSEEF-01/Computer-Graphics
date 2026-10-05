$taskPython = Join-Path (Split-Path -Parent $PSScriptRoot) '.venv\Scripts\python.exe'
& $taskPython (Join-Path $PSScriptRoot 'dda_zones.py')
exit $LASTEXITCODE

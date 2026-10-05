# Build using the local 32-bit FreeGLUT library matched to C:/MinGW.
$ErrorActionPreference = 'Stop'
$taskRoot = Split-Path -Parent $PSScriptRoot
$taskFreeglut = Join-Path $taskRoot '.venv\cpp-deps\freeglut-MinGW-rel-v3.0.0-1.tz'
$taskInclude = Join-Path $taskFreeglut 'include'
$taskLibrary = Join-Path $taskFreeglut 'lib\libfreeglut_static.a'
$taskSource = Join-Path $PSScriptRoot 'dda_zones.cpp'
$taskExecutable = Join-Path $PSScriptRoot 'dda_zones.exe'
if (-not (Test-Path -LiteralPath $taskLibrary)) {
    throw "Local FreeGLUT library is missing: $taskLibrary"
}
& 'C:\MinGW\bin\g++.exe' -std=c++11 -Wall -Wextra -DFREEGLUT_STATIC "-I$taskInclude" $taskSource $taskLibrary -o $taskExecutable -lopengl32 -lgdi32 -lwinmm -static-libgcc -static-libstdc++
if ($LASTEXITCODE -ne 0) { throw 'C++ compilation failed.' }
Write-Output "Built: $taskExecutable"

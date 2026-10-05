# Lab 4: eight line-drawing zones

## C++ version

The C++ file retains the earlier DDA implementation. The Python version below now uses Bresenham.

From the Lab4 directory:

```powershell
.\build_cpp.ps1
.\dda_zones.exe
```

The build script uses `C:\MinGW\bin\g++.exe` and a 32-bit FreeGLUT static library built with that compiler. Headers and the library are installed locally under `.venv/cpp-deps/freeglut-MinGW-rel-v3.0.0-1.tz`. The static build embeds FreeGLUT and the C++ runtime, so no separate FreeGLUT DLL is needed beside the executable.

FreeGLUT source: [TransmissionZero/freeglut-MinGW release 3.0.0-1.tz](https://github.com/TransmissionZero/freeglut-MinGW/tree/rel/v3.0.0-1.tz). To rebuild that dependency, run `mingw32-make SHELL=cmd.exe lib/libfreeglut_static.a` from its source directory.

## Python version

Run from the project directory:

```powershell
.\Lab4\run.ps1
```

Based on Lab3, this program draws 36 diameters (180/5) as 72 colored half-lines, spaced 5 degrees apart, with radius 250 in a 960×540 window. Each half-line starts at the origin, so its direction identifies its zone. Zone colors replace the Lab3 error-based grayscale.

`find_zone()` determines the zone using dx, dy and their absolute magnitudes. `drawLine()` calls the matching function. Each `drawLine_0` through `drawLine_7` supplies its dominant distance, other distance, and movement directions to `plot_bresenham_points()`.

The shared Bresenham loop uses integer arithmetic. Its decision variable starts at `2 * minor - major`. Every step moves along the dominant axis. If the decision variable is non-negative, it also moves along the other axis and adds `2 * (minor - major)` to the decision; otherwise it adds `2 * minor`. Both endpoints are included, including the special case of a single-point line. Coordinate rounding is used only to calculate the integer circle endpoints, not during line drawing.

Use the zone functions with integer endpoints belonging to their respective zones; use `drawLine()` for automatic selection.

| Zone | Direction | Dominant coordinate | Color | Function |
|---|---|---|---|---|
| 0 | Right/up | x | Cyan | drawLine_0 |
| 1 | Right/up | y | Magenta | drawLine_1 |
| 2 | Left/up | y | Yellow | drawLine_2 |
| 3 | Left/up | x | Red | drawLine_3 |
| 4 | Left/down | x | Green | drawLine_4 |
| 5 | Left/down | y | Orange | drawLine_5 |
| 6 | Right/down | y | Black | drawLine_6 |
| 7 | Right/down | x | Blue | drawLine_7 |

When |dx| equals |dy|, the line belongs to the x-dominant zone of its quadrant. The horizontal/vertical boundaries are resolved by the sign checks in `find_zone()`. The background is white. Set `PRINT_POINTS = True` to print the Bresenham coordinates.

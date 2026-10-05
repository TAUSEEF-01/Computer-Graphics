# Lab 4: eight DDA zones

Run from the project directory:

```powershell
.\Lab4\run.ps1
```

Based on Lab3, this program draws 36 diameters (180/5) as 72 colored half-lines, spaced 5 degrees apart, with radius 250 in a 960×540 window. Each half-line starts at the origin, so its direction identifies its zone. Zone colors replace the Lab3 error-based grayscale.

`find_zone()` determines the zone using dx, dy and their absolute magnitudes. `drawLine()` calls the matching function. Each `drawLine_0` through `drawLine_7` calculates its own DDA step count and coordinate increments, then calls the shared pixel plotting loop. Use these functions with integer endpoints belonging to their respective zones; use `drawLine()` for automatic selection.

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

When |dx| equals |dy|, the line belongs to the x-dominant zone of its quadrant. The horizontal/vertical boundaries are resolved by the sign checks in `find_zone()`. The gray background makes black and the other colors visible. Set `PRINT_POINTS = True` to print the DDA coordinates.

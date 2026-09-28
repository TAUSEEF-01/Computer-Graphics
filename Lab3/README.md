# Lab 3: DDA rounding-error rays

Run from the Computer-Graphics project directory:

```powershell
.\Lab3\run.ps1
```

The program uses a 960×540 window and draws exactly **36 diameter lines** through a circle of radius 250:

```text
number of lines = 180 / 5 = 36
```

The line orientations are `0, 5, 10, ..., 175` degrees. Each line runs between opposite circle points, such as `(-250,0)` and `(250,0)`. An angle of 180 degrees would duplicate the line at 0 degrees, so it is excluded.

The background is medium blue-gray. Low-error lines approach black and high-error lines approach white, so both extremes can be distinguished from the background.

The program works in two passes:

1. `calculate_line_error()` runs DDA for every ray. At each DDA point it applies the required rounding rule:

   ```python
   rounded_x = int(x + 0.5 * sign(x))
   rounded_y = int(y + 0.5 * sign(y))
   ```

   The error magnitude is calculated from the requested expression:

   ```python
   error = abs((x - rounded_x) + (y - rounded_y))
   ```

   Each point's non-negative error magnitude is added to `line_total_error`. This sum becomes that line's error. After calculating all 36 line totals, the largest total becomes `MAX_ERROR`. At 45 and 135 degrees, x and y advance by exact integer amounts together, so their total error is zero.

2. `draw_dda_line()` runs DDA again. Each entire line receives the grayscale color `line_total_error / MAX_ERROR`. A line with a small total error is dark, and the line with the largest total error is white.

The terminal prints every line's endpoint, total error, and normalized brightness. Change `PRINT_POINTS` to `True` to also print every DDA point using the requested format.

The existing project `.venv` and PyOpenGL installation are reused from the earlier labs.

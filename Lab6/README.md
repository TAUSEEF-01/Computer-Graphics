# Lab 6: falling circle and midpoint ellipse

Run from this Lab6 folder using the repository's existing Python environment:

```powershell
..\.venv\Scripts\python.exe .\falling_ellipse.py
```

Uses the same PyOpenGL/freeglut setup as Lab5. No new dependencies are needed in
the existing environment.

## Mathematical interpretation

The original statements `a = b = r` and `a*a + b*b = r*r` cannot both hold for a
nonzero r. This implementation follows the selected interpretation: preserve
`a*a + b*b = r*r`. Here a and b are horizontal and vertical semiaxes; r is the
invariant parameter, not the starting circle radius.

- Initial circle: `a = b = r / sqrt(2)`.
- During compression: decrease b and compute `a = sqrt(r*r - b*b)`.
- Maximum compression at `a = 2*b`: `b = r/sqrt(5)` and `a = 2*r/sqrt(5)`.
- During the rebound, b increases back to `r/sqrt(2)` while a is recomputed
  from the invariant. The shape becomes a circle at the original top height.

The outline uses the PDF's implicit function
`f(x,y) = b*b*x*x + a*a*y*y - a*a*b*b`, four-way symmetry, and two regions.
Region 1 tests `(x+1, y-0.5)` and chooses E or SE. Region 2 tests
`(x+0.5, y-1)` and chooses S or SE. The incremental formulas use coordinates
before the pixel step. Only drawing rounds the semiaxes to integer pixels;
the mathematical semiaxes preserve the invariant to floating-point precision.

## Movement

Acceleration is interpreted as pixels/frame squared; speed is pixels/frame.
Each falling frame applies `velocity += 5`, then `yc -= velocity`.
At ground contact, clamp the bottom to the floor and stop the falling velocity.
Compression starts from rest with `velocity += 1`, then `b -= velocity`, clamped
at `r/sqrt(5)`. Set `yc = FLOOR_Y + b` so the bottom stays on the floor.
At maximum deformation, the shape launches upward. With downward acceleration
`g = 5`, a launch speed `sqrt(2*g*h)` reaches the original top with zero speed;
h is the center's height difference from maximum compression to the top.
Velocity is negative during ascent. Each rising frame integrates
`yc -= velocity*dt + 0.5*g*dt*dt`, then `velocity += g*dt`. The last step uses
the remaining fraction of a frame `dt = -velocity/g` to reach the apex exactly.
The ellipse gradually recovers its circle shape in proportion to height gained,
while maintaining the invariant. It reaches the top with zero velocity as a
circle, then begins the next drop on the following frame. This sequence repeats
until the window is closed or ESC is pressed.
This is a prescribed lab animation rather than a physical elastic collision.

Set `R`, `FPS`, and the acceleration constants near the top of the script.
Acceleration is per frame, so changing FPS changes playback duration.

The display shows only the animated shape and the floor, with no status text or
control hints. Close the window or press ESC to exit.

Run the focused mathematical checks:

```powershell
..\.venv\Scripts\python.exe -m unittest -v test_falling_ellipse.py
```

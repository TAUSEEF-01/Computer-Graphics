# Lab 6: falling circle and midpoint ellipse

Run from this Lab6 folder using the repository's existing Python environment:

```powershell
..\.venv\Scripts\python.exe .\falling_ellipse.py
```

Uses the same PyOpenGL/freeglut setup as Lab5. No new dependencies are needed in
the existing environment.

## C++ version

`falling_ellipse.cpp` implements the same animation with OpenGL/FreeGLUT,
including the current `R = 30` setting. From Lab6, build and run:

```powershell
.\build_cpp.ps1
.\falling_ellipse.exe
```

The build script reuses the repository's local 32-bit FreeGLUT static library
and `C:\MinGW\bin\g++.exe`, as Lab4 does. It needs no separate FreeGLUT DLL.
For another MinGW setup with FreeGLUT installed, an equivalent dynamic build is:

```powershell
g++ -std=c++11 -Wall -Wextra falling_ellipse.cpp -o falling_ellipse.exe -lfreeglut -lopengl32
```

For a dynamic build, the matching FreeGLUT DLL must be beside the executable
or on PATH. Close the window or press ESC to exit either version.

## Mathematical interpretation

The Python version starts with `a = b = r`, so r is the initial circle radius.
It preserves `a*a + b*b = 2*r*r` during compression and rebound.

- Initial circle: `a = b = r`.
- During compression: decrease b and compute `a = sqrt(2*r*r - b*b)`.
- Maximum compression at `a = 2*b`: `b = r*sqrt(2/5)` and `a = 2*b`.
- During the rebound, b increases back to r while a is recomputed from the
  invariant. The shape becomes a circle at the original top height.

The C++ version retains its earlier initialization `a = b = r/sqrt(2)` and
invariant `a*a + b*b = r*r`.

The outline uses the PDF's implicit function
`f(x,y) = b*b*x*x + a*a*y*y - a*a*b*b`, four-way symmetry, and two regions.
The first quadrant is traced from `(a,0)` toward `(0,b)`. The C++ implementation
swaps the axes for the midpoint calculation, then maps each local `(x,y)` to
display `(y,x)`. Local E/SE steps become N/NW, and local S/SE steps become
W/NW. The incremental formulas use coordinates before the pixel step.
Only drawing rounds the semiaxes to integer pixels;
the mathematical semiaxes preserve the invariant to floating-point precision.

The Python version uses ordinary functions and global variables, like Lab5.
`draw_ellipse()` starts directly at `(a,0)`, takes N/NW steps near the right
edge, then W/NW steps near the top. `draw4way_symmetry()` plots four pixels
directly with `glVertex2i`. There are no generators or animation classes.

## Movement

Acceleration is interpreted as pixels/frame squared; speed is pixels/frame.
Each falling frame applies `velocity += 5`, then `yc -= velocity`.
At ground contact, clamp the bottom to the floor and stop the falling velocity.
Compression starts from rest with `velocity += 1`, then `b -= velocity`, clamped
at `r*sqrt(2/5)` in Python (`r/sqrt(5)` in C++). Set `yc = FLOOR_Y + b` so the bottom stays on the floor.
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

Set `r` and `FPS` near the top of the Python script; acceleration is set in the movement functions.
Acceleration is per frame, so changing FPS changes playback duration.

The display shows only the animated shape and the floor, with no status text or
control hints. Close the window or press ESC to exit.

Run the focused mathematical checks:

```powershell
..\.venv\Scripts\python.exe -m unittest -v test_falling_ellipse.py
```


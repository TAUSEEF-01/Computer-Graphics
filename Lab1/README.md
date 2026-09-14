# Lab 1: raster graphics, graphics pipeline, and pixel plotting

## Run

From the Computer-Graphics project directory in PowerShell:

```powershell
.\Lab1\run.ps1
.\Lab1\run.ps1 --pixel 100 100 255 255 255
.\Lab1\run.ps1 --pixel -200 80 0 255 0 --pixel 150 -100 0 0 255
```

If PowerShell script execution is disabled, run Python directly:

```powershell
& .\.venv\Scripts\python.exe .\Lab1\pixel_plotter.py --pixel 100 100 255 255 255
```

The background is black. The default plots a **white 3×3 block centered at (100, 100)**: its nine pixels span x=99..101 and y=99..101. Each `--pixel` takes **x y red green blue** and draws a centered 3×3 block; RGB channels are integers from 0 to 255. Repeat this option to plot several blocks. Click to add blocks in the last supplied color (white by default). **C** clears plotted pixels, **G** toggles the grid, and **Esc** or the close button exits. Read the center coordinate in the last-pixel status at the bottom. Blocks at the canvas boundary are clipped to valid coordinates.

## Coordinate system

The drawing area is **960 by 720 device pixels**, with x from **-480 to +479** and y from **-360 to +359**. The height was chosen for this lab because only the x range was specified. The origin (0, 0) is near the center; positive x goes right and positive y goes up. Grid lines are 20 units apart, with stronger lines and labels every 100 units.

OpenGL uses `glOrtho(-480, 480, -360, 360, -1, 1)`. Those projection bounds describe pixel *edges*; the valid integer pixel coordinates end at 479 and 359. `plot_pixel()` places each point at `(x + 0.5, y + 0.5)` so it lands at the center of exactly one device pixel. Mouse positions start at the top left, so the mouse callback reverses y. Resizing preserves a 960 by 720 viewport: larger windows add margins and smaller windows clip the canvas. Keep the original size to see every coordinate.

The reusable plotting function is:

```python
plot_pixel(x, y, red, green, blue)
```

Call it with an active OpenGL context and the projection above, during rendering. `plot_pixel()` draws one device pixel. The application calls `plot_pixel_block()` to draw that center pixel and its eight neighbors in the same color, forming a 3×3 block. It stores center coordinates in a dictionary and redraws the blocks whenever GLUT requests a repaint.

## Raster graphics overview

A raster image is a rectangular array of pixels. Each pixel stores a color; an RGB color combines red, green, and blue intensities. For example, (255, 0, 0) is red, (0, 255, 0) is green, (0, 0, 255) is blue, and (255, 255, 255) is white. Increasing the pixel count can show more detail. Zooming into a raster image eventually reveals individual pixels.

## Graphics pipeline overview

1. **Application:** validate coordinates/colors, store pixels, and issue drawing commands.
2. **Vertex transformation:** apply model/view and projection transformations; this lab uses an identity model/view and an orthographic projection.
3. **Clipping and viewport mapping:** clip geometry to the view and map it to window coordinates.
4. **Rasterization:** convert points and lines into fragments covering device pixels. `GL_POINTS` with size 1 draws the requested pixel.
5. **Fragment processing:** determine fragment colors and apply enabled tests/operations. This program disables smoothing, blending, and dithering to preserve the requested RGB values.
6. **Framebuffer and presentation:** write colors into the back buffer and use `glutSwapBuffers()` to display the completed frame.

This introductory program uses OpenGL's compatibility API (`glBegin`/`glEnd`). Modern OpenGL commonly uses vertex buffers and shaders, but the stages above still describe the overall pipeline.

## Environment and dependencies

The project uses **Python 3.12** and a local **.venv** in Computer-Graphics. PyOpenGL provides Python bindings; GLUT/FreeGLUT creates the window and handles input. PyOpenGL_accelerate supplies optional acceleration. The installed Windows PyOpenGL wheel includes the FreeGLUT DLLs, so no system DLL copying was needed on this machine.

To recreate the environment from the project directory:

```powershell
py -3.12 -m venv .venv
& .\.venv\Scripts\python.exe -m pip install -r .\Lab1\requirements.txt
```

Select `.venv\Scripts\python.exe` as your editor's interpreter. If GLUT cannot load, confirm Python and the GLUT library have matching architecture (this setup uses 64-bit Python). On Linux, install your distribution's FreeGLUT runtime separately. An OpenGL-capable graphics driver is required.

Dependency references: [PyOpenGL installation](https://pyopengl.sourceforge.net/documentation/installation.html), [PyOpenGL package](https://pypi.org/project/PyOpenGL/), and [FreeGLUT project](https://freeglut.sourceforge.net/index.php).

## Verify the actual rendering

```powershell
& .\.venv\Scripts\python.exe .\Lab1\pixel_plotter.py --self-test
```

This briefly creates an OpenGL window and reads back six rendered pixels, including the four coordinate corners and the origin, to check the exact RGB colors and coordinate mapping. Another 25 readbacks verify that the centered block covers exactly nine white pixels and the surrounding border stays black with the grid hidden. It exits after reporting the result.

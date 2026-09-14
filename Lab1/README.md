# Lab 1: white pixels at the origin

Run from the Computer-Graphics project directory:

```powershell
.\Lab1\run.ps1
```

Or run Python directly:

```powershell
& .\.venv\Scripts\python.exe .\Lab1\pixel_plotter.py
```

The program draws a black 960 by 720 window with graph-paper lines and labeled axes. The x coordinates range from -480 to 479, and y from -360 to 359. A white 3x3 block is fixed at the origin: x=-1,0,1 and y=-1,0,1. The main pixel is (0,0), surrounded by its eight white neighbors. There are no mouse-click features or keyboard controls. Close the window using its close button.

`plot_pixel(x, y, red, green, blue)` draws one device pixel. RGB intensities range from 0.0 to 1.0; (1.0,1.0,1.0) is white. Two short loops in `display()` draw the nine pixels. The half-unit offset places each point at a device pixel's center. Resizing keeps the canvas at 960 by 720 pixels, adding margins or clipping it.

A raster image is an array of pixels, each storing a color. This lab follows the graphics pipeline: issue drawing commands, transform coordinates with an orthographic projection, map them into the viewport, rasterize points and lines, write their colors to the framebuffer, and swap buffers to display the image.

## Environment setup

The project-local `.venv` already contains PyOpenGL and PyOpenGL_accelerate. The Windows PyOpenGL wheel includes FreeGLUT for window creation.

To recreate the environment:

```powershell
py -3.12 -m venv .venv
& .\.venv\Scripts\python.exe -m pip install -r .\Lab1\requirements.txt
```

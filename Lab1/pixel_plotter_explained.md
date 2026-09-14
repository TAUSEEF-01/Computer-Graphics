# `pixel_plotter.py`: a complete beginner's guide

This guide explains the original 95-line `pixel_plotter.py`, function by function and line by line. It also explains the Python built-in functions and the OpenGL/GLUT library functions used by the code. Line numbers below refer to the original Python file; they are not part of Python syntax.

You do not need previous knowledge of Python or computer graphics. Start with the first three sections, then read the functions in order. The small examples are learning examples, not changes to the original program.

## 1. What does the program do?

It opens a window and draws:

- A black background.
- Dark gray horizontal and vertical lines, like graph paper.
- Brighter gray x and y axes, with numbers beside them.
- Nine white pixels arranged in a 3×3 square near the center.

The drawing area starts at **960 pixels wide and 720 pixels high**. A pixel is one tiny colored cell in the image stored for the window. A 3×3 block is extremely small: it is only three pixels across and three pixels tall.

The nine selected pixel coordinates are:

```text
                   x coordinate
                 -1       0       1
             +--------+--------+--------+
     y =  1  | (-1,1) | (0,1)  | (1,1)  |
             +--------+--------+--------+
     y =  0  | (-1,0) | (0,0)  | (1,0)  |
             +--------+--------+--------+
     y = -1  |(-1,-1) | (0,-1) | (1,-1) |
             +--------+--------+--------+
```

The center pixel is `(0, 0)`. The other eight surround it. The program has no mouse-click drawing or keyboard controls. Closing its window ends the event loop.

Here, “nine white pixels” means the nine points deliberately plotted by `display()`. The grid and text also consist of pixels, but they use gray colors.

## 2. Python ideas you need first

### Variables, numbers, and strings

A **variable** is a name that refers to a value:

```python
x = 20
text = "Hello"
```

`x` refers to the integer `20`. An **integer** is a whole number. A **float**, such as `0.75`, can represent a fractional number. A **string**, such as `"Hello"`, is text. Quotation marks mark the boundaries of a string; they are not displayed as part of its contents.

### Functions, parameters, and arguments

A **function** is a named piece of reusable code:

```python
def greet(name):
    print(name)

greet("Asha")
```

- `def` defines the function.
- `greet` is its name.
- `name` is a **parameter**: a name for an input the function receives.
- `"Asha"` is an **argument**: the actual input provided in this call.
- `greet("Asha")` **calls** the function, so its body runs.

Defining a function does not immediately run its body. Python remembers it so it can be called later.

The six functions defined in this file do their work by changing graphics settings or drawing. None has a `return` statement, so each returns Python's `None` when it finishes. `None` means that no useful result value is being returned. A function can do useful work without returning a number or string.

### Indentation and the colon

Python uses indentation—the spaces at the beginning of a line—to show which statements belong together:

```python
for x in range(3):
    print(x)
print("Finished")
```

The indented `print(x)` belongs to the loop and runs three times. The unindented final statement runs once afterward. A colon `:` begins a block after a function definition, loop, or condition. This file uses four spaces for each indentation level.

### Loops and conditions

A `for` loop repeats work for each item:

```python
for character in "cat":
    print(character)
```

The variable `character` receives `"c"`, then `"a"`, then `"t"`.

An `if` condition runs its indented block only when the condition is true:

```python
if x != 0:
    print(x)
```

`!=` means “is not equal to.” `==` means “is equal to.” A single `=` assigns a value; it does not test equality.

### Imports and the dot

An **import** makes code from another module or package available. A module is a unit of Python code; a package organizes modules.

In `GL.glColor3f(...)`, the dot means “look up `glColor3f` inside `GL`.” The parentheses then call that function. In `GL.GL_LINES`, the dot looks up a named constant instead; there are no call parentheses.

### Three types of names in this file

| Type | Examples | Where they come from |
|---|---|---|
| User-defined functions | `draw_grid`, `display`, `main` | Defined by this file using `def` |
| Python built-ins | `range`, `ord`, `str` | Available from Python without an import |
| Library functions | `GL.glVertex2f`, `GLUT.glutCreateWindow` | Supplied by imported libraries |

`sys.argv` is an attribute containing a list, not a function. `GL.GL_POINTS` and similar uppercase names are constants, not functions.

## 3. Graphics ideas you need first

### OpenGL, PyOpenGL, and GLUT

**OpenGL** provides commands for graphics. **PyOpenGL** makes those commands accessible from Python. The imported `GL` module supplies the drawing and graphics-setting calls used here.

**GLUT** is a toolkit for creating graphics windows and handling window events. The imported `GLUT` module exposes toolkit calls to Python. This program also uses a **FreeGLUT** extension to make its main loop return when the window closes. See the [FreeGLUT API documentation](https://freeglut.sourceforge.net/docs/api.php).

### Coordinates

A position `(x, y)` describes a location:

- `x` tells you the horizontal position: negative is left, positive is right.
- `y` tells you the vertical position: negative is down, positive is up.
- `(0, 0)` is the **origin**, placed at the center of this program's coordinate area.

```text
                         positive y
                             ^
                             |
      negative x <-----------+-----------> positive x
                           (0,0)
                             |
                             v
                         negative y
```

`reshape()` sets coordinate boundaries of `-480` to `480` horizontally and `-360` to `360` vertically. Their spans are `960` and `720` units. The viewport has the same size in framebuffer pixels, so one coordinate unit maps to one framebuffer pixel.

The boundaries are not all pixel-center coordinates. The plotted integer pixel labels run from `-480` through `479`, and `-360` through `359`; the code adds `0.5` to reach their centers.

### RGB colors

RGB means **red, green, blue**. This code uses intensities between `0.0` and `1.0`:

| RGB values | Color |
|---|---|
| `(0.0, 0.0, 0.0)` | Black |
| `(1.0, 1.0, 1.0)` | White |
| `(1.0, 0.0, 0.0)` | Red |
| `(0.0, 1.0, 0.0)` | Green |
| `(0.0, 0.0, 1.0)` | Blue |
| `(0.5, 0.5, 0.5)` | Gray |

Equal red, green, and blue values produce gray. Increasing all three makes a brighter gray.

### OpenGL remembers settings

OpenGL maintains **state**, meaning settings that remain active until changed. Setting the current color does not draw anything by itself. Later drawing commands use that color.

Think of choosing a pen color before drawing. Similarly, `glPointSize(1)` chooses a size for subsequent points; `glMatrixMode(...)` selects which transformation setting later matrix calls modify.

### Vertices, primitives, and rasterization

A **vertex** is a position supplied to OpenGL. A **primitive** is a basic drawing element, such as a point or line. In this file:

- `GL_POINTS` treats each vertex as a separate point.
- `GL_LINES` treats each pair of vertices as a separate line segment.

Turning these mathematical positions and lines into colored image pixels is called **rasterization**. See the [Khronos explanation of primitives](https://wikis.khronos.org/opengl/Primitive).

This file uses the older OpenGL immediate-mode style: begin a primitive group, supply vertices, and end the group. The relevant legacy functions are listed in the [OpenGL 2.1 reference](https://registry.khronos.org/OpenGL-Refpages/gl2.1/xhtml/).

## 4. File description, imports, and window size — lines 1–6

```python
"""Lab 1: graph paper with nine white pixels centered at (0, 0)."""

import sys
from OpenGL import GL, GLUT

WIDTH, HEIGHT = 960, 720
```

**Line 1 — module docstring:** The triple-quoted string describes the file's purpose. A descriptive string at the start of a module is called its **docstring**. Python stores it as documentation; it does not print it or draw it in the window.

**Line 3 — `import sys`:** Imports Python's standard `sys` module, which provides information about the running Python process. This file only uses its `argv` attribute, explained at line 80.

**Line 4 — `from OpenGL import GL, GLUT`:** Imports two modules from the `OpenGL` package. `GL` handles graphics commands; `GLUT` handles the window, callbacks, event loop, and bitmap text.

**Line 6 — `WIDTH, HEIGHT = 960, 720`:** Assigns `960` to `WIDTH` and `720` to `HEIGHT`. This is equivalent to:

```python
WIDTH = 960
HEIGHT = 720
```

The uppercase names signal that these values are intended as constants. Python does not enforce that convention: the names could still be reassigned. They are defined outside functions, so the functions can read them as module-level names.

## 5. `draw_text(x, y, text)` — lines 9–13

**Purpose:** Draw a string at a chosen position, one character at a time.

**Inputs:** `x` and `y` are the starting coordinates. `text` is the string to draw.

```python
def draw_text(x, y, text):
    GL.glColor3f(0.75, 0.75, 0.75)
    GL.glRasterPos2f(x, y)
    for character in text:
        GLUT.glutBitmapCharacter(GLUT.GLUT_BITMAP_8_BY_13, ord(character))
```

**Line 9 — `def draw_text(x, y, text):`:** Defines a function named `draw_text` with three parameters. For example, `draw_text(7, -17, "0")` gives it `x = 7`, `y = -17`, and `text = "0"` for that call.

**Line 10 — `GL.glColor3f(0.75, 0.75, 0.75)`:** Sets the current drawing color to light gray. `glColor3f(red, green, blue)` takes three floating-point color components. In this naming convention, `3` indicates three components and `f` indicates floating-point inputs.

**Line 11 — `GL.glRasterPos2f(x, y)`:** Sets the raster position used to place bitmap text. `2f` indicates two floating-point coordinates. This position goes through the current transformations; it is not an instruction to bypass the coordinate system and directly use raw window coordinates. The current color is also captured for bitmap drawing when the raster position is set, which is why line 10 comes first.

**Line 12 — `for character in text:`:** Loops over the string. If `text` is `"100"`, the values are `"1"`, `"0"`, and `"0"`. The more deeply indented line 13 runs once for each character.

**Line 13 — `GLUT.glutBitmapCharacter(...)`:** Draws one character using the selected bitmap font. `GLUT_BITMAP_8_BY_13` identifies an 8-by-13 fixed-size font. `ord(character)` converts the character to its numeric Unicode code point; the digits, minus sign, and axis letters used here have codes supported by this font. For example, `ord("0")` is `48`. The font drawing call advances the raster position, allowing the next character to follow the previous one. See [FreeGLUT font rendering](https://freeglut.sourceforge.net/docs/api.php#FontRendering).

### Build up the function's behavior

To draw `"-100"`, the function:

1. Selects light gray.
2. Selects the text's starting position.
3. Draws `"-"` using `ord("-")`, which is `45`.
4. Draws `"1"` using code `49`.
5. Draws each `"0"` using code `48`.

The function draws into the current graphics buffer. It does not print to a terminal, and it does not return the text.

## 6. `draw_grid()` — lines 16–44

**Purpose:** Draw the graph-paper lines, the two brighter axes, and their labels.

**Inputs:** None. The empty parentheses mean that callers do not pass arguments.

### 6.1 Vertical and horizontal grid lines — lines 16–25

```python
def draw_grid():
    GL.glColor3f(0.12, 0.12, 0.12)
    GL.glBegin(GL.GL_LINES)
    for x in range(-480, 480, 20):
        GL.glVertex2f(x + 0.5, -360)
        GL.glVertex2f(x + 0.5, 360)
    for y in range(-360, 360, 20):
        GL.glVertex2f(-480, y + 0.5)
        GL.glVertex2f(480, y + 0.5)
    GL.glEnd()
```

**Line 16 — `def draw_grid():`:** Defines the function. Its body runs later when `display()` calls it.

**Line 17 — `GL.glColor3f(0.12, 0.12, 0.12)`:** Selects a very dark gray for the ordinary grid lines. Equal components give gray; `0.12` makes it darker than the text and axes.

**Line 18 — `GL.glBegin(GL.GL_LINES)`:** Begins a group of independent line segments. OpenGL interprets vertices in pairs: vertices 1 and 2 form one line, vertices 3 and 4 another, and so on. It does not join every vertex into a single continuous path.

**Line 19 — `for x in range(-480, 480, 20):`:** Repeats for x values starting at `-480`, increasing by `20`, and stopping before `480`:

```text
-480, -460, -440, ..., -20, 0, 20, ..., 440, 460
```

There are 48 values, producing 48 vertical grid segments. The spacing is 20 coordinate units, which here maps to 20 framebuffer pixels.

**Line 20 — `GL.glVertex2f(x + 0.5, -360)`:** Supplies the lower endpoint of one vertical line. `glVertex2f(x, y)` supplies a two-dimensional vertex; the implicit z coordinate is `0`. The `+ 0.5` aligns the line's horizontal location with pixel centers in this mapping.

**Line 21 — `GL.glVertex2f(x + 0.5, 360)`:** Supplies the upper endpoint. Both endpoints have the same x coordinate, so the segment is vertical. With `x = 20`, the two endpoints are `(20.5, -360)` and `(20.5, 360)`.

**Line 22 — `for y in range(-360, 360, 20):`:** Starts a separate loop for y values:

```text
-360, -340, -320, ..., -20, 0, 20, ..., 320, 340
```

There are 36 values, producing 36 horizontal grid segments. This loop is aligned with the first `for`, so it runs after the vertical loop finishes; it is not nested inside it.

**Line 23 — `GL.glVertex2f(-480, y + 0.5)`:** Supplies the left endpoint of one horizontal line.

**Line 24 — `GL.glVertex2f(480, y + 0.5)`:** Supplies its right endpoint. Equal y coordinates make it horizontal. With `y = 20`, the endpoints are `(-480, 20.5)` and `(480, 20.5)`.

**Line 25 — `GL.glEnd()`:** Ends this vertex group. It matches the `glBegin` at line 18. The group contains 84 segments altogether: 48 vertical and 36 horizontal. `glEnd()` does not close the window or display the finished frame by itself.

### 6.2 Brighter axes — lines 27–34

```python
    # Draw the x and y axes brighter than the grid.
    GL.glColor3f(0.5, 0.5, 0.5)
    GL.glBegin(GL.GL_LINES)
    GL.glVertex2f(-480, 0.5)
    GL.glVertex2f(480, 0.5)
    GL.glVertex2f(0.5, -360)
    GL.glVertex2f(0.5, 360)
    GL.glEnd()
```

**Line 27 — comment:** A line beginning with `#` explains the code for human readers. Python does not execute the comment.

**Line 28 — `GL.glColor3f(0.5, 0.5, 0.5)`:** Selects medium gray. This is brighter than the grid's `0.12` components.

**Line 29 — `GL.glBegin(GL.GL_LINES)`:** Begins another independent line group, now using the brighter color.

**Line 30 — `GL.glVertex2f(-480, 0.5)`:** Supplies the left endpoint of the horizontal x axis.

**Line 31 — `GL.glVertex2f(480, 0.5)`:** Supplies its right endpoint. These two vertices form one segment.

**Line 32 — `GL.glVertex2f(0.5, -360)`:** Supplies the bottom endpoint of the vertical y axis.

**Line 33 — `GL.glVertex2f(0.5, 360)`:** Supplies its top endpoint. These two vertices form the second segment.

**Line 34 — `GL.glEnd()`:** Ends the axes group.

The mathematical axes are associated with x or y equal to zero. The actual vertices use `0.5` to put the thin axes on the pixel centers for that row and column. The earlier grid loops already drew dark lines there; these brighter lines are drawn over them.

### 6.3 Numbers and axis names — lines 36–44

```python
    for x in range(-400, 401, 100):
        if x != 0:
            draw_text(x + 3, -17, str(x))
    for y in range(-300, 301, 100):
        if y != 0:
            draw_text(7, y + 3, str(y))
    draw_text(7, -17, "0")
    draw_text(460, 7, "x")
    draw_text(7, 340, "y")
```

**Line 36 — `for x in range(-400, 401, 100):`:** Produces `-400, -300, -200, -100, 0, 100, 200, 300, 400`. The stop is `401` so that `400` is included. `range` always excludes its stop value.

**Line 37 — `if x != 0:`:** Only draws a label when x is not zero. This prevents this loop from drawing an origin label that will be handled separately.

**Line 38 — `draw_text(x + 3, -17, str(x))`:** Draws the x-axis number slightly to the right of its corresponding coordinate and below the axis. `str(x)` converts the number to text. For `x = -200`, this becomes:

```python
draw_text(-197, -17, "-200")
```

`x + 3` changes where the label is placed; it does not change the number being displayed.

**Line 39 — `for y in range(-300, 301, 100):`:** Produces `-300, -200, -100, 0, 100, 200, 300` for the y-axis labels.

**Line 40 — `if y != 0:`:** Skips zero in this loop too.

**Line 41 — `draw_text(7, y + 3, str(y))`:** Draws the y-axis number to the right of the axis and slightly above its coordinate. With `y = 200`, the call is `draw_text(7, 203, "200")`.

**Line 42 — `draw_text(7, -17, "0")`:** Draws one zero near the origin. The loops skipped zero so the origin is labeled once.

**Line 43 — `draw_text(460, 7, "x")`:** Draws the letter `x` near the positive end of the horizontal axis.

**Line 44 — `draw_text(7, 340, "y")`:** Draws the letter `y` near the positive end of the vertical axis.

### Build up `draw_grid()` in your mind

Its three stages are: dark grid, brighter axes, then labels. It calls `draw_text()` 17 times: 8 nonzero x labels, 6 nonzero y labels, the origin label, and two axis names.

## 7. `plot_pixel(x, y, red, green, blue)` — lines 47–54

**Purpose:** Draw one one-pixel point at the chosen pixel coordinate using the requested color.

**Inputs:** The first two arguments choose the position. The last three choose the RGB color.

```python
def plot_pixel(x, y, red, green, blue):
    """Draw one device pixel with RGB intensities from 0.0 to 1.0."""
    GL.glColor3f(red, green, blue)
    GL.glPointSize(1)
    GL.glBegin(GL.GL_POINTS)
    # Offset by half a unit to land at the center of a device pixel.
    GL.glVertex2f(x + 0.5, y + 0.5)
    GL.glEnd()
```

**Line 47 — function definition:** Defines five parameters. In `plot_pixel(0, 0, 1.0, 1.0, 1.0)`, the function receives x and y equal to zero and all three color components equal to one.

**Line 48 — function docstring:** Documents the function's intended behavior. It does not draw anything. The stated `0.0`–`1.0` range describes the expected color inputs; this function does not contain its own input-validation checks.

**Line 49 — `GL.glColor3f(red, green, blue)`:** Selects the supplied color. The parameter names are replaced by their current values when the call runs. Equal values of `1.0` select white.

**Line 50 — `GL.glPointSize(1)`:** Sets the point size to one framebuffer pixel. Point size is specified in pixel units rather than this program's world-coordinate units. Here, the fixed viewport/projection mapping also keeps neighboring point positions one pixel apart.

**Line 51 — `GL.glBegin(GL.GL_POINTS)`:** Begins a group of points. Each supplied vertex represents a separate point; OpenGL does not connect them with lines.

**Line 52 — comment:** Explains the half-unit offset on the next line.

**Line 53 — `GL.glVertex2f(x + 0.5, y + 0.5)`:** Supplies the position for this point. Adding `0.5` in both directions targets the center of the selected pixel in the program's one-unit-per-pixel mapping.

**Line 54 — `GL.glEnd()`:** Ends the point group. Only one vertex was supplied, so this call draws one point.

### Why add `0.5`?

Imagine one pixel cell occupying the interval from `0` to `1`. Its center is `0.5`, not `0`. With the initial viewport, the coordinate conversion is:

```text
framebuffer x = drawing x + 480
framebuffer y = drawing y + 360
```

So the integer pixel label `(0, 0)` is plotted using the vertex `(0.5, 0.5)`, which maps to framebuffer position `(480.5, 360.5)`. This is the center of framebuffer pixel column `480`, row `360`. The lower-left framebuffer corner is the reference for these row/column numbers.

The selected three columns have drawing-coordinate centers `-0.5`, `0.5`, and `1.5`; their integer labels are `-1`, `0`, and `1`. Thus “centered at `(0, 0)`” refers to the middle pixel label, while the middle submitted vertex is `(0.5, 0.5)`.

These are framebuffer pixels. A desktop's display scaling can affect how large the window image looks on the physical screen.

### Build up a white pixel call

```python
plot_pixel(0, 0, 1.0, 1.0, 1.0)
```

means: choose white, choose a size of one pixel, begin points, supply `(0.5, 0.5)`, and end points. A red example would use `plot_pixel(10, 20, 1.0, 0.0, 0.0)` inside the drawing callback, after the OpenGL window has been created.

## 8. `display()` — lines 57–66

**Purpose:** Draw one complete frame—the image that should appear in the window.

**Inputs:** None. GLUT calls it when the window needs drawing.

```python
def display():
    GL.glClear(GL.GL_COLOR_BUFFER_BIT)
    draw_grid()

    # (0, 0) and its eight neighbors: exactly nine white pixels.
    for x in range(-1, 2):
        for y in range(-1, 2):
            plot_pixel(x, y, 1.0, 1.0, 1.0)

    GLUT.glutSwapBuffers()
```

**Line 57 — `def display():`:** Defines the complete-frame drawing function. Its name is chosen by the programmer; registering it at line 89 makes it the display callback.

**Line 58 — `GL.glClear(GL.GL_COLOR_BUFFER_BIT)`:** Clears the color buffer using the clear color chosen at line 86: black. A **buffer** here is storage for an image. The constant identifies which buffer to clear. Clearing removes the previous frame's colors before a new frame is drawn. Under the settings used here, clearing covers the drawable buffer, including margins outside the viewport.

**Line 59 — `draw_grid()`:** Calls the earlier function to draw the grid, axes, and labels. Execution returns here when `draw_grid()` finishes.

**Line 61 — comment:** Explains that the following loops select the origin pixel and its eight neighbors.

**Line 62 — `for x in range(-1, 2):`:** Gives x the values `-1`, `0`, and `1`. It never gives x the value `2`, because the stop is excluded.

**Line 63 — `for y in range(-1, 2):`:** Creates an inner loop, shown by the extra indentation. For each individual x value, y runs through all three values `-1`, `0`, and `1` again.

**Line 64 — `plot_pixel(x, y, 1.0, 1.0, 1.0)`:** Draws a white pixel for the current pair. The line belongs to both loops, so it runs `3 × 3 = 9` times.

The exact call order is:

| Call | x | y | Pixel label |
|---|---:|---:|---|
| 1 | -1 | -1 | `(-1, -1)` |
| 2 | -1 | 0 | `(-1, 0)` |
| 3 | -1 | 1 | `(-1, 1)` |
| 4 | 0 | -1 | `(0, -1)` |
| 5 | 0 | 0 | `(0, 0)` |
| 6 | 0 | 1 | `(0, 1)` |
| 7 | 1 | -1 | `(1, -1)` |
| 8 | 1 | 0 | `(1, 0)` |
| 9 | 1 | 1 | `(1, 1)` |

**Line 66 — `GLUT.glutSwapBuffers()`:** Presents the completed frame through the double-buffered window. The **front buffer** is the displayed image; the **back buffer** is where the new image is prepared. Swapping presents the prepared image after drawing finishes. See [FreeGLUT display functions](https://freeglut.sourceforge.net/docs/api.php#Display).

### Why does drawing order matter?

The program clears first, draws the grid second, and plots white points third. Under this program's settings, later drawing replaces earlier colors where they overlap. The white pixels therefore appear over the gray axes/grid. Clearing last would erase the drawing.

`display()` contains no animation loop. GLUT may call it more than once—for example, after the window needs redisplaying—but each call draws the same image.

## 9. `reshape(width, height)` — lines 69–76

**Purpose:** Set the mapping between drawing coordinates and the window's pixels. Keep the drawing canvas at a fixed size as the window changes size.

**Inputs:** `width` and `height` describe the current drawable window size supplied to the function. `main()` also calls it once explicitly with `960` and `720`.

```python
def reshape(width, height):
    # Keep one coordinate unit equal to one device pixel when resized.
    GL.glViewport((width - WIDTH) // 2, (height - HEIGHT) // 2, WIDTH, HEIGHT)
    GL.glMatrixMode(GL.GL_PROJECTION)
    GL.glLoadIdentity()
    GL.glOrtho(-480, 480, -360, 360, -1, 1)
    GL.glMatrixMode(GL.GL_MODELVIEW)
    GL.glLoadIdentity()
```

**Line 69 — function definition:** Defines two parameters. Lowercase `width`/`height` are the current dimensions for this call. Uppercase `WIDTH`/`HEIGHT` remain the fixed canvas dimensions. Python names are case-sensitive.

**Line 70 — comment:** States the intended fixed scale: one drawing-coordinate unit maps to one framebuffer pixel.

**Line 71 — `GL.glViewport(...)`:** Sets the rectangle used to map projected coordinates into window pixels. Its argument order is `glViewport(left, bottom, viewport_width, viewport_height)`. The lower-left origin is described in the [OpenGL viewport specification, section 2.10.1](https://registry.khronos.org/OpenGL/specs/gl/glspec121.pdf).

Here the four arguments are:

```text
left            = (width  - 960) // 2
bottom          = (height - 720) // 2
viewport_width  = 960
viewport_height = 720
```

`//` is **floor division**: divide, then round downward to a whole integer. For example, `241 // 2` is `120`, while `-241 // 2` is `-121`. Using integers is appropriate for the viewport's pixel offsets.

Subtracting the canvas dimensions finds the extra space; dividing by two distributes it on opposite sides. When a difference is odd, the sides differ by one pixel.

| Current window | Left offset | Bottom offset | Result |
|---|---:|---:|---|
| 960×720 | 0 | 0 | Canvas fills the drawable window |
| 1200×900 | 120 | 90 | Canvas stays 960×720, with margins |
| 800×600 | -80 | -60 | Canvas stays 960×720, with outer parts clipped |

The viewport's size stays fixed even when its position changes. The grid does not stretch to fill a larger window. Making the window smaller hides the outer portions of the drawing rather than shrinking it.

**Line 72 — `GL.glMatrixMode(GL.GL_PROJECTION)`:** Selects the projection matrix as the target of subsequent matrix operations. A **matrix** is a table of numbers used for coordinate transformations. A **projection** determines how a coordinate space is mapped into the visible view. You do not need matrix algebra to follow this setup.

**Line 73 — `GL.glLoadIdentity()`:** Resets the selected projection matrix to the **identity matrix**, a transformation that leaves coordinates unchanged. This removes the previous projection before a fresh one is applied. Without resetting, repeated calls to `glOrtho()` would multiply additional transformations onto the old one.

**Line 74 — `GL.glOrtho(-480, 480, -360, 360, -1, 1)`:** Applies an **orthographic projection**. Its parameters are `left, right, bottom, top, near, far`:

| Argument | Value | Meaning here |
|---|---:|---|
| left | -480 | Left coordinate boundary |
| right | 480 | Right coordinate boundary |
| bottom | -360 | Bottom coordinate boundary |
| top | 360 | Top coordinate boundary |
| near | -1 | Near clipping-plane distance |
| far | 1 | Far clipping-plane distance |

Orthographic projection keeps parallel lines parallel and does not make distant objects appear smaller. All the two-dimensional vertices here have implicit z equal to zero, which is within this depth setup. The first four arguments establish the useful 2D drawing area.

Because the horizontal span is `480 - (-480) = 960` units and the viewport width is 960 pixels, the horizontal scale is one pixel per unit. The vertical calculation is `360 - (-360) = 720` units across 720 pixels, also one pixel per unit.

**Line 75 — `GL.glMatrixMode(GL.GL_MODELVIEW)`:** Selects the model-view matrix. It is the transformation used for positioning objects and the viewing coordinate system before projection. Switching the mode does not itself move or draw anything.

**Line 76 — `GL.glLoadIdentity()`:** Resets that model-view matrix, so this program does not apply an additional translation, rotation, or scaling to its supplied vertices.

### Build up `reshape()` in your mind

The viewport chooses the fixed pixel rectangle. The projection chooses the coordinate boundaries. The identity model-view leaves the supplied positions unchanged before projection. Together, these settings produce the one-unit-per-pixel mapping.

The function does not itself redraw the grid or points. It prepares the mapping used by the drawing callback.

## 10. `main()` — lines 79–91

**Purpose:** Initialize the toolkit, create the window, set initial graphics settings, register callbacks, and start event processing.

**Inputs:** None.

```python
def main():
    GLUT.glutInit([sys.argv[0]])
    GLUT.glutInitDisplayMode(GLUT.GLUT_DOUBLE | GLUT.GLUT_RGB)
    GLUT.glutInitWindowSize(WIDTH, HEIGHT)
    GLUT.glutCreateWindow(b"Lab 1 - White 3x3 Pixels at the Origin")
    GLUT.glutSetOption(GLUT.GLUT_ACTION_ON_WINDOW_CLOSE,
                       GLUT.GLUT_ACTION_GLUTMAINLOOP_RETURNS)
    GL.glClearColor(0.0, 0.0, 0.0, 1.0)
    GL.glDisable(GL.GL_DITHER)
    reshape(WIDTH, HEIGHT)
    GLUT.glutDisplayFunc(display)
    GLUT.glutReshapeFunc(reshape)
    GLUT.glutMainLoop()
```

**Line 79 — `def main():`:** Defines the setup function. `main` is a conventional name, not a Python keyword. Python runs it because line 95 explicitly calls it.

**Line 80 — `GLUT.glutInit([sys.argv[0]])`:** Initializes GLUT. `sys.argv` is a list of command-line arguments. Index `[0]` selects the first item, normally the script's name or path when launched as a script. The outer brackets create a new one-item list:

```python
# Illustrative values:
sys.argv = ["pixel_plotter.py", "extra_argument"]
sys.argv[0]               # "pixel_plotter.py"
[sys.argv[0]]             # ["pixel_plotter.py"]
```

The actual code passes only that first item to GLUT, not every command-line argument. The example assignment above is just a demonstration; it is not performed in the original program.

**Line 81 — `GLUT.glutInitDisplayMode(GLUT.GLUT_DOUBLE | GLUT.GLUT_RGB)`:** Requests a double-buffered RGB window. `GLUT_DOUBLE` selects double buffering; `GLUT_RGB` selects the RGB color mode. The `|` operator is **bitwise OR**, used here to combine toolkit mode flags in one argument. It is neither a loop nor Python's logical `or` keyword. These mode flags are established by the toolkit; their numeric bit patterns need not be memorized.

**Line 82 — `GLUT.glutInitWindowSize(WIDTH, HEIGHT)`:** Requests the initial drawable size of 960×720 pixels for the window that will be created. This sets the requested size; it does not create the window yet. The title bar and borders are outside the drawable area.

**Line 83 — `GLUT.glutCreateWindow(b"Lab 1 - White 3x3 Pixels at the Origin")`:** Creates the graphics window and its OpenGL context. A **context** contains the OpenGL state associated with graphics work. The prefix `b` makes a **bytes literal**, suitable for passing this title to the underlying native library. The displayed title does not include the `b` or quotation marks. The call returns a window identifier, but this program does not store it.

**Line 84 — `GLUT.glutSetOption(GLUT.GLUT_ACTION_ON_WINDOW_CLOSE,`:** Begins a two-argument call that chooses the window-close behavior. The comma separates the first argument from the second.

**Line 85 — `GLUT.GLUT_ACTION_GLUTMAINLOOP_RETURNS)`:** Supplies the option value and closes the call. The open parenthesis lets one Python statement continue onto the next physical line. With this FreeGLUT option, closing the window permits the main loop to return to its caller. This extension is documented in [FreeGLUT event processing](https://freeglut.sourceforge.net/docs/api.php#EventProcessing).

**Line 86 — `GL.glClearColor(0.0, 0.0, 0.0, 1.0)`:** Sets the color that `glClear()` will use. Its four components are red, green, blue, and **alpha**. RGB zeros select black. Alpha `1.0` represents full opacity, but this call alone does not enable blending or make the operating-system window transparent. It sets a clearing value; the actual clearing happens in `display()`.

**Line 87 — `GL.glDisable(GL.GL_DITHER)`:** Turns off OpenGL color dithering. Dithering can vary neighboring pixel colors to approximate colors on a framebuffer with limited color precision. Disabling it avoids that color adjustment for this pixel-focused exercise. It does not disable the grid or change the point count.

**Line 88 — `reshape(WIDTH, HEIGHT)`:** Calls the program's own function immediately to establish the initial viewport and coordinate mapping. This is now possible because the window and context have been created.

**Line 89 — `GLUT.glutDisplayFunc(display)`:** Registers `display` as the function GLUT should call when drawing is needed. A function registered for later invocation is a **callback**.

Notice the difference:

```python
display()                       # Call it immediately.
GLUT.glutDisplayFunc(display)    # Pass the function for GLUT to call later.
```

Passing `display()` to the registration call would immediately draw and pass its result, `None`, rather than passing the function.

**Line 90 — `GLUT.glutReshapeFunc(reshape)`:** Registers `reshape` as the callback for window-size changes. GLUT supplies the width and height when invoking it; the programmer does not supply those arguments in the registration call.

**Line 91 — `GLUT.glutMainLoop()`:** Starts the event loop, which processes window events and invokes registered callbacks. Control generally stays inside this call while the window is open. After the window closes and the loop returns under the chosen option, `main()` has no remaining statements and finishes.

### Build up `main()` in your mind

The order matters: initialize the toolkit, choose the window format and size, create the context, configure graphics, register callbacks, and enter the event loop. OpenGL drawing requires an appropriate current context; defining the drawing functions earlier is fine because their bodies have not run yet.

## 11. The entry-point check — lines 94–95

```python
if __name__ == "__main__":
    main()
```

**Line 94 — `if __name__ == "__main__":`:** Checks whether Python is running this file as the top-level program. `__name__` is a special module variable set by Python. When the file is executed directly, its value is `"__main__"`. When another program imports it as a module, its value is the module name instead.

**Line 95 — `main()`:** Calls the setup function if the check is true. This is the point that starts the window application during a direct script run.

For example:

```powershell
python .\Lab1\pixel_plotter.py
```

runs the file directly, so the check succeeds. By contrast, importing the module makes its definitions available without automatically executing this guarded `main()` call. The module-level imports and assignments still execute during import.

## 12. Every blank line accounted for

The original file's blank lines are **2, 5, 7–8, 14–15, 26, 35, 45–46, 55–56, 60, 65, 67–68, 77–78, and 92–93**. They separate functions or stages to make the source easier to read. They do not call a function, draw anything, or add another loop iteration.

All other original lines are explained above, including the docstrings, comments, and the continuation at line 85.

## 13. Python built-in functions and syntax reference

### `range()` — generate a sequence of integers

The forms used here are:

```python
range(start, stop)
range(start, stop, step)
```

`start` is included, `stop` is excluded, and the default step is `1`. A range object supplies values for a loop without building a list of all those values. See [Python's range documentation](https://docs.python.org/3/library/stdtypes.html#range).

| Expression from the file | Values |
|---|---|
| `range(-1, 2)` | `-1, 0, 1` |
| `range(-400, 401, 100)` | `-400, -300, ..., 300, 400` |
| `range(-300, 301, 100)` | `-300, -200, ..., 200, 300` |
| `range(-480, 480, 20)` | `-480, -460, ..., 440, 460` |
| `range(-360, 360, 20)` | `-360, -340, ..., 320, 340` |

### `ord()` — a character to its numeric code

```python
ord("0")   # 48
ord("x")   # 120
ord("-")   # 45
```

It takes one character and returns its Unicode code point. Here that integer identifies the glyph passed to `glutBitmapCharacter()`. See [Python's `ord` documentation](https://docs.python.org/3/library/functions.html#ord).

### `str()` — a value to text

```python
str(-100)  # "-100"
str(200)   # "200"
```

`str` is Python's string type, used here as a conversion callable. It lets `draw_text()` iterate over the characters of a coordinate label. The integer `200` is a number; the string `"200"` contains three characters. See [Python's `str` documentation](https://docs.python.org/3/library/functions.html#func-str).

### Other syntax used in the file

| Syntax | Meaning | Example |
|---|---|---|
| `def` | Define a function | `def display():` |
| `for ... in ...` | Repeat for each supplied item | `for x in range(-1, 2):` |
| `if` | Conditionally run a block | `if x != 0:` |
| `=` | Assign a value | `WIDTH = 960` |
| `==` | Test equality | `__name__ == "__main__"` |
| `!=` | Test inequality | `x != 0` |
| `+` | Add numbers | `x + 0.5` |
| `-` | Subtract, or mark a negative number | `width - WIDTH`, `-480` |
| `//` | Floor division | `(width - WIDTH) // 2` |
| `|` | Bitwise OR, used to combine flags | `GLUT_DOUBLE | GLUT_RGB` |
| `name(...)` | Call a function | `draw_grid()` |
| `[...]` | Create a list, or index an object | `[sys.argv[0]]`, `sys.argv[0]` |
| `.` | Access a module's attribute | `GL.glEnd`, `sys.argv` |
| `#` | Start a comment | `# Draw the x and y axes...` |
| `"""..."""` | A triple-quoted string; used here for docstrings | Line 48 |
| `b"..."` | A bytes literal | Window title at line 83 |

Keywords such as `def`, `for`, and `if` are language syntax, not built-in functions that you can call with arguments.

## 14. Library-call reference

These are library calls, not functions the file implements. Their role in this program is:

| Call | Role |
|---|---|
| `GL.glColor3f(r, g, b)` | Select the color used for subsequent drawing |
| `GL.glRasterPos2f(x, y)` | Set the transformed starting position for bitmap text |
| `GLUT.glutBitmapCharacter(font, code)` | Draw one character in a bitmap font |
| `GL.glBegin(mode)` | Start a primitive group |
| `GL.glVertex2f(x, y)` | Supply a vertex in that group |
| `GL.glEnd()` | End the primitive group |
| `GL.glPointSize(size)` | Set point size in framebuffer pixels |
| `GL.glClear(mask)` | Clear the selected image buffer |
| `GLUT.glutSwapBuffers()` | Present the frame prepared with double buffering |
| `GL.glViewport(x, y, w, h)` | Set the projected drawing rectangle in pixel coordinates |
| `GL.glMatrixMode(mode)` | Select the matrix affected by later matrix calls |
| `GL.glLoadIdentity()` | Reset the selected matrix |
| `GL.glOrtho(l, r, b, t, n, f)` | Apply the orthographic projection |
| `GLUT.glutInit(arguments)` | Initialize the toolkit |
| `GLUT.glutInitDisplayMode(mode)` | Request the window's color/buffering mode |
| `GLUT.glutInitWindowSize(w, h)` | Request the initial drawable window dimensions |
| `GLUT.glutCreateWindow(title)` | Create the window and OpenGL context |
| `GLUT.glutSetOption(option, value)` | Configure the toolkit's close behavior here |
| `GL.glClearColor(r, g, b, a)` | Set the value used when clearing the color buffer |
| `GL.glDisable(capability)` | Disable the named graphics feature |
| `GLUT.glutDisplayFunc(function)` | Register the drawing callback |
| `GLUT.glutReshapeFunc(function)` | Register the resize callback |
| `GLUT.glutMainLoop()` | Process events and invoke callbacks |

The detailed explanations for these calls appear beside the original lines above. For additional library reference material, use the [Khronos OpenGL reference](https://registry.khronos.org/OpenGL-Refpages/) and [FreeGLUT API reference](https://freeglut.sourceforge.net/docs/api.php).

## 15. How the whole program runs

Reading a file from top to bottom is different from the order in which its function bodies are later executed:

1. Python imports `sys`, `GL`, and `GLUT`.
2. Python assigns the fixed width and height.
3. Python defines the six functions without running their bodies.
4. The entry-point check succeeds for a direct script run and calls `main()`.
5. `main()` creates the window, configures graphics, and calls `reshape(960, 720)`.
6. `main()` registers callbacks and enters `glutMainLoop()`.
7. GLUT invokes the callbacks as required. `display()` clears the buffer, calls `draw_grid()`, calls `plot_pixel()` nine times, and swaps buffers.
8. During `draw_grid()`, `draw_text()` is called to render the labels.
9. When the drawable window size changes, GLUT calls `reshape()` with the new dimensions. Drawing then uses that mapping.
10. Closing the window lets the main loop return; `main()` and the script finish.

The event system determines the exact callback timing, including the initial resize/display notifications. The list above explains the overall flow rather than promising a particular ordering of every operating-system event.

```text
Direct script execution
    |
    v
main()
    |-- initialize toolkit and create window
    |-- reshape(WIDTH, HEIGHT)
    |-- register callbacks
    `-- glutMainLoop()
            |-- drawing needed --> display()
            |                         |-- clear background
            |                         |-- draw_grid()
            |                         |      `-- draw_text() for labels
            |                         |-- plot_pixel() nine times
            |                         `-- swap buffers
            |-- size changes --> reshape(width, height)
            `-- window closes --> return from loop
```

## 16. Small practice changes to help you learn

These are optional experiments you can make after understanding the original code. They have not been applied to `pixel_plotter.py`.

### Make the nine pixels red

Change the color arguments in the call inside `display()`:

```python
plot_pixel(x, y, 1.0, 0.0, 0.0)
```

The loops still choose nine positions; only the color changes.

### Make a 5×5 block

Use five values for each coordinate:

```python
for x in range(-2, 3):
    for y in range(-2, 3):
        plot_pixel(x, y, 1.0, 1.0, 1.0)
```

Each loop supplies `-2, -1, 0, 1, 2`, giving `5 × 5 = 25` white pixels.

### Move the original block

Keep the original loops and shift the arguments:

```python
plot_pixel(x + 100, y + 50, 1.0, 1.0, 1.0)
```

The middle pixel label becomes `(100, 50)`: 100 units right and 50 units up from the original middle pixel.

### Change grid spacing

Change the step in both grid ranges from `20` to `40`. The spacing doubles and fewer grid lines are drawn. Changing the number-label loops is a separate decision because those currently use a step of `100`.

### Predict before you change

Try answering these from the explanations:

- Why does `range(-1, 2)` give three values?
- Why do the nested loops draw nine points instead of six?
- What would happen if clearing occurred after plotting?
- Why is `str(x)` needed for the coordinate labels?
- Why is `display` passed without parentheses when registering the callback?
- Why does enlarging the window add margins instead of enlarging the white block?

Answers: the stop value is excluded; each of three x values is paired with all three y values; clearing would erase the drawing; the label must be text that can be iterated character by character; GLUT needs the function itself to call later; the viewport and coordinate spans stay fixed.

## 17. Running this project's version

From the project directory, the existing launcher can be used:

```powershell
.\Lab1\run.ps1
```

Or use the project-local Python environment described in `Lab1/README.md`:

```powershell
& .\.venv\Scripts\python.exe .\Lab1\pixel_plotter.py
```

The code depends on PyOpenGL and a GLUT/FreeGLUT implementation. This section records the existing project's launch commands; creating this guide does not install packages or launch the graphics window.

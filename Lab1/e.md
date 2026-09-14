This program opens a black window, draws graph-paper lines and labeled axes, and draws **nine white pixels centered at (0, 0)**.

The code is in [pixel_plotter.py](</F:/Windows/Local_Disk_D/DUCSE/4th year/4-2/Computer_Graphics/Computer-Graphics/Lab1/pixel_plotter.py>).

Before reading the code, you need a few basic ideas:

- A **pixel** is one tiny square of color in a drawing area.
- A **coordinate** such as `(100, 50)` tells us where to draw something.
- A **function** is a named group of instructions. Defining a function saves those instructions; calling it runs them.
- A **library** is code written by other people that our program can use.
- In Python, **indentation**—the spaces before a line—shows which instructions belong to a function, loop, or condition.

Blank lines make the code easier to read. Lines starting with `#` are comments for people; Python does not execute them.

Let’s go through the file in order.

**Lines 1–6: description, libraries, and window size**

```python
"""Lab 1: graph paper with nine white pixels centered at (0, 0)."""
```

This is a **docstring**: a description enclosed in three quotation marks. It explains what the file does.

```python
import sys
```

This loads Python’s built-in `sys` library. We use it later to get the program’s name.

```python
from OpenGL import GL, GLUT
```

This loads two parts of the installed OpenGL library:

| Name | Its job in this program |
|---|---|
| `GL` | Draw colors, points, and lines; configure coordinates |
| `GLUT` | Create the window, draw text, and manage window events |

When you see:

```python
GL.glColor3f(...)
```

the dot means “use the `glColor3f` function that belongs to `GL`.”

```python
WIDTH, HEIGHT = 960, 720
```

This assigns two values:

```python
WIDTH = 960
HEIGHT = 720
```

Our drawing area is **960 pixels wide and 720 pixels high**.

These names are uppercase because they represent fixed settings that we intend to keep unchanged.

---

**Lines 9–13: `draw_text()` writes a label**

```python
def draw_text(x, y, text):
```

`def` means “define a function.”

The function’s name is `draw_text`. It accepts three **parameters**, which are values supplied when calling it:

- `x`: horizontal position.
- `y`: vertical position.
- `text`: the words or numbers to write.

For example:

```python
draw_text(7, -17, "0")
```

means “write the text `0` at the position `(7, -17)`.”

```python
GL.glColor3f(0.75, 0.75, 0.75)
```

This sets the color for drawing that follows.

The three numbers represent **red, green, and blue**, usually called **RGB**. Here, each number ranges from `0.0` to `1.0`.

| RGB values | Color |
|---|---|
| `(0.0, 0.0, 0.0)` | Black |
| `(1.0, 1.0, 1.0)` | White |
| `(1.0, 0.0, 0.0)` | Red |
| `(0.0, 1.0, 0.0)` | Green |
| `(0.0, 0.0, 1.0)` | Blue |
| `(0.75, 0.75, 0.75)` | Light gray |

Equal amounts of red, green, and blue produce gray.

In `glColor3f`, `3` means three color components, and `f` means the function accepts floating-point numbers—numbers that can have a decimal part.

**Setting a color does not draw anything yet.** It tells OpenGL which color to use for upcoming drawing commands.

```python
GL.glRasterPos2f(x, y)
```

This sets the starting position for drawing the text.

You can think of it as placing a text cursor at `(x, y)`.

The `2f` means two floating-point coordinates: x and y.

```python
for character in text:
```

This starts a **loop**, which repeats instructions.

It takes the text one character at a time. For `"100"`, the loop handles:

```text
"1"
"0"
"0"
```

```python
GLUT.glutBitmapCharacter(GLUT.GLUT_BITMAP_8_BY_13, ord(character))
```

This draws the current character.

The two arguments are:

- `GLUT.GLUT_BITMAP_8_BY_13`: a small font with 8×13 character cells.
- `ord(character)`: converts the character into its numeric character code.

For example:

```python
ord("A")
```

produces `65`.

After drawing each character, GLUT advances the text position so the next character appears beside it.

---

**Lines 16–44: `draw_grid()` draws the graph paper and axes**

```python
def draw_grid():
```

This defines a function named `draw_grid`.

Its empty parentheses mean it does not need any parameters.

```python
GL.glColor3f(0.12, 0.12, 0.12)
```

This selects dark gray for the graph-paper lines.

The background is black, so these gray lines will be visible without being too bright.

```python
GL.glBegin(GL.GL_LINES)
```

This tells OpenGL:

“Start receiving the endpoints of lines.”

A line needs two endpoints. In `GL_LINES` mode, OpenGL treats each pair of supplied points as a separate line.

For example:

```text
First point + second point → first line
Third point + fourth point → second line
```

```python
for x in range(-480, 480, 20):
```

This repeats the following instructions for different x positions.

Python’s `range(start, stop, step)` works like this:

- Start at `-480`.
- Increase by `20` each time.
- Stop before reaching `480`.

So x takes these values:

```text
-480, -460, -440, ..., 0, 20, ..., 460
```

**The stop value is excluded.**

```python
GL.glVertex2f(x + 0.5, -360)
GL.glVertex2f(x + 0.5, 360)
```

These two lines supply the endpoints of a vertical line.

Both endpoints have the same x coordinate. Their y coordinates extend from the bottom of the drawing area to the top.

For example, when `x` is `100`, the endpoints are:

```text
(100.5, -360)
(100.5,  360)
```

The extra `0.5` aligns the line with the centers of device pixels. We will look at that more closely in `plot_pixel()`.

```python
for y in range(-360, 360, 20):
```

This starts another loop, now for horizontal lines.

The y values are:

```text
-360, -340, -320, ..., 0, 20, ..., 340
```

```python
GL.glVertex2f(-480, y + 0.5)
GL.glVertex2f(480, y + 0.5)
```

These supply the endpoints of a horizontal line.

Both endpoints have the same y coordinate, while x extends from the left edge to the right edge.

```python
GL.glEnd()
```

This ends the group of line-drawing instructions started by `glBegin()`.

Now the ordinary grid lines have been submitted.

```python
# Draw the x and y axes brighter than the grid.
```

This comment explains the next part.

```python
GL.glColor3f(0.5, 0.5, 0.5)
```

This changes the drawing color to a brighter gray for the axes.

It affects the next lines drawn, without changing the grid lines already drawn.

```python
GL.glBegin(GL.GL_LINES)
```

This starts another group of lines.

```python
GL.glVertex2f(-480, 0.5)
GL.glVertex2f(480, 0.5)
```

These endpoints draw the horizontal **x-axis**, aligned with the row of pixels representing `y = 0`.

```python
GL.glVertex2f(0.5, -360)
GL.glVertex2f(0.5, 360)
```

These endpoints draw the vertical **y-axis**, aligned with the column representing `x = 0`.

```python
GL.glEnd()
```

This finishes drawing the axes.

Next, we add numbers.

```python
for x in range(-400, 401, 100):
```

This produces:

```text
-400, -300, -200, -100, 0, 100, 200, 300, 400
```

The stop value is `401` so that `400` is included.

```python
if x != 0:
```

`if` means “execute the indented instructions only when this condition is true.”

`!=` means “is not equal to.”

So this says:

“Draw a label if x is not zero.”

We skip zero because it will get its own label later.

```python
draw_text(x + 3, -17, str(x))
```

This calls the text function we defined earlier.

- `x + 3` puts the label slightly to the right of its grid position.
- `-17` places it below the x-axis.
- `str(x)` converts the number into text.

For example:

```python
str(-100)
```

produces the text `"-100"`.

```python
for y in range(-300, 301, 100):
```

This produces y-axis label positions:

```text
-300, -200, -100, 0, 100, 200, 300
```

```python
if y != 0:
```

Again, skip zero because we will draw it separately.

```python
draw_text(7, y + 3, str(y))
```

This writes the y value:

- Slightly to the right of the y-axis, at x = `7`.
- Slightly above its grid position, at y + `3`.

```python
draw_text(7, -17, "0")
```

This writes the origin label `0` near the axes’ intersection.

```python
draw_text(460, 7, "x")
```

This writes `x` near the right end of the x-axis.

```python
draw_text(7, 340, "y")
```

This writes `y` near the upper end of the y-axis.

---

**Lines 47–54: `plot_pixel()` draws one pixel**

```python
def plot_pixel(x, y, red, green, blue):
```

This defines a function that accepts a position and a color.

For example:

```python
plot_pixel(0, 0, 1.0, 1.0, 1.0)
```

means “draw a white pixel at `(0, 0)`.”

```python
"""Draw one device pixel with RGB intensities from 0.0 to 1.0."""
```

This docstring describes the function and the expected color values.

```python
GL.glColor3f(red, green, blue)
```

This selects the supplied color.

```python
GL.glPointSize(1)
```

This sets the point size to one device pixel.

```python
GL.glBegin(GL.GL_POINTS)
```

This tells OpenGL that the positions supplied next represent individual points.

Unlike `GL_LINES`, each supplied position represents a separate point.

```python
# Offset by half a unit to land at the center of a device pixel.
```

This comment explains the next line.

```python
GL.glVertex2f(x + 0.5, y + 0.5)
```

This supplies the point’s position.

Why add `0.5`?

With our projection, the device pixel identified as `(0, 0)` occupies the small area between coordinate edges `0` and `1` in both directions. Its center is:

```text
(0.5, 0.5)
```

Therefore:

```python
plot_pixel(0, 0, ...)
```

places the drawing point at `(0.5, 0.5)`, inside the center of that pixel.

This avoids placing the point exactly on a boundary between pixels.

**The pixel we call `(0, 0)` is still the intended center pixel.** The half-unit offset is how we place the OpenGL point inside it.

```python
GL.glEnd()
```

This finishes the point-drawing instructions.

---

**Lines 57–66: `display()` draws the complete picture**

```python
def display():
```

This defines the function that draws the window’s contents.

```python
GL.glClear(GL.GL_COLOR_BUFFER_BIT)
```

This clears the drawing buffer using the background color configured later in `main()`.

A **buffer** is a region of memory that holds the image being drawn.

`GL_COLOR_BUFFER_BIT` tells OpenGL to clear the stored pixel colors.

In this program, clearing produces a black background.

```python
draw_grid()
```

This calls `draw_grid()` to draw the graph-paper lines, axes, and labels.

```python
# (0, 0) and its eight neighbors: exactly nine white pixels.
```

This comment describes the two loops below.

```python
for x in range(-1, 2):
```

This gives x three values:

```text
-1, 0, 1
```

Remember: `2` is excluded.

```python
for y in range(-1, 2):
```

For **each x value**, this inner loop gives y three values:

```text
-1, 0, 1
```

These are **nested loops**: one loop inside another.

```python
plot_pixel(x, y, 1.0, 1.0, 1.0)
```

This draws a white pixel for each coordinate pair.

The loops produce all these positions:

| | x = −1 | x = 0 | x = 1 |
|---|---|---|---|
| **y = 1** | (−1, 1) | (0, 1) | (1, 1) |
| **y = 0** | (−1, 0) | **(0, 0)** | (1, 0) |
| **y = −1** | (−1, −1) | (0, −1) | (1, −1) |

Three x values multiplied by three y values gives:

```text
3 × 3 = 9 white pixels
```

The middle pixel is `(0, 0)`.

We draw these pixels **after the grid**, so the white pixels cover the grid or axes underneath them.

```python
GLUT.glutSwapBuffers()
```

This displays the completed picture.

The program uses two buffers:

- The **front buffer** holds the picture currently displayed.
- The **back buffer** holds the picture being drawn.

We draw into the back buffer, then swap the buffers to show the completed image. This helps avoid showing a partly drawn picture.

---

**Lines 69–76: `reshape()` configures the drawing coordinates**

```python
def reshape(width, height):
```

This defines a function that receives the window’s current width and height.

GLUT calls it when the drawing area changes size. We also call it ourselves during startup.

```python
# Keep one coordinate unit equal to one device pixel when resized.
```

This explains why we keep a fixed drawing area.

```python
GL.glViewport((width - WIDTH) // 2, (height - HEIGHT) // 2, WIDTH, HEIGHT)
```

A **viewport** is the rectangular area of the window where OpenGL maps the drawing.

Its four arguments mean:

```python
GL.glViewport(left, bottom, drawing_width, drawing_height)
```

In our code:

- `(width - WIDTH) // 2` calculates the left margin.
- `(height - HEIGHT) // 2` calculates the bottom margin.
- `WIDTH` keeps the drawing width at `960`.
- `HEIGHT` keeps the drawing height at `720`.

`//` is floor division. For example:

```python
200 // 2
```

gives `100`.

If the window becomes `1160` pixels wide:

```text
Left margin = (1160 − 960) // 2 = 100
```

So the original drawing area stays centered.

A larger window adds margins. A smaller window clips part of the drawing.

```python
GL.glMatrixMode(GL.GL_PROJECTION)
```

This selects the **projection matrix**.

A matrix is a table of numbers that OpenGL uses to transform coordinates. Here, you can think of the projection as the setting that decides which coordinate region is visible.

This line selects the setting we are about to change.

```python
GL.glLoadIdentity()
```

This resets the selected matrix to its starting state.

It removes any previous transformation before we configure the projection.

```python
GL.glOrtho(-480, 480, -360, 360, -1, 1)
```

This creates an **orthographic projection**.

An orthographic projection maps coordinates without perspective effects—objects do not appear smaller just because they are farther away.

The six arguments mean:

```text
left, right, bottom, top, near, far
```

For our program:

| Boundary | Value |
|---|---:|
| Left | −480 |
| Right | 480 |
| Bottom | −360 |
| Top | 360 |
| Near depth boundary | −1 |
| Far depth boundary | 1 |

The visible coordinate region is:

```text
Width:  480 − (−480) = 960 units
Height: 360 − (−360) = 720 units
```

That matches our viewport size, making **one coordinate unit correspond to one device pixel**.

The projection bounds describe the drawing area’s edges. The integer pixel coordinates are x = `−480…479` and y = `−360…359`.

We are drawing a flat image at z = `0`, so you do not need to work with depth yet.

```python
GL.glMatrixMode(GL.GL_MODELVIEW)
```

This selects the **model-view matrix**.

That matrix can move, rotate, or scale the objects being drawn.

```python
GL.glLoadIdentity()
```

This resets it so we apply no movement, rotation, or scaling.

Our supplied coordinates can therefore pass through unchanged before projection.

---

**Lines 79–91: `main()` sets up and runs the application**

```python
def main():
```

This defines the function that starts the graphics application.

```python
GLUT.glutInit([sys.argv[0]])
```

This initializes GLUT so we can use its window functions.

Breaking down the argument:

- `sys.argv` contains the program name and command-line arguments.
- `[0]` selects the first item, normally the program name.
- The outer brackets create a list containing that one item.

So GLUT receives a list containing the program’s name.

```python
GLUT.glutInitDisplayMode(GLUT.GLUT_DOUBLE | GLUT.GLUT_RGB)
```

This selects the window’s drawing mode.

- `GLUT_DOUBLE` requests two buffers.
- `GLUT_RGB` requests RGB color.

The `|` symbol combines these option flags so both are requested.

```python
GLUT.glutInitWindowSize(WIDTH, HEIGHT)
```

This requests an initial drawing area of `960 × 720` pixels.

```python
GLUT.glutCreateWindow(b"Lab 1 - White 3x3 Pixels at the Origin")
```

This creates the window and gives it a title.

The `b` before the quotation marks makes the text a **byte string**, which this GLUT function expects.

Creating the window also creates an **OpenGL context**: the drawing environment that OpenGL needs before its drawing commands can work.

```python
GLUT.glutSetOption(GLUT.GLUT_ACTION_ON_WINDOW_CLOSE,
                   GLUT.GLUT_ACTION_GLUTMAINLOOP_RETURNS)
```

This is one instruction written across two lines.

It configures what happens when you close the window: GLUT stops its main loop and returns control to our Python program.

Since no more work follows the loop, the program finishes.

```python
GL.glClearColor(0.0, 0.0, 0.0, 1.0)
```

This selects the color used whenever `glClear()` clears the drawing buffer.

The four values are:

```text
red, green, blue, alpha
```

The first three are zero, giving black.

`alpha` is the transparency component. `1.0` means fully opaque.

This line **sets the clearing color**. The actual clearing happens in `display()`.

```python
GL.glDisable(GL.GL_DITHER)
```

This disables **dithering**.

Dithering can slightly adjust pixel colors to approximate colors on some displays or buffers. Disabling it helps preserve the exact colors we request.

```python
reshape(WIDTH, HEIGHT)
```

This calls our `reshape()` function immediately to set up the viewport and coordinate system.

```python
GLUT.glutDisplayFunc(display)
```

This tells GLUT:

“Whenever the window needs drawing, call our `display` function.”

Notice that we write:

```python
display
```

rather than:

```python
display()
```

The difference matters:

- `display()` calls the function immediately.
- `display` passes the function itself to GLUT so GLUT can call it later.

A function registered to be called later like this is called a **callback**.

```python
GLUT.glutReshapeFunc(reshape)
```

This registers our `reshape` function as another callback.

GLUT will call it with the new width and height when the window’s drawing area changes size.

```python
GLUT.glutMainLoop()
```

This starts GLUT’s **event loop**.

The loop keeps the application running and handles events such as:

- The window needing to be redrawn.
- The window being resized.
- The window being closed.

When drawing is needed, GLUT calls `display()`.

There is no mouse-click drawing feature because we have not registered a mouse callback.

---

**Lines 94–95: start the program**

```python
if __name__ == "__main__":
```

Python gives every file a special variable called `__name__`.

When you run this file directly, its value is:

```python
"__main__"
```

This condition therefore means:

“Run the following instructions if this file is the program being started directly.”

If another Python file imports this file, this condition is false, so the window does not automatically open.

```python
main()
```

This calls `main()` and starts the application.

The execution order is:

```text
Python loads the imports and settings
            ↓
Python defines the functions
            ↓
The final condition calls main()
            ↓
main() creates and configures the window
            ↓
GLUT starts its event loop
            ↓
GLUT calls display()
            ↓
display() clears the background, draws the grid,
draws the nine white pixels, and displays the picture
```

For your first reading, focus especially on these lines:

```python
for x in range(-1, 2):
    for y in range(-1, 2):
        plot_pixel(x, y, 1.0, 1.0, 1.0)
```

They are the part that directly fulfills your requirement: **draw the pixel at (0, 0) and its eight neighbors in white.**
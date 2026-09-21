"""Lab 2: draw a raster line with the Digital Differential Analyzer."""

import sys
from OpenGL import GL, GLUT


# The logical raster is 96 x 54. Each logical pixel is a 10 x 10 block
# of physical monitor pixels, producing a 960 x 540 window.
LOGICAL_WIDTH, LOGICAL_HEIGHT = 96, 54
PIXEL_SIZE = 10
WINDOW_WIDTH = LOGICAL_WIDTH * PIXEL_SIZE
WINDOW_HEIGHT = LOGICAL_HEIGHT * PIXEL_SIZE

X_MIN = -(LOGICAL_WIDTH // 2)       # -48
X_MAX = X_MIN + LOGICAL_WIDTH - 1   #  47
Y_MIN = -(LOGICAL_HEIGHT // 2)      # -27
Y_MAX = Y_MIN + LOGICAL_HEIGHT - 1  #  26


def draw_grid():
    # Draw the coordinate axes more brightly than the grid.
    GL.glColor3f(0.5, 0.5, 0.5)
    GL.glBegin(GL.GL_LINES)
    GL.glVertex2i(X_MIN, 0)
    GL.glVertex2i(X_MAX + 1, 0)
    GL.glVertex2i(0, Y_MIN)
    GL.glVertex2i(0, Y_MAX + 1)
    GL.glEnd()


def plot_pixel(x, y, red=1.0, green=1.0, blue=1.0):
    """Fill one logical pixel (a 10 x 10 monitor-pixel block)."""
    if not (X_MIN <= x <= X_MAX and Y_MIN <= y <= Y_MAX):
        return

    GL.glColor3f(red, green, blue)
    GL.glBegin(GL.GL_QUADS)
    GL.glVertex2i(x, y)
    GL.glVertex2i(x + 1, y)
    GL.glVertex2i(x + 1, y + 1)
    GL.glVertex2i(x, y + 1)
    GL.glEnd()


def dda_line(x1, y1, x2, y2, red=1.0, green=1.0, blue=1.0):
    """Rasterize a line from (x1, y1) to (x2, y2) using DDA."""
    dx = x2 - x1
    dy = y2 - y1
    steps = max(abs(dx), abs(dy))

    # A zero-length line still contains one pixel.
    if steps == 0:
        plot_pixel(round(x1), round(y1), red, green, blue)
        return

    x_increment = dx / steps
    y_increment = dy / steps
    x = float(x1)
    y = float(y1)

    # Include both endpoints, hence steps + 1 samples.
    for _ in range(steps + 1):
        plot_pixel(round(x), round(y), red, green, blue)
        x += x_increment
        y += y_increment


def display():
    GL.glClear(GL.GL_COLOR_BUFFER_BIT)
    draw_grid()

    dda_line(-5, 7, 6, -8, 1.0, 1.0, 1.0)

    GLUT.glutSwapBuffers()


def main():
    GLUT.glutInit([sys.argv[0]])
    GLUT.glutInitDisplayMode(GLUT.GLUT_DOUBLE | GLUT.GLUT_RGB)
    GLUT.glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    GLUT.glutCreateWindow(b"Lab 2 - DDA Line (96 x 54 logical raster)")
    GLUT.glutSetOption(
        GLUT.GLUT_ACTION_ON_WINDOW_CLOSE,
        GLUT.GLUT_ACTION_GLUTMAINLOOP_RETURNS,
    )

    GL.glClearColor(0.0, 0.0, 0.0, 1.0)
    GL.glDisable(GL.GL_DITHER)

    # Map the 96 x 54 logical raster onto the fixed 960 x 540 window.
    GL.glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    GL.glMatrixMode(GL.GL_PROJECTION)
    GL.glLoadIdentity()
    GL.glOrtho(X_MIN, X_MAX + 1, Y_MIN, Y_MAX + 1, -1, 1)
    GL.glMatrixMode(GL.GL_MODELVIEW)
    GL.glLoadIdentity()

    GLUT.glutDisplayFunc(display)
    GLUT.glutMainLoop()


if __name__ == "__main__":
    main()

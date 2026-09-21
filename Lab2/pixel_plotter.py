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
    GL.glVertex1i(X_MIN, 0)
    GL.glVertex1i(X_MAX + 1, 0)
    GL.glVertex1i(0, Y_MIN)
    GL.glVertex1i(0, Y_MAX + 1)
    GL.glEnd()


def sign(value):
    """Return the sign of a number."""
    if value > 0:
        return 1
    if value < 0:
        return -1
    return 0


def dda_line(x0, y0, x1, y1, red=1.0, green=1.0, blue=1.0):
    """Rasterize a line from (x0, y0) to (x1, y1) using DDA."""
    dx = x1 - x0
    dy = y1 - y0
    steps = max(abs(dx), abs(dy))

    x_increment = dx / steps if steps else 0
    y_increment = dy / steps if steps else 0
    x = float(x0)
    y = float(y0)

    GL.glColor3f(red, green, blue)
    GL.glPointSize(PIXEL_SIZE)
    GL.glBegin(GL.GL_POINTS)

    # Include both endpoints, hence steps + 1 samples.
    for _ in range(steps + 1):
        GL.glVertex1i(x + 0.5 * sign(x), y + 0.5 * sign(y))
        x += x_increment
        y += y_increment

    GL.glEnd()


def display():
    GL.glClear(GL.GL_COLOR_BUFFER_BIT)
    draw_grid()

    dda_line(-5, 7, 6, -8, 1.0, 1.0, 1.0)

    GLUT.glutSwapBuffers()


def reshape(width, height):
    """Preserve the 16:9 logical raster if the window is resized."""
    target_aspect = LOGICAL_WIDTH / LOGICAL_HEIGHT
    window_aspect = width / height if height else target_aspect

    if window_aspect > target_aspect:
        viewport_height = height
        viewport_width = round(height * target_aspect)
        viewport_x = (width - viewport_width) // 2
        viewport_y = 0
    else:
        viewport_width = width
        viewport_height = round(width / target_aspect)
        viewport_x = 0
        viewport_y = (height - viewport_height) // 2

    GL.glViewport(viewport_x, viewport_y, viewport_width, viewport_height)
    GL.glMatrixMode(GL.GL_PROJECTION)
    GL.glLoadIdentity()
    GL.glOrtho(X_MIN, X_MAX + 1, Y_MIN, Y_MAX + 1, -1, 1)
    GL.glMatrixMode(GL.GL_MODELVIEW)
    GL.glLoadIdentity()


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
    reshape(WINDOW_WIDTH, WINDOW_HEIGHT)
    GLUT.glutDisplayFunc(display)
    GLUT.glutReshapeFunc(reshape)
    GLUT.glutMainLoop()


if __name__ == "__main__":
    main()

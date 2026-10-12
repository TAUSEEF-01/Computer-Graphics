"""Animate a Bresenham circle using eight-way symmetry."""

import sys
from OpenGL import GL, GLUT


WINDOW_WIDTH = 960
WINDOW_HEIGHT = 540
xmax = WINDOW_WIDTH
ymax = WINDOW_HEIGHT

# Circle center, movement per animation frame, and circle radius.
xc = 0
yc = 0
dx = 2
dy = -1
r = 50

def draw8way_symmetry(x, y):
    """After zone 0 is plotted, draw its seven reflected circle points."""
    GL.glVertex2i(xc + y, yc + x)
    GL.glVertex2i(xc - y, yc + x)
    GL.glVertex2i(xc - x, yc + y)
    GL.glVertex2i(xc - x, yc - y)
    GL.glVertex2i(xc - y, yc - x)
    GL.glVertex2i(xc + y, yc - x)
    GL.glVertex2i(xc + x, yc - y)


def draw_circle():
    """Draw zone 0 first, then reflect each point into the other zones."""
    x = r
    y = 0
    decision = 3 - 2 * r

    GL.glColor3f(0.0, 0.7, 1.0)
    GL.glPointSize(2.0)
    GL.glBegin(GL.GL_POINTS)

    while y <= x:
        # Draw zone 0, then its seven symmetric counterparts.
        GL.glVertex2i(xc + x, yc + y)
        draw8way_symmetry(x, y)

        if decision < 0:
            y += 1
            decision += 4 * y + 2
        else:
            x -= 1
            y += 1
            decision += 4 * (y - x) + 2

    GL.glEnd()


def display():
    GL.glClear(GL.GL_COLOR_BUFFER_BIT)
    draw_circle()
    GLUT.glutSwapBuffers()


def reshape(width, height):
    """Keep the 960x540 coordinate view centered as the window is resized."""
    scale = min(width / WINDOW_WIDTH, height / WINDOW_HEIGHT)
    viewport_width = round(WINDOW_WIDTH * scale)
    viewport_height = round(WINDOW_HEIGHT * scale)
    GL.glViewport(
        (width - viewport_width) // 2,
        (height - viewport_height) // 2,
        viewport_width,
        viewport_height,
    )
    GL.glMatrixMode(GL.GL_PROJECTION)
    GL.glLoadIdentity()
    GL.glOrtho(-480, 480, -270, 270, -1, 1)
    GL.glMatrixMode(GL.GL_MODELVIEW)
    GL.glLoadIdentity()


def animate(_value):
    """Move the center and bounce the circle off the window boundaries."""
    global xc, yc, dx, dy

    xc += dx
    yc += dy

    if xc + r >= xmax // 2:
        xc = xmax // 2 - r
        dx = -abs(dx)
    if xc - r <= -(xmax // 2):
        xc = -(xmax // 2) + r
        dx = abs(dx)
    if yc + r >= ymax // 2:
        yc = ymax // 2 - r
        dy = -abs(dy)
    if yc - r <= -(ymax // 2):
        yc = -(ymax // 2) + r
        dy = abs(dy)

    GLUT.glutPostRedisplay()
    GLUT.glutTimerFunc(16, animate, 0)  # About 60 animation updates per second.


def main():
    GLUT.glutInit([sys.argv[0]])
    GLUT.glutInitDisplayMode(GLUT.GLUT_DOUBLE | GLUT.GLUT_RGB)
    GLUT.glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    GLUT.glutCreateWindow(b"Lab 5 - Animated Bresenham Circle")
    GLUT.glutSetOption(
        GLUT.GLUT_ACTION_ON_WINDOW_CLOSE,
        GLUT.GLUT_ACTION_GLUTMAINLOOP_RETURNS,
    )

    GL.glClearColor(0.0, 0.0, 0.0, 1.0)
    GL.glDisable(GL.GL_DITHER)
    reshape(WINDOW_WIDTH, WINDOW_HEIGHT)
    GLUT.glutDisplayFunc(display)
    GLUT.glutReshapeFunc(reshape)
    GLUT.glutTimerFunc(16, animate, 0)
    GLUT.glutMainLoop()


if __name__ == "__main__":
    main()

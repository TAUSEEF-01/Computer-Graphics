"""Lab 1: graph paper with nine white pixels centered at (0, 0)."""

import sys
from OpenGL import GL, GLUT

WIDTH, HEIGHT = 960, 720


def draw_text(x, y, text):
    GL.glColor3f(0.75, 0.75, 0.75)
    GL.glRasterPos2f(x, y)
    for character in text:
        GLUT.glutBitmapCharacter(GLUT.GLUT_BITMAP_8_BY_13, ord(character))


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

    # Draw the x and y axes brighter than the grid.
    GL.glColor3f(0.5, 0.5, 0.5)
    GL.glBegin(GL.GL_LINES)
    GL.glVertex2f(-480, 0.5)
    GL.glVertex2f(480, 0.5)
    GL.glVertex2f(0.5, -360)
    GL.glVertex2f(0.5, 360)
    GL.glEnd()

    for x in range(-400, 401, 100):
        if x != 0:
            draw_text(x + 3, -17, str(x))
    for y in range(-300, 301, 100):
        if y != 0:
            draw_text(7, y + 3, str(y))
    draw_text(7, -17, "0")
    draw_text(460, 7, "x")
    draw_text(7, 340, "y")


def plot_pixel(x, y, red, green, blue):
    """Draw one device pixel with RGB intensities from 0.0 to 1.0."""
    GL.glColor3f(red, green, blue)
    GL.glPointSize(1)
    GL.glBegin(GL.GL_POINTS)
    # Offset by half a unit to land at the center of a device pixel.
    GL.glVertex2f(x + 0.5, y + 0.5)
    GL.glEnd()


def display():
    GL.glClear(GL.GL_COLOR_BUFFER_BIT)
    draw_grid()

    # (0, 0) and its eight neighbors: exactly nine white pixels.
    for x in range(-1, 2):
        for y in range(-1, 2):
            plot_pixel(x, y, 1.0, 1.0, 1.0)

    GLUT.glutSwapBuffers()


def reshape(width, height):
    # Keep one coordinate unit equal to one device pixel when resized.
    GL.glViewport((width - WIDTH) // 2, (height - HEIGHT) // 2, WIDTH, HEIGHT)
    GL.glMatrixMode(GL.GL_PROJECTION)
    GL.glLoadIdentity()
    GL.glOrtho(-480, 480, -360, 360, -1, 1)
    GL.glMatrixMode(GL.GL_MODELVIEW)
    GL.glLoadIdentity()


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


if __name__ == "__main__":
    main()

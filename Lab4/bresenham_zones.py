"""Lab 4: draw radius-250 lines using Bresenham in eight zone colors."""

import math
import sys
from OpenGL import GL, GLUT

WINDOW_WIDTH, WINDOW_HEIGHT = 960, 540
RADIUS = 250
ANGLE_STEP = 5
PRINT_POINTS = False

ZONE_NAMES = ("cyan", "magenta", "yellow", "red", "green", "orange", "black", "blue")
ZONE_COLORS = (
    (0.0, 1.0, 1.0),  # Zone 0: cyan
    (1.0, 0.0, 1.0),  # Zone 1: magenta
    (1.0, 1.0, 0.0),  # Zone 2: yellow
    (1.0, 0.0, 0.0),  # Zone 3: red
    (0.0, 1.0, 0.0),  # Zone 4: green
    (1.0, 0.5, 0.0),  # Zone 5: orange
    (0.0, 0.0, 0.0),  # Zone 6: black
    (0.0, 0.0, 1.0),  # Zone 7: blue
)


def sign(value):
    if value > 0:
        return 1
    if value < 0:
        return -1
    return 0


def round_coordinate(value):
    return int(value + 0.5 * sign(value))


def find_zone(x0, y0, x1, y1):
    """Classify the direction using signs and the dominant coordinate."""
    dx, dy = x1 - x0, y1 - y0
    if dx >= 0 and dy >= 0:
        return 0 if abs(dx) >= abs(dy) else 1
    if dx < 0 and dy >= 0:
        return 3 if abs(dx) >= abs(dy) else 2
    if dx < 0 and dy < 0:
        return 4 if abs(dx) >= abs(dy) else 5
    return 7 if abs(dx) >= abs(dy) else 6


def drawPixel(x, y):
    """Submit one pixel inside a GL_POINTS drawing block."""
    if PRINT_POINTS:
        print(f"Plotting point: ({x}, {y})")
    GL.glVertex2i(x, y)


def drawLine_0(x0, y0, x1, y1):
    """Zone 0 Bresenham: choose East or North-East at each step."""
    dx = x1 - x0
    dy = y1 - y0
    d = 2 * dy - dx
    x = x0
    y = y0

    GL.glColor3f(*ZONE_COLORS[0])
    GL.glPointSize(2.0)
    GL.glBegin(GL.GL_POINTS)

    drawPixel(x, y)
    while x < x1:
        if d < 0:
            x += 1
            d += 2 * dy
        else:
            x += 1
            y += 1
            d += 2 * (dy - dx)
        drawPixel(x, y)

    GL.glEnd()


def drawLine_1(x0, y0, x1, y1):
    """Zone 1: choose North or North-East."""
    dx = x1 - x0
    dy = y1 - y0
    d = 2 * dx - dy
    x = x0
    y = y0

    GL.glColor3f(*ZONE_COLORS[1])
    GL.glPointSize(2.0)
    GL.glBegin(GL.GL_POINTS)
    drawPixel(x, y)
    while y < y1:
        if d < 0:
            y += 1
            d += 2 * dx
        else:
            x += 1
            y += 1
            d += 2 * (dx - dy)
        drawPixel(x, y)
    GL.glEnd()


def drawLine_2(x0, y0, x1, y1):
    """Zone 2: choose North or North-West."""
    dx = x0 - x1  # Positive horizontal distance to the left.
    dy = y1 - y0
    d = 2 * dx - dy
    x = x0
    y = y0

    GL.glColor3f(*ZONE_COLORS[2])
    GL.glPointSize(2.0)
    GL.glBegin(GL.GL_POINTS)
    drawPixel(x, y)
    while y < y1:
        if d < 0:
            y += 1
            d += 2 * dx
        else:
            x -= 1
            y += 1
            d += 2 * (dx - dy)
        drawPixel(x, y)
    GL.glEnd()


def drawLine_3(x0, y0, x1, y1):
    """Zone 3: choose West or North-West."""
    dx = x0 - x1
    dy = y1 - y0
    d = 2 * dy - dx
    x = x0
    y = y0

    GL.glColor3f(*ZONE_COLORS[3])
    GL.glPointSize(2.0)
    GL.glBegin(GL.GL_POINTS)
    drawPixel(x, y)
    while x > x1:
        if d < 0:
            x -= 1
            d += 2 * dy
        else:
            x -= 1
            y += 1
            d += 2 * (dy - dx)
        drawPixel(x, y)
    GL.glEnd()


def drawLine_4(x0, y0, x1, y1):
    """Zone 4: choose West or South-West."""
    dx = x0 - x1
    dy = y0 - y1  # Positive vertical distance downward.
    d = 2 * dy - dx
    x = x0
    y = y0

    GL.glColor3f(*ZONE_COLORS[4])
    GL.glPointSize(2.0)
    GL.glBegin(GL.GL_POINTS)
    drawPixel(x, y)
    while x > x1:
        if d < 0:
            x -= 1
            d += 2 * dy
        else:
            x -= 1
            y -= 1
            d += 2 * (dy - dx)
        drawPixel(x, y)
    GL.glEnd()


def drawLine_5(x0, y0, x1, y1):
    """Zone 5: choose South or South-West."""
    dx = x0 - x1
    dy = y0 - y1
    d = 2 * dx - dy
    x = x0
    y = y0

    GL.glColor3f(*ZONE_COLORS[5])
    GL.glPointSize(2.0)
    GL.glBegin(GL.GL_POINTS)
    drawPixel(x, y)
    while y > y1:
        if d < 0:
            y -= 1
            d += 2 * dx
        else:
            x -= 1
            y -= 1
            d += 2 * (dx - dy)
        drawPixel(x, y)
    GL.glEnd()


def drawLine_6(x0, y0, x1, y1):
    """Zone 6: choose South or South-East."""
    dx = x1 - x0
    dy = y0 - y1
    d = 2 * dx - dy
    x = x0
    y = y0

    GL.glColor3f(*ZONE_COLORS[6])
    GL.glPointSize(2.0)
    GL.glBegin(GL.GL_POINTS)
    drawPixel(x, y)
    while y > y1:
        if d < 0:
            y -= 1
            d += 2 * dx
        else:
            x += 1
            y -= 1
            d += 2 * (dx - dy)
        drawPixel(x, y)
    GL.glEnd()


def drawLine_7(x0, y0, x1, y1):
    """Zone 7: choose East or South-East."""
    dx = x1 - x0
    dy = y0 - y1
    d = 2 * dy - dx
    x = x0
    y = y0

    GL.glColor3f(*ZONE_COLORS[7])
    GL.glPointSize(2.0)
    GL.glBegin(GL.GL_POINTS)
    drawPixel(x, y)
    while x < x1:
        if d < 0:
            x += 1
            d += 2 * dy
        else:
            x += 1
            y -= 1
            d += 2 * (dy - dx)
        drawPixel(x, y)
    GL.glEnd()


DRAW_FUNCTIONS = (
    drawLine_0, drawLine_1, drawLine_2, drawLine_3,
    drawLine_4, drawLine_5, drawLine_6, drawLine_7,
)


def drawLine(x0, y0, x1, y1):
    zone = find_zone(x0, y0, x1, y1)
    DRAW_FUNCTIONS[zone](x0, y0, x1, y1)


def display():
    GL.glClear(GL.GL_COLOR_BUFFER_BIT)
    # 36 diameters, each drawn as two separately colored half-lines.
    for angle in range(0, 180, ANGLE_STEP):
        radians = math.radians(angle)
        x = round_coordinate(RADIUS * math.cos(radians))
        y = round_coordinate(RADIUS * math.sin(radians))
        drawLine(0, 0, x, y)
        drawLine(0, 0, -x, -y)
    GLUT.glutSwapBuffers()


def reshape(width, height):
    scale = min(width / WINDOW_WIDTH, height / WINDOW_HEIGHT)
    viewport_width = round(WINDOW_WIDTH * scale)
    viewport_height = round(WINDOW_HEIGHT * scale)
    GL.glViewport((width - viewport_width) // 2,
                  (height - viewport_height) // 2,
                  viewport_width, viewport_height)
    GL.glMatrixMode(GL.GL_PROJECTION)
    GL.glLoadIdentity()
    GL.glOrtho(-480, 480, -270, 270, -1, 1)
    GL.glMatrixMode(GL.GL_MODELVIEW)
    GL.glLoadIdentity()


def main():
    for zone, name in enumerate(ZONE_NAMES):
        print(f"Zone {zone}: {name}, function: drawLine_{zone}")
    GLUT.glutInit([sys.argv[0]])
    GLUT.glutInitDisplayMode(GLUT.GLUT_DOUBLE | GLUT.GLUT_RGB)
    GLUT.glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    GLUT.glutCreateWindow(b"Lab 4 - Eight Bresenham Zones")
    GLUT.glutSetOption(GLUT.GLUT_ACTION_ON_WINDOW_CLOSE,
                       GLUT.GLUT_ACTION_GLUTMAINLOOP_RETURNS)
    # White background displays the eight zone colors.
    GL.glClearColor(1.0, 1.0, 1.0, 1.0)
    GL.glDisable(GL.GL_DITHER)
    reshape(WINDOW_WIDTH, WINDOW_HEIGHT)
    GLUT.glutDisplayFunc(display)
    GLUT.glutReshapeFunc(reshape)
    GLUT.glutMainLoop()


if __name__ == "__main__":
    main()

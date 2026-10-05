"""Lab 4: draw a radius-250 circle of DDA lines in eight zone colors."""

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


def plot_dda_points(x, y, step, x_increment, y_increment, zone):
    """Shared pixel plotting; each zone function supplies its increments."""
    GL.glColor3f(*ZONE_COLORS[zone])
    GL.glPointSize(2.0)
    GL.glBegin(GL.GL_POINTS)
    for _ in range(step + 1):
        rounded_x = int(x + 0.5 * sign(x))
        rounded_y = int(y + 0.5 * sign(y))
        if PRINT_POINTS:
            print(f"Plotting point: ({rounded_x}, {rounded_y})")
        GL.glVertex2i(rounded_x, rounded_y)
        x += x_increment
        y += y_increment
    GL.glEnd()


def drawLine_0(x0, y0, x1, y1):
    """Right and up, shallow: x increases by 1."""
    dx, dy = x1 - x0, y1 - y0
    step = dx
    plot_dda_points(x0, y0, step, 1, dy / step if step else 0, 0)


def drawLine_1(x0, y0, x1, y1):
    """Right and up, steep: y increases by 1."""
    dx, dy = x1 - x0, y1 - y0
    step = dy
    plot_dda_points(x0, y0, step, dx / step, 1, 1)


def drawLine_2(x0, y0, x1, y1):
    """Left and up, steep: y increases by 1."""
    dx, dy = x1 - x0, y1 - y0
    step = dy
    plot_dda_points(x0, y0, step, dx / step, 1, 2)


def drawLine_3(x0, y0, x1, y1):
    """Left and up, shallow: x decreases by 1."""
    dx, dy = x1 - x0, y1 - y0
    step = -dx
    plot_dda_points(x0, y0, step, -1, dy / step, 3)


def drawLine_4(x0, y0, x1, y1):
    """Left and down, shallow: x decreases by 1."""
    dx, dy = x1 - x0, y1 - y0
    step = -dx
    plot_dda_points(x0, y0, step, -1, dy / step, 4)


def drawLine_5(x0, y0, x1, y1):
    """Left and down, steep: y decreases by 1."""
    dx, dy = x1 - x0, y1 - y0
    step = -dy
    plot_dda_points(x0, y0, step, dx / step, -1, 5)


def drawLine_6(x0, y0, x1, y1):
    """Right and down, steep: y decreases by 1."""
    dx, dy = x1 - x0, y1 - y0
    step = -dy
    plot_dda_points(x0, y0, step, dx / step, -1, 6)


def drawLine_7(x0, y0, x1, y1):
    """Right and down, shallow: x increases by 1."""
    dx, dy = x1 - x0, y1 - y0
    step = dx
    plot_dda_points(x0, y0, step, 1, dy / step, 7)


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
    GLUT.glutCreateWindow(b"Lab 4 - Eight DDA Zones")
    GLUT.glutSetOption(GLUT.GLUT_ACTION_ON_WINDOW_CLOSE,
                       GLUT.GLUT_ACTION_GLUTMAINLOOP_RETURNS)
    # Light gray makes every zone color, including black, visible.
    GL.glClearColor(0.65, 0.65, 0.65, 1.0)
    GL.glDisable(GL.GL_DITHER)
    reshape(WINDOW_WIDTH, WINDOW_HEIGHT)
    GLUT.glutDisplayFunc(display)
    GLUT.glutReshapeFunc(reshape)
    GLUT.glutMainLoop()


if __name__ == "__main__":
    main()

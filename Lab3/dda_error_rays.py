"""Lab 3: visualize the rounding error of DDA lines using brightness."""

import math
import sys

from OpenGL import GL, GLUT


WINDOW_WIDTH = 960
WINDOW_HEIGHT = 540
RADIUS = 250
ANGLE_START = 0
ANGLE_END = 180
ANGLE_STEP = 5
NUMBER_OF_LINES = ANGLE_END // ANGLE_STEP  # 180 / 5 = 36 lines
CONTRAST_POWER = 6

# Set this to True if every calculated DDA point should be printed.
PRINT_POINTS = False

# Filled once in main(), then used by display().
LINES = []
MAX_ERROR = 0.0


def sign(value):
    """Return 1 for positive, -1 for negative, and 0 for zero."""
    if value > 0:
        return 1
    if value < 0:
        return -1
    return 0


def round_coordinate(value):
    """Round a coordinate using the rule specified in the activity."""
    return int(value + 0.5 * sign(value))


def error_to_brightness(error, max_error):
    """Spread clustered error values across more visible gray levels."""
    normalized_error = error / max_error if max_error else 0.0
    return normalized_error ** CONTRAST_POWER


def calculate_line_error(x0, y0, x1, y1):
    """First DDA loop: sum the rounding errors of all points on one line."""
    dx = x1 - x0
    dy = y1 - y0
    step = max(abs(dx), abs(dy))
    x_increment = dx / step if step else 0
    y_increment = dy / step if step else 0

    x = x0
    y = y0
    line_total_error = 0.0

    for _ in range(step + 1):
        rounded_x = int(x + 0.5 * sign(x))
        rounded_y = int(y + 0.5 * sign(y))

        if PRINT_POINTS:
            print(f"Plotting point: ({rounded_x}, {rounded_y})")

        # The absolute value makes the error a non-negative magnitude.
        error = abs((x - rounded_x) + (y - rounded_y))
        line_total_error += error

        x += x_increment
        y += y_increment

    return line_total_error


def draw_dda_line(x0, y0, x1, y1, error, max_error):
    """Second DDA loop: draw one line using error/max_error as its color."""
    dx = x1 - x0
    dy = y1 - y0
    step = max(abs(dx), abs(dy))
    x_increment = dx / step if step else 0
    y_increment = dy / step if step else 0

    brightness = error_to_brightness(error, max_error)
    GL.glColor3d(brightness, brightness, brightness)
    GL.glPointSize(2.0)
    GL.glBegin(GL.GL_POINTS)

    x = x0
    y = y0
    for _ in range(step + 1):
        GL.glVertex2i(
            int(x + 0.5 * sign(x)),
            int(y + 0.5 * sign(y)),
        )
        x += x_increment
        y += y_increment

    GL.glEnd()


def prepare_lines():
    """Create the 36 diameters and complete the error-calculation pass."""
    lines = []

    # 180 degrees duplicates the orientation at 0 degrees, so it is excluded.
    for angle in range(ANGLE_START, ANGLE_END, ANGLE_STEP):
        radians = math.radians(angle)
        end_x = round_coordinate(RADIUS * math.cos(radians))
        end_y = round_coordinate(RADIUS * math.sin(radians))
        start_x = -end_x
        start_y = -end_y
        error = calculate_line_error(start_x, start_y, end_x, end_y)
        lines.append((angle, start_x, start_y, end_x, end_y, error))

    max_error = max(line[5] for line in lines)
    return lines, max_error


def display():
    """Clear the window and draw all rays during the second pass."""
    GL.glClear(GL.GL_COLOR_BUFFER_BIT)

    for angle, start_x, start_y, end_x, end_y, error in LINES:
        draw_dda_line(start_x, start_y, end_x, end_y, error, MAX_ERROR)

    GLUT.glutSwapBuffers()


def reshape(width, height):
    """Keep the 16:9 drawing area when the window is resized."""
    target_aspect = WINDOW_WIDTH / WINDOW_HEIGHT
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
    GL.glOrtho(-480, 480, -270, 270, -1, 1)
    GL.glMatrixMode(GL.GL_MODELVIEW)
    GL.glLoadIdentity()


def main():
    global LINES, MAX_ERROR

    # First pass: calculate each line's total error and the largest total.
    LINES, MAX_ERROR = prepare_lines()
    print(f"Number of lines: {len(LINES)}")
    print(f"Global maximum error: {MAX_ERROR:.12f}")
    for angle, start_x, start_y, end_x, end_y, error in LINES:
        print(
            f"Angle {angle:3d} degrees: "
            f"start=({start_x:4d}, {start_y:4d}), "
            f"end=({end_x:4d}, {end_y:4d}), "
            f"total error={error:.12f}, "
            f"brightness={error_to_brightness(error, MAX_ERROR):.6f}"
        )

    GLUT.glutInit([sys.argv[0]])
    GLUT.glutInitDisplayMode(GLUT.GLUT_DOUBLE | GLUT.GLUT_RGB)
    GLUT.glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    GLUT.glutCreateWindow(b"Lab 3 - DDA Rounding Error Circle")
    GLUT.glutSetOption(
        GLUT.GLUT_ACTION_ON_WINDOW_CLOSE,
        GLUT.GLUT_ACTION_GLUTMAINLOOP_RETURNS,
    )

    # A medium blue-gray reveals both dark low-error and bright high-error rays.
    GL.glClearColor(0.20, 0.30, 0.40, 1.0)
    GL.glDisable(GL.GL_DITHER)
    reshape(WINDOW_WIDTH, WINDOW_HEIGHT)
    GLUT.glutDisplayFunc(display)
    GLUT.glutReshapeFunc(reshape)
    GLUT.glutMainLoop()


if __name__ == "__main__":
    main()

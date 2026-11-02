"""Lab 6: midpoint ellipse with a repeating drop, compression, and rebound."""

import math
import sys
from OpenGL import GL, GLUT


WIDTH = 960
HEIGHT = 600
FLOOR_Y = 45
FPS = 30
r = 30.0
xc = WIDTH // 2

# Keep a*a + b*b = r*r. The starting circle radius is r/sqrt(2).
a = b = r / math.sqrt(2)
top_y = HEIGHT - b - 2
yc = top_y
velocity = 0.0
acceleration = 5.0
phase = "FALLING"
rise_start_y = 0.0


def reset_animation():
    global a, b, yc, top_y, velocity, acceleration, phase, rise_start_y
    a = b = r / math.sqrt(2)
    top_y = HEIGHT - b - 2
    yc = top_y
    velocity = 0.0
    acceleration = 5.0
    phase = "FALLING"
    rise_start_y = 0.0


def draw4way_symmetry(x, y):
    GL.glVertex2i(xc + x, round(yc) + y)
    GL.glVertex2i(xc - x, round(yc) + y)
    GL.glVertex2i(xc + x, round(yc) - y)
    GL.glVertex2i(xc - x, round(yc) - y)


def draw_ellipse():
    # Start at (a,0) and move toward (0,b).
    rx = max(1, round(a))
    ry = max(1, round(b))
    a2 = rx * rx
    b2 = ry * ry
    x = rx
    y = 0

    GL.glColor3f(0.15, 0.8, 1.0)
    GL.glPointSize(2.0)
    GL.glBegin(GL.GL_POINTS)

    # Near the right edge: increase y, choosing N or NW.
    decision = b2 * (x - 0.5) ** 2 + a2 - a2 * b2
    while a2 * y < b2 * x:
        draw4way_symmetry(x, y)
        if decision < 0:  # N
            decision += a2 * (2 * y + 3)
        else:             # NW
            decision += a2 * (2 * y + 3) + b2 * (-2 * x + 2)
            x -= 1
        y += 1

    # Near the top: decrease x, choosing W or NW.
    decision = b2 * (x - 1) ** 2 + a2 * (y + 0.5) ** 2 - a2 * b2
    while x >= 0:
        draw4way_symmetry(x, y)
        if decision < 0:  # NW
            decision += b2 * (-2 * x + 3) + a2 * (2 * y + 2)
            y += 1
        else:             # W
            decision += b2 * (-2 * x + 3)
        x -= 1

    GL.glEnd()


def update_animation():
    global a, b, yc, velocity, acceleration, phase, rise_start_y

    if phase == "FALLING":
        velocity += acceleration
        yc -= velocity
        if yc - b <= FLOOR_Y:
            yc = FLOOR_Y + b
            phase = "COMPRESSING"
            acceleration = 1.0
            velocity = 0.0

    elif phase == "COMPRESSING":
        velocity += acceleration
        minimum_b = r / math.sqrt(5)
        b = max(minimum_b, b - velocity)
        a = math.sqrt(r * r - b * b)
        yc = FLOOR_Y + b
        if b <= minimum_b:
            phase = "RISING"
            rise_start_y = yc
            acceleration = 5.0
            # Launch speed needed to reach the original top with zero velocity.
            velocity = -math.sqrt(2 * acceleration * (top_y - yc))

    elif phase == "RISING":
        # Use the remaining fraction of a frame when reaching the top.
        time_to_top = -velocity / acceleration
        dt = min(1.0, time_to_top)
        yc -= velocity * dt + 0.5 * acceleration * dt * dt
        velocity += acceleration * dt

        # Gradually recover the circle while preserving a*a + b*b = r*r.
        progress = (yc - rise_start_y) / (top_y - rise_start_y)
        progress = min(1.0, max(0.0, progress))
        minimum_b = r / math.sqrt(5)
        b = minimum_b + (r / math.sqrt(2) - minimum_b) * progress
        a = math.sqrt(r * r - b * b)
        if time_to_top <= 1.0:
            reset_animation()


def display():
    GL.glClear(GL.GL_COLOR_BUFFER_BIT)
    GL.glLoadIdentity()

    GL.glColor3f(0.45, 0.48, 0.52)
    GL.glBegin(GL.GL_LINES)
    GL.glVertex2i(0, FLOOR_Y)
    GL.glVertex2i(WIDTH, FLOOR_Y)
    GL.glEnd()

    draw_ellipse()
    GLUT.glutSwapBuffers()


def reshape(width, height):
    scale = min(max(1, width) / WIDTH, max(1, height) / HEIGHT)
    viewport_width = max(1, round(WIDTH * scale))
    viewport_height = max(1, round(HEIGHT * scale))
    GL.glViewport((width - viewport_width) // 2, (height - viewport_height) // 2,
                  viewport_width, viewport_height)
    GL.glMatrixMode(GL.GL_PROJECTION)
    GL.glLoadIdentity()
    GL.glOrtho(0, WIDTH, 0, HEIGHT, -1, 1)
    GL.glMatrixMode(GL.GL_MODELVIEW)
    GL.glLoadIdentity()


def keyboard(key, _x, _y):
    if key == b"\x1b":
        GLUT.glutLeaveMainLoop()


def animate(_value):
    update_animation()
    GLUT.glutPostRedisplay()
    GLUT.glutTimerFunc(round(1000 / FPS), animate, 0)


def main():
    GLUT.glutInit([sys.argv[0]])
    GLUT.glutInitDisplayMode(GLUT.GLUT_DOUBLE | GLUT.GLUT_RGB)
    GLUT.glutInitWindowSize(WIDTH, HEIGHT)
    GLUT.glutCreateWindow(b"Lab 6 - Falling Circle to Midpoint Ellipse")
    GLUT.glutSetOption(GLUT.GLUT_ACTION_ON_WINDOW_CLOSE,
                       GLUT.GLUT_ACTION_GLUTMAINLOOP_RETURNS)
    GL.glClearColor(0.025, 0.035, 0.055, 1.0)
    GL.glDisable(GL.GL_DITHER)
    reshape(WIDTH, HEIGHT)
    GLUT.glutDisplayFunc(display)
    GLUT.glutReshapeFunc(reshape)
    GLUT.glutKeyboardFunc(keyboard)
    GLUT.glutTimerFunc(round(1000 / FPS), animate, 0)
    GLUT.glutMainLoop()


if __name__ == "__main__":
    main()

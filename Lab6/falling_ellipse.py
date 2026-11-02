"""Lab 6: falling circle and midpoint ellipse deformation (PyOpenGL).

r is the invariant parameter: a*a + b*b = r*r. Consequently the initial
circle radius is r/sqrt(2), as agreed, rather than r. Run this file to animate.
"""

import math
import sys
from dataclasses import dataclass, field
from collections.abc import Iterator

from OpenGL import GL, GLUT


WIDTH, HEIGHT = 960, 600
FLOOR_Y = 45
R = 30.0
FPS = 30
FALL_ACCELERATION = 5.0       # pixels/frame^2
COMPRESSION_ACCELERATION = 1.0  # pixels/frame^2


def midpoint_ellipse(a: float, b: float) -> Iterator[tuple[int, int]]:
    """Generate outline pixels using the PDF's two-region midpoint algorithm.

    Round the semiaxes only for rasterization; keep the animation's mathematical
    a and b as floats so their invariant is not damaged by integer rounding.
    All decision increments below use the OLD x,y, before taking a step.
    """
    if not (math.isfinite(a) and math.isfinite(b) and a > 0 and b > 0):
        raise ValueError("Ellipse semiaxes must be finite and positive.")
    # Swap axes for the midpoint calculation: local x is vertical, local y
    # is horizontal. Mapping back starts at (a,0) and ends toward (0,b).
    rx, ry = max(1, round(b)), max(1, round(a))
    rx2, ry2 = rx * rx, ry * ry
    x, y = 0, ry

    def symmetric_points() -> Iterator[tuple[int, int]]:
        yield y, x
        yield -y, x
        yield y, -x
        yield -y, -x

    # Local Region 1: mapped to N or NW in display coordinates.
    decision = ry2 - rx2 * ry + 0.25 * rx2
    while ry2 * x < rx2 * y:
        yield from symmetric_points()
        if decision < 0:             # E: (x+1, y)
            decision += ry2 * (2 * x + 3)
        else:                        # SE: (x+1, y-1)
            decision += ry2 * (2 * x + 3) + rx2 * (-2 * y + 2)
            y -= 1
        x += 1

    # Local Region 2: mapped to W or NW in display coordinates.
    decision = ry2 * (x + 0.5) ** 2 + rx2 * (y - 1) ** 2 - rx2 * ry2
    while y >= 0:
        yield from symmetric_points()
        if decision < 0:             # SE: (x+1, y-1)
            decision += ry2 * (2 * x + 2) + rx2 * (-2 * y + 3)
            x += 1
        else:                        # S: (x, y-1)
            decision += rx2 * (-2 * y + 3)
        y -= 1


@dataclass
class Animation:
    """Frame-based movement; positive velocity is down, negative is up."""

    r: float = R
    a: float = field(init=False)
    b: float = field(init=False)
    yc: float = field(init=False)
    velocity: float = field(init=False, default=0.0)
    acceleration: float = field(init=False, default=FALL_ACCELERATION)
    phase: str = field(init=False, default="FALLING")
    rise_start_y: float = field(init=False, default=0.0)

    @property
    def top_y(self) -> float:
        """Center height of the original circle at the top of the display."""
        return HEIGHT - self.r / math.sqrt(2) - 2

    def __post_init__(self) -> None:
        initial_radius = self.r / math.sqrt(2)
        if not math.isfinite(self.r) or initial_radius < 2:
            raise ValueError("r must be finite and give a circle radius >= 2 pixels.")
        if 2 * initial_radius >= HEIGHT - FLOOR_Y - 2:
            raise ValueError("The initial circle does not fit above the floor.")
        if 2 * self.r / math.sqrt(5) >= WIDTH / 2 - 2:
            raise ValueError("The final ellipse does not fit inside the display.")
        self.reset()

    def reset(self) -> None:
        self.a = self.b = self.r / math.sqrt(2)
        self.yc = self.top_y
        self.rise_start_y = 0.0
        self.velocity = 0.0
        self.acceleration = FALL_ACCELERATION
        self.phase = "FALLING"

    def step(self) -> None:
        if self.phase == "FALLING":
            # Acceleration changes velocity; velocity changes position.
            self.velocity += self.acceleration
            self.yc -= self.velocity
            if self.yc - self.b <= FLOOR_Y:
                self.yc = FLOOR_Y + self.b  # prevent floor penetration
                self.phase = "COMPRESSING"
                self.acceleration = COMPRESSION_ACCELERATION
                # Ground contact stops the falling motion. Compression starts
                # from rest with its own acceleration of 1 pixel/frame^2.
                self.velocity = 0.0

        elif self.phase == "COMPRESSING":
            self.velocity += self.acceleration
            # a=2b and a^2+b^2=r^2 imply b_min=r/sqrt(5).
            minimum_b = self.r / math.sqrt(5)
            self.b = max(minimum_b, self.b - self.velocity)
            self.a = math.sqrt(self.r * self.r - self.b * self.b)
            self.yc = FLOOR_Y + self.b  # bottom remains on the floor
            if self.b <= minimum_b:
                self.phase = "RISING"
                self.rise_start_y = self.yc
                self.acceleration = FALL_ACCELERATION
                # v_final^2 = v_initial^2 - 2*g*h, with v_final=0.
                # Choose launch speed to reach the original top exactly.
                height = self.top_y - self.yc
                self.velocity = -math.sqrt(2 * self.acceleration * height)

        elif self.phase == "RISING":
            # Integrate constant downward acceleration for one frame, or the
            # remaining fraction of a frame if the apex occurs sooner.
            time_to_top = -self.velocity / self.acceleration
            dt = min(1.0, time_to_top)
            self.yc -= self.velocity * dt + 0.5 * self.acceleration * dt * dt
            self.velocity += self.acceleration * dt

            # Recover the circle progressively during ascent. Computing a
            # from b preserves a^2+b^2=r^2 throughout the rebound as well.
            progress = (self.yc - self.rise_start_y) / (self.top_y - self.rise_start_y)
            progress = min(1.0, max(0.0, progress))
            minimum_b = self.r / math.sqrt(5)
            circle_radius = self.r / math.sqrt(2)
            self.b = minimum_b + (circle_radius - minimum_b) * progress
            self.a = math.sqrt(self.r * self.r - self.b * self.b)
            if time_to_top <= 1.0:
                # Reach the top as a circle at rest, ready for the next drop.
                # The next timer frame starts falling again automatically.
                self.reset()


animation = Animation()


def display() -> None:
    GL.glClear(GL.GL_COLOR_BUFFER_BIT)
    GL.glLoadIdentity()

    GL.glColor3f(0.45, 0.48, 0.52)
    GL.glBegin(GL.GL_LINES)
    GL.glVertex2i(0, FLOOR_Y)
    GL.glVertex2i(WIDTH, FLOOR_Y)
    GL.glEnd()

    # Plot individual pixels, not an OpenGL ellipse primitive.
    GL.glColor3f(0.15, 0.8, 1.0)
    GL.glPointSize(2.0)
    GL.glBegin(GL.GL_POINTS)
    for x, y in midpoint_ellipse(animation.a, animation.b):
        GL.glVertex2i(WIDTH // 2 + x, round(animation.yc) + y)
    GL.glEnd()

    GLUT.glutSwapBuffers()


def reshape(width: int, height: int) -> None:
    # Preserve proportions if the user resizes the window.
    scale = min(max(1, width) / WIDTH, max(1, height) / HEIGHT)
    viewport_width, viewport_height = max(1, round(WIDTH * scale)), max(1, round(HEIGHT * scale))
    GL.glViewport((width - viewport_width) // 2, (height - viewport_height) // 2,
                  viewport_width, viewport_height)
    GL.glMatrixMode(GL.GL_PROJECTION)
    GL.glLoadIdentity()
    GL.glOrtho(0, WIDTH, 0, HEIGHT, -1, 1)
    GL.glMatrixMode(GL.GL_MODELVIEW)
    GL.glLoadIdentity()


def keyboard(key: bytes, _x: int, _y: int) -> None:
    if key == b"\x1b":
        GLUT.glutLeaveMainLoop()


def animate(_value: int) -> None:
    animation.step()
    GLUT.glutPostRedisplay()
    GLUT.glutTimerFunc(round(1000 / FPS), animate, 0)


def main() -> None:
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

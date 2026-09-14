"""Lab 1: a Cartesian graph-paper window and one-device-pixel RGB plotting."""

import argparse
import ctypes
import sys

from OpenGL import GL, GLUT

WIDTH, HEIGHT = 960, 720
X_MIN, X_MAX = -480, 479
Y_MIN, Y_MAX = -360, 359


def validate_pixel(x, y, red, green, blue):
    """Use integer coordinates and RGB channels in the inclusive range 0..255."""
    values = (x, y, red, green, blue)
    if any(type(value) is not int for value in values):
        raise ValueError("Coordinates and RGB channels must be integers.")
    if not X_MIN <= x <= X_MAX or not Y_MIN <= y <= Y_MAX:
        raise ValueError(f"Coordinates must be x={X_MIN}..{X_MAX}, y={Y_MIN}..{Y_MAX}.")
    if any(not 0 <= channel <= 255 for channel in (red, green, blue)):
        raise ValueError("RGB channels must be in 0..255.")
    return values


def plot_pixel(x, y, red, green, blue):
    """Draw one pixel. Call only after creating an OpenGL context/projection."""
    validate_pixel(x, y, red, green, blue)
    GL.glPointSize(1.0)
    GL.glColor3ub(red, green, blue)
    GL.glBegin(GL.GL_POINTS)
    # Put the vertex at the CENTER of its device pixel, away from raster edges.
    GL.glVertex2f(x + 0.5, y + 0.5)
    GL.glEnd()


class GraphPaper:
    def __init__(self, pixels):
        self.pixels = {(x, y): (r, g, b) for x, y, r, g, b in pixels}
        self.color = pixels[-1][2:] if pixels else (255, 0, 0)
        self.show_grid = True
        self.viewport = (0, 0, WIDTH, HEIGHT)
        self.window_height = HEIGHT
        self.last_pixel = pixels[-1] if pixels else None

    @staticmethod
    def text(x, y, message):
        GL.glColor3ub(45, 55, 65)
        GL.glRasterPos2f(x, y)
        for character in message:
            GLUT.glutBitmapCharacter(GLUT.GLUT_BITMAP_8_BY_13, ord(character))

    def reshape(self, width, height):
        # A fixed 960x720 viewport preserves one logical pixel = one device pixel.
        # Smaller windows clip the canvas; larger ones add centered margins.
        self.window_height = height
        self.viewport = ((width - WIDTH) // 2, (height - HEIGHT) // 2, WIDTH, HEIGHT)
        GL.glViewport(*self.viewport)
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GL.glOrtho(X_MIN, X_MAX + 1, Y_MIN, Y_MAX + 1, -1, 1)
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()

    def grid(self):
        GL.glLineWidth(1.0)
        GL.glBegin(GL.GL_LINES)
        for x in range(X_MIN, X_MAX + 1, 20):
            GL.glColor3ub(*(195, 205, 215) if x % 100 == 0 else (231, 236, 241))
            GL.glVertex2f(x + 0.5, Y_MIN)
            GL.glVertex2f(x + 0.5, Y_MAX + 1)
        for y in range(Y_MIN, Y_MAX + 1, 20):
            GL.glColor3ub(*(195, 205, 215) if y % 100 == 0 else (231, 236, 241))
            GL.glVertex2f(X_MIN, y + 0.5)
            GL.glVertex2f(X_MAX + 1, y + 0.5)
        GL.glColor3ub(75, 90, 110)
        GL.glVertex2f(X_MIN, 0.5)
        GL.glVertex2f(X_MAX + 1, 0.5)
        GL.glVertex2f(0.5, Y_MIN)
        GL.glVertex2f(0.5, Y_MAX + 1)
        GL.glEnd()
        for x in range(-400, 401, 100):
            if x:
                self.text(x + 3, -17, str(x))
        for y in range(-300, 301, 100):
            if y:
                self.text(7, y + 3, str(y))
        self.text(7, -17, "0")
        self.text(460, 7, "x")
        self.text(7, 340, "y")

    def render(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        if self.show_grid:
            self.grid()
        self.text(-460, 334, "LAB 1 | x: -480..479 | y: -360..359 | RGB: 0..255")
        self.text(-460, 314, "Click: plot | C: clear | G: grid | Esc: exit")
        if self.last_pixel:
            x, y, r, g, b = self.last_pixel
            self.text(-460, -340, f"Last pixel: ({x}, {y})  RGB({r}, {g}, {b})")
        # Draw pixels last so their specified color also wins over grid/labels.
        for (x, y), (r, g, b) in self.pixels.items():
            plot_pixel(x, y, r, g, b)

    def display(self):
        self.render()
        GLUT.glutSwapBuffers()

    def mouse(self, button, state, mouse_x, mouse_y):
        if button != GLUT.GLUT_LEFT_BUTTON or state != GLUT.GLUT_DOWN:
            return
        viewport_x, viewport_y, _, _ = self.viewport
        x = mouse_x - viewport_x + X_MIN
        y = self.window_height - 1 - mouse_y - viewport_y + Y_MIN
        if X_MIN <= x <= X_MAX and Y_MIN <= y <= Y_MAX:
            self.pixels[x, y] = self.color
            self.last_pixel = (x, y, *self.color)
            print(f"Pixel ({x}, {y}), RGB{self.color}", flush=True)
            GLUT.glutPostRedisplay()

    def keyboard(self, key, _x, _y):
        if key == b"\x1b":
            GLUT.glutLeaveMainLoop()
        elif key.lower() == b"c":
            self.pixels.clear()
            self.last_pixel = None
        elif key.lower() == b"g":
            self.show_grid = not self.show_grid
        GLUT.glutPostRedisplay()


def verify_framebuffer(app):
    """Verify actual raster output, including all four coordinate boundaries."""
    samples = [
        (-480, -360, 255, 0, 0), (479, -360, 0, 255, 0),
        (-480, 359, 0, 0, 255), (479, 359, 255, 255, 0),
        (0, 0, 17, 83, 201), (100, 100, 255, 0, 0),
    ]
    app.pixels = {(x, y): (r, g, b) for x, y, r, g, b in samples}
    app.render()
    GL.glFinish()
    GL.glReadBuffer(GL.GL_BACK)
    GL.glPixelStorei(GL.GL_PACK_ALIGNMENT, 1)
    def read_pixel(x, y):
        buffer = ctypes.create_string_buffer(3)
        GL.glReadPixels(x - X_MIN, y - Y_MIN, 1, 1,
                        GL.GL_RGB, GL.GL_UNSIGNED_BYTE, buffer)
        return tuple(buffer.raw)

    for x, y, r, g, b in samples:
        actual = read_pixel(x, y)
        if actual != (r, g, b):
            raise RuntimeError(f"Pixel ({x}, {y}): expected {(r, g, b)}, got {actual}")
    app.show_grid = False
    app.render()
    GL.glFinish()
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            expected = (255, 0, 0) if (dx, dy) == (0, 0) else (255, 255, 255)
            actual = read_pixel(100 + dx, 100 + dy)
            if actual != expected:
                raise RuntimeError(f"Single-pixel coverage failed at offset {(dx, dy)}.")
    renderer = GL.glGetString(GL.GL_RENDERER).decode()
    print(f"PASS: six pixel/color checks and nine single-pixel coverage checks. Renderer: {renderer}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pixel", nargs=5, type=int, action="append",
                        metavar=("X", "Y", "R", "G", "B"),
                        help="Plot a pixel; repeat for multiple pixels. RGB is 0..255.")
    parser.add_argument("--self-test", action="store_true",
                        help="Verify real OpenGL framebuffer coordinates/colors, then exit.")
    args = parser.parse_args()
    pixels = args.pixel if args.pixel is not None else [(100, 100, 255, 0, 0)]
    try:
        for pixel in pixels:
            validate_pixel(*pixel)
    except ValueError as error:
        parser.error(str(error))
    if not bool(GLUT.glutInit):
        parser.exit(1, "GLUT is unavailable. Reinstall the packages in requirements.txt.\n")
    # argparse consumes application options; pass only the program name to GLUT.
    GLUT.glutInit([sys.argv[0]])
    GLUT.glutInitDisplayMode(GLUT.GLUT_DOUBLE | GLUT.GLUT_RGB)
    GLUT.glutInitWindowSize(WIDTH, HEIGHT)
    window = GLUT.glutCreateWindow(b"Lab 1 - Graph Paper and RGB Pixel Plotting")
    GLUT.glutSetOption(GLUT.GLUT_ACTION_ON_WINDOW_CLOSE,
                       GLUT.GLUT_ACTION_GLUTMAINLOOP_RETURNS)
    GL.glClearColor(1.0, 1.0, 1.0, 1.0)
    # Keep exact RGB values and one-pixel coverage (no smoothing or dithering).
    for capability in (GL.GL_DITHER, GL.GL_POINT_SMOOTH, GL.GL_LINE_SMOOTH,
                       GL.GL_BLEND, GL.GL_MULTISAMPLE, GL.GL_DEPTH_TEST):
        GL.glDisable(capability)
    app = GraphPaper(pixels)
    app.reshape(WIDTH, HEIGHT)
    GLUT.glutDisplayFunc(app.display)
    GLUT.glutReshapeFunc(app.reshape)
    GLUT.glutMouseFunc(app.mouse)
    GLUT.glutKeyboardFunc(app.keyboard)
    if args.self_test:
        try:
            verify_framebuffer(app)
        finally:
            GLUT.glutDestroyWindow(window)
        return
    print("Canvas: x=-480..479, y=-360..359. RGB channels: 0..255.")
    for pixel in pixels:
        print(f"Pixel ({pixel[0]}, {pixel[1]}), RGB{tuple(pixel[2:])}")
    print("Click to plot with the last RGB color. C: clear; G: grid; Esc: exit.")
    GLUT.glutMainLoop()


if __name__ == "__main__":
    main()

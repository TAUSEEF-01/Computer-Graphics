"""Lab 6: midpoint ellipse with a repeating drop, compression, and rebound."""

import math  # Square roots used in the shape and motion formulas.
import sys  # Pass the program name to GLUT.
from OpenGL import GL, GLUT  # GL draws pixels; GLUT manages the window and timer.


WIDTH = 960  # Display width in pixels.
HEIGHT = 600  # Display height in pixels.
FLOOR_Y = 45  # Height of the floor above the bottom edge.
FPS = 30  # Animation updates per second.
r = 25.0  # Radius of the initial circle.
xc = WIDTH // 2  # Keep the center horizontally in the middle.

# Start with a = b = r, and preserve a*a + b*b = 2*r*r.
a = b = r  # Equal horizontal and vertical radii form a circle.
top_y = HEIGHT - b - 2  # Place the top of the circle two pixels below the window edge.
yc = top_y  # Start the center at its original top position.
velocity = 0.0  # Begin this motion from rest.
acceleration = 5.0  # Downward acceleration during falling and rising, in pixels/frame squared.
phase = "FALLING"  # Begin the next falling stage.
rise_start_y = 0.0  # Clear the previous launch height.


def reset_animation():  # Restore the circle at the top for another cycle.
    global a, b, yc, top_y, velocity, acceleration, phase, rise_start_y
    a = b = r  # Equal horizontal and vertical radii form a circle.
    top_y = HEIGHT - b - 2  # Place the top of the circle two pixels below the window edge.
    yc = top_y  # Start the center at its original top position.
    velocity = 0.0  # Begin this motion from rest.
    acceleration = 5.0  # Downward acceleration during falling and rising, in pixels/frame squared.
    phase = "FALLING"  # Begin the next falling stage.
    rise_start_y = 0.0  # Clear the previous launch height.


def draw4way_symmetry(x, y):  # Reflect one ellipse point into all four quadrants.
    GL.glVertex2i(xc + x, round(yc) + y)  # Plot the upper-right point relative to the center.
    GL.glVertex2i(xc - x, round(yc) + y)  # Plot the upper-left reflection.
    GL.glVertex2i(xc + x, round(yc) - y)  # Plot the lower-right reflection.
    GL.glVertex2i(xc - x, round(yc) - y)  # Plot the lower-left reflection.


def draw_ellipse():  # Draw the outline using midpoint decisions and symmetry.
    # Start at (a,0) and move toward (0,b).
    rx = max(1, round(a))  # Round the horizontal semiaxis only for pixel drawing.
    ry = max(1, round(b))  # Round the vertical semiaxis only for pixel drawing.
    a2 = rx * rx  # Squared horizontal semiaxis for the decision formulas.
    b2 = ry * ry  # Squared vertical semiaxis for the decision formulas.
    x = rx  # Start at the rightmost ellipse point.
    y = 0  # The rightmost point lies on the horizontal axis.

    GL.glColor3f(0.15, 0.8, 1.0)  # Use cyan for the outline.
    GL.glPointSize(2.0)  # Draw each plotted pixel with a two-pixel point size.
    GL.glBegin(GL.GL_POINTS)  # Begin drawing individual points.

    # Near the right edge: increase y, choosing N or NW.
    decision = b2 * (x - 0.5) ** 2 + a2 - a2 * b2  # Evaluate f(x-1/2, 1) at the first midpoint.
    while a2 * y < b2 * x:  # Use vertical steps while the tangent is steep.
        draw4way_symmetry(x, y)  # Draw this point and its three reflections.
        if decision < 0:  # N
            decision += a2 * (2 * y + 3)  # Update the next midpoint value after an N step.
        else:             # NW
            decision += a2 * (2 * y + 3) + b2 * (-2 * x + 2)  # Update after moving NW; use the old x and y.
            x -= 1  # Move one pixel to the left.
        y += 1  # Move one pixel upward.

    # Near the top: decrease x, choosing W or NW.
    decision = b2 * (x - 1) ** 2 + a2 * (y + 0.5) ** 2 - a2 * b2  # Evaluate the midpoint between W and NW.
    while x >= 0:  # Continue leftward until the vertical axis is reached.
        draw4way_symmetry(x, y)  # Draw this point and its three reflections.
        if decision < 0:  # NW
            decision += b2 * (-2 * x + 3) + a2 * (2 * y + 2)  # Update the midpoint value after an NW step.
            y += 1  # Move one pixel upward.
        else:             # W
            decision += b2 * (-2 * x + 3)  # Update the midpoint value after a W step.
        x -= 1  # Move one pixel to the left.

    GL.glEnd()  # Finish the current group of drawing commands.


def update_animation():  # Advance the drop, compression, or rebound by one frame.
    global a, b, yc, velocity, acceleration, phase, rise_start_y

    if phase == "FALLING":  # Handle downward movement before ground contact.
        velocity += acceleration  # Increase the motion speed by its acceleration.
        yc -= velocity  # Positive velocity moves the center downward.
        if yc - b <= FLOOR_Y:  # Check whether the bottom has reached the floor.
            yc = FLOOR_Y + b  # Keep the bottom on the floor without penetration.
            phase = "COMPRESSING"  # Begin flattening the circle.
            acceleration = 1.0  # Use the slower compression acceleration.
            velocity = 0.0  # Begin this motion from rest.

    elif phase == "COMPRESSING":  # Reduce height and increase width on the floor.
        velocity += acceleration  # Increase the motion speed by its acceleration.
        minimum_b = r * math.sqrt(2 / 5)  # From a=2b and a*a+b*b=2*r*r, solve 5*b*b=2*r*r.
        b = max(minimum_b, b - velocity)  # Compress vertically without exceeding the maximum flattening.
        a = math.sqrt(2 * r * r - b * b)  # Compute width so a*a+b*b stays equal to 2*r*r.
        yc = FLOOR_Y + b  # Keep the bottom on the floor without penetration.
        if b <= minimum_b:  # Maximum flattening has reached a=2b.
            phase = "RISING"  # Begin the upward rebound.
            rise_start_y = yc  # Remember the center height at launch.
            acceleration = 5.0  # Downward acceleration during falling and rising, in pixels/frame squared.
            # Launch speed needed to reach the original top with zero velocity.
            velocity = -math.sqrt(2 * acceleration * (top_y - yc))  # Negative launch speed points up; its magnitude is sqrt(2*g*h).

    elif phase == "RISING":  # Move upward while downward acceleration reduces upward speed.
        # Use the remaining fraction of a frame when reaching the top.
        time_to_top = -velocity / acceleration  # Time remaining until upward velocity reaches zero.
        dt = min(1.0, time_to_top)  # Take one frame or the final fraction of a frame.
        yc -= velocity * dt + 0.5 * acceleration * dt * dt  # Update height using displacement v*dt + g*dt*dt/2.
        velocity += acceleration * dt  # Reduce upward speed toward zero.

        # Gradually recover the circle while preserving a*a + b*b = 2*r*r.
        progress = (yc - rise_start_y) / (top_y - rise_start_y)  # Fraction of the return height already gained.
        progress = min(1.0, max(0.0, progress))  # Keep the recovery fraction between zero and one.
        minimum_b = r * math.sqrt(2 / 5)  # From a=2b and a*a+b*b=2*r*r, solve 5*b*b=2*r*r.
        b = minimum_b + (r - minimum_b) * progress  # Restore the vertical radius gradually toward r.
        a = math.sqrt(2 * r * r - b * b)  # Compute width so a*a+b*b stays equal to 2*r*r.
        if time_to_top <= 1.0:  # The circle reaches its highest point during this frame.
            reset_animation()  # Return to a circle at rest, ready for the next drop.


def display():  # Redraw the complete scene for the current frame.
    GL.glClear(GL.GL_COLOR_BUFFER_BIT)  # Erase the previous frame.
    GL.glLoadIdentity()  # Reset the active transformation matrix.

    GL.glColor3f(0.45, 0.48, 0.52)  # Use gray for the floor.
    GL.glBegin(GL.GL_LINES)  # Begin drawing the floor line.
    GL.glVertex2i(0, FLOOR_Y)  # Left endpoint of the floor.
    GL.glVertex2i(WIDTH, FLOOR_Y)  # Right endpoint of the floor.
    GL.glEnd()  # Finish the current group of drawing commands.

    draw_ellipse()  # Draw the shape at its current size and position.
    GLUT.glutSwapBuffers()  # Show the newly drawn frame without flickering.


def reshape(width, height):  # Keep the scene proportions when the window is resized.
    scale = min(max(1, width) / WIDTH, max(1, height) / HEIGHT)  # Choose the scale that fits both dimensions.
    viewport_width = max(1, round(WIDTH * scale))  # Scaled drawing-area width.
    viewport_height = max(1, round(HEIGHT * scale))  # Scaled drawing-area height.
    GL.glViewport((width - viewport_width) // 2, (height - viewport_height) // 2,
                  viewport_width, viewport_height)
    GL.glMatrixMode(GL.GL_PROJECTION)  # Select the coordinate-system matrix.
    GL.glLoadIdentity()  # Reset the active transformation matrix.
    GL.glOrtho(0, WIDTH, 0, HEIGHT, -1, 1)  # Use pixel-like coordinates with y increasing upward.
    GL.glMatrixMode(GL.GL_MODELVIEW)  # Return to the drawing transformation matrix.
    GL.glLoadIdentity()  # Reset the active transformation matrix.


def keyboard(key, _x, _y):  # Handle the exit key.
    if key == b"\x1b":  # Escape key.
        GLUT.glutLeaveMainLoop()  # Exit the window event loop.


def animate(_value):  # Timer callback that advances and redraws the animation.
    update_animation()  # Calculate the next animation state.
    GLUT.glutPostRedisplay()  # Request a new frame.
    GLUT.glutTimerFunc(round(1000 / FPS), animate, 0)  # Schedule the next update after approximately 33 milliseconds.


def main():  # Create the OpenGL window and register callbacks.
    GLUT.glutInit([sys.argv[0]])  # Initialize the GLUT window toolkit.
    GLUT.glutInitDisplayMode(GLUT.GLUT_DOUBLE | GLUT.GLUT_RGB)  # Use double buffering and RGB colors.
    GLUT.glutInitWindowSize(WIDTH, HEIGHT)  # Set the initial window size.
    GLUT.glutCreateWindow(b"Lab 6 - Falling Circle to Midpoint Ellipse")  # Create the animation window.
    GLUT.glutSetOption(GLUT.GLUT_ACTION_ON_WINDOW_CLOSE,
                       GLUT.GLUT_ACTION_GLUTMAINLOOP_RETURNS)  # Allow closing the window to return from the event loop.
    GL.glClearColor(0.025, 0.035, 0.055, 1.0)  # Set the background color.
    GL.glDisable(GL.GL_DITHER)  # Disable color dithering for consistent pixel colors.
    reshape(WIDTH, HEIGHT)  # Set the initial drawing coordinates.
    GLUT.glutDisplayFunc(display)  # Register the drawing callback.
    GLUT.glutReshapeFunc(reshape)  # Register the window-resize callback.
    GLUT.glutKeyboardFunc(keyboard)  # Register the keyboard callback.
    GLUT.glutTimerFunc(round(1000 / FPS), animate, 0)  # Schedule the next update after approximately 33 milliseconds.
    GLUT.glutMainLoop()  # Process window events until the program is closed.


if __name__ == "__main__":  # Run only when this file is started directly.
    main()  # Start the animation window.


"""Check the invariant, contact constraints, and midpoint raster quality."""

import math
import unittest  # Python standard library for automated checks.
from unittest.mock import patch  # Replace drawing calls temporarily during tests.
from contextlib import ExitStack  # Restore all temporary patches when the block ends.

import falling_ellipse as lab  # Import the actual animation being checked.
from falling_ellipse import FLOOR_Y  # Use the same floor height as the animation.


# Test adapter for the lab's simple global variables and ordinary functions.
class Animation:  # Test adapter for the main program globals; not part of the animation.
    def __init__(self, radius=30.0):
        lab.r = radius  # Select a circle radius for this test.
        lab.reset_animation()  # Reset the actual program state.

    def __getattr__(self, name):
        return getattr(lab, name)  # Read an animation variable from the main module.

    def step(self):
        lab.update_animation()  # Advance the real animation by one frame.

    def reset(self):
        lab.reset_animation()  # Reset the actual program state.


def midpoint_ellipse(a, b):
    vertices = []  # Collect drawn points instead of opening a window.
    with ExitStack() as patches:  # Apply temporary replacements and restore them automatically.
        patches.enter_context(patch.object(lab, 'a', a))  # Temporarily choose the horizontal radius.
        patches.enter_context(patch.object(lab, 'b', b))  # Temporarily choose the vertical radius.
        for name in ('glColor3f', 'glPointSize', 'glBegin', 'glEnd'):
            patches.enter_context(patch.object(lab.GL, name))  # Disable GL calls that require a real window.
        patches.enter_context(patch.object(
            lab.GL, 'glVertex2i',
            side_effect=lambda x, y: vertices.append((x - lab.xc, y - round(lab.yc))),
        ))
        lab.draw_ellipse()  # Run the real midpoint drawing routine.
    return vertices  # Return recorded points for geometric checks.


class AnimationTests(unittest.TestCase):  # Group the automated correctness checks.
    def test_fall_accelerates_and_lands_without_penetrating(self):
        state = Animation()  # Start from the default circle and initial position.
        initial_y = state.yc  # Remember the original top position.
        state.step()  # Simulate one animation frame.
        self.assertEqual(state.velocity, 5)  # Verify the first falling speed.
        self.assertEqual(state.yc, initial_y - 5)  # Verify the first downward displacement.
        state.step()  # Simulate one animation frame.
        self.assertEqual(state.velocity, 10)  # Verify acceleration increases speed on the next frame.
        self.assertEqual(state.yc, initial_y - 15)  # Verify the combined displacement of two frames.
        while state.phase == "FALLING":
            state.step()  # Simulate one animation frame.
            self.assertGreaterEqual(state.yc - state.b, FLOOR_Y - 1e-10)  # Ensure the bottom never passes through the floor.
        self.assertEqual(state.phase, "COMPRESSING")
        self.assertEqual(state.acceleration, 1)  # Verify the slower acceleration at compression.
        self.assertEqual(state.velocity, 0)  # Check the expected moment of rest.

    def test_invariant_and_repeated_drop_compression_rebound(self):
        for radius in (20.0, 90.0, 150.0):  # Check repeated bouncing for several circle sizes.
            with self.subTest(r=radius):  # Report a failing radius separately.
                state = Animation(radius)
                initial_y = state.yc  # Remember the original top position.
                completed_cycles = 0  # Count returns to the top.
                reached_phases = {state.phase}  # Record which animation stages are reached.
                self.assertAlmostEqual(state.a, radius)
                for _ in range(1000):  # Bound the simulation so a broken cycle cannot hang the test.
                    old_a, old_b = state.a, state.b  # Remember the shape before this frame.
                    old_phase = state.phase  # Remember the previous stage to detect transitions.
                    state.step()  # Simulate one animation frame.
                    reached_phases.add(state.phase)  # Record the resulting stage.
                    self.assertAlmostEqual(state.a**2 + state.b**2, 2 * radius**2)  # Check the squared-axis invariant throughout the motion.
                    self.assertLessEqual(state.a / state.b, 2 + 1e-12)  # Ensure flattening never exceeds a=2b.
                    self.assertGreaterEqual(state.yc - state.b, FLOOR_Y - 1e-10)  # Ensure the bottom never passes through the floor.
                    self.assertLessEqual(state.yc + state.b, initial_y + radius + 1e-10)
                    if old_phase in ("FALLING", "COMPRESSING"):
                        self.assertGreaterEqual(state.a, old_a - 1e-12)
                        self.assertLessEqual(state.b, old_b + 1e-12)
                    else:
                        self.assertLessEqual(state.a, old_a + 1e-12)
                        self.assertGreaterEqual(state.b, old_b - 1e-12)
                    if state.phase == "COMPRESSING" or old_phase == "COMPRESSING":
                        self.assertAlmostEqual(state.yc - state.b, FLOOR_Y)  # Ensure ground contact is maintained during compression.
                    if old_phase == "COMPRESSING" and state.phase == "RISING":
                        self.assertAlmostEqual(state.a, 2 * state.b)  # Check the maximum flattening ratio.
                        self.assertAlmostEqual(state.b, radius * math.sqrt(2 / 5))  # Check the derived minimum vertical radius.
                    if old_phase == "RISING" and state.phase == "FALLING":
                        completed_cycles += 1  # Count one full drop and rebound.
                        self.assertEqual(state.yc, initial_y)  # Check the return to the original top position.
                        self.assertEqual(state.velocity, 0)  # Check the expected moment of rest.
                        self.assertEqual(state.a, state.b)  # Check that the recovered shape is a circle.
                        if completed_cycles == 5:  # Five successful cycles are enough for this check.
                            break
                else:
                    self.fail("Animation did not complete five cycles")  # Fail if repeated bouncing stalls.
                self.assertEqual(completed_cycles, 5)
                self.assertEqual(reached_phases, {"FALLING", "COMPRESSING", "RISING"})
                self.assertEqual(state.yc, initial_y)  # Check the return to the original top position.
                self.assertEqual(state.velocity, 0)  # Check the expected moment of rest.
                self.assertAlmostEqual(state.b, radius)
                self.assertEqual(state.a, state.b)  # Check that the recovered shape is a circle.
                state.step()  # Simulate one animation frame.
                self.assertEqual(state.phase, "FALLING")
                self.assertEqual(state.velocity, 5)  # Verify the first falling speed.
                self.assertEqual(state.yc, initial_y - 5)  # Verify the first downward displacement.
                state.reset()
                self.assertEqual(state.phase, "FALLING")
                self.assertEqual(state.yc, initial_y)  # Check the return to the original top position.
                self.assertAlmostEqual(state.a, state.b)

    def test_rebound_launch_speed_and_deceleration(self):
        state = Animation()  # Start from the default circle and initial position.
        for _ in range(1000):  # Bound the simulation so a broken cycle cannot hang the test.
            if state.phase == "RISING":
                break
            state.step()  # Simulate one animation frame.
        self.assertEqual(state.phase, "RISING")
        height = state.top_y - state.yc  # Measure the height the rebound must gain.
        self.assertLess(state.velocity, 0)  # Upward velocity must be negative in this convention.
        self.assertAlmostEqual(state.velocity**2, 2 * state.acceleration * height)  # Check launch speed using v*v=2*g*h.
        old_y, old_velocity, old_b = state.yc, state.velocity, state.b
        state.step()  # Simulate one animation frame.
        self.assertGreater(state.yc, old_y)  # Check upward movement.
        self.assertGreater(state.b, old_b)  # Check that the ellipse recovers height during ascent.
        self.assertAlmostEqual(state.velocity, old_velocity + 5)  # Check downward acceleration during ascent.
        self.assertAlmostEqual(state.yc, old_y - old_velocity - 2.5)

    def test_compression_accelerates_from_rest(self):
        state = Animation()  # Start from the default circle and initial position.
        while state.phase == "FALLING":
            state.step()  # Simulate one animation frame.
        initial_b = state.b
        state.step()  # Simulate one animation frame.
        self.assertAlmostEqual(state.b, initial_b - 1)
        state.step()  # Simulate one animation frame.
        self.assertAlmostEqual(state.b, initial_b - 3)  # Check compression distances of one plus two pixels.

    def test_midpoint_symmetry_continuity_and_curve_distance(self):
        for a, b in ((64, 64), (80, 40), (40, 80), (1, 1), (2, 1)):
            with self.subTest(a=a, b=b):
                outline = list(midpoint_ellipse(a, b))  # Capture all points drawn for these semiaxes.
                quadrant = outline[::4]  # Take the first point from each four-way symmetry group.
                self.assertEqual(quadrant[0], (a, 0))  # Check that drawing starts at the right edge.
                self.assertEqual(quadrant[-1], (0, b))  # Check that drawing ends at the top.
                for previous, current in zip(quadrant, quadrant[1:]):
                    self.assertLessEqual(current[0], previous[0])  # The traced x coordinate must move left or stay unchanged.
                    self.assertGreaterEqual(current[1], previous[1])  # The traced y coordinate must move up or stay unchanged.
                points = set(outline)  # Remove duplicate points before symmetry and connectivity checks.
                self.assertIn((0, b), points)
                self.assertIn((a, 0), points)
                for x, y in points:
                    self.assertIn((-x, y), points)  # Check horizontal reflection.
                    self.assertIn((x, -y), points)  # Check vertical reflection.
                    # Radial difference is bounded by approximately one pixel.
                    radius = math.hypot(x, y)  # Distance from the center to the plotted point.
                    curve_radius = radius / math.sqrt(x*x/(a*a) + y*y/(b*b))
                    self.assertLessEqual(abs(radius - curve_radius), 1)  # Allow at most one pixel of radial rasterization error.
                # Check actual 8-neighbor connectivity, independent of ordering.
                pending = [next(iter(points))]  # Begin exploring the outline from one pixel.
                visited = set(pending)  # Remember pixels already reached.
                while pending:
                    x, y = pending.pop()
                    for dx in (-1, 0, 1):
                        for dy in (-1, 0, 1):
                            neighbor = (x + dx, y + dy)  # Check one of the eight surrounding pixels.
                            if neighbor in points and neighbor not in visited:
                                visited.add(neighbor)  # Record a newly reached outline pixel.
                                pending.append(neighbor)  # Explore this connected pixel next.
                self.assertEqual(visited, points)  # All outline pixels must belong to one connected shape.


if __name__ == "__main__":
    unittest.main()  # Run these checks when this test file is executed directly.


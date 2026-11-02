"""Check the invariant, contact constraints, and midpoint raster quality."""

import math
import unittest

from falling_ellipse import Animation, FLOOR_Y, midpoint_ellipse


class AnimationTests(unittest.TestCase):
    def test_fall_accelerates_and_lands_without_penetrating(self):
        state = Animation()
        initial_y = state.yc
        state.step()
        self.assertEqual(state.velocity, 5)
        self.assertEqual(state.yc, initial_y - 5)
        state.step()
        self.assertEqual(state.velocity, 10)
        self.assertEqual(state.yc, initial_y - 15)
        while state.phase == "FALLING":
            state.step()
            self.assertGreaterEqual(state.yc - state.b, FLOOR_Y - 1e-10)
        self.assertEqual(state.phase, "COMPRESSING")
        self.assertEqual(state.acceleration, 1)
        self.assertEqual(state.velocity, 0)

    def test_invariant_and_repeated_drop_compression_rebound(self):
        for radius in (20.0, 90.0, 150.0):
            with self.subTest(r=radius):
                state = Animation(radius)
                initial_y = state.yc
                completed_cycles = 0
                reached_phases = {state.phase}
                self.assertAlmostEqual(state.a, radius / math.sqrt(2))
                for _ in range(1000):
                    old_a, old_b = state.a, state.b
                    old_phase = state.phase
                    state.step()
                    reached_phases.add(state.phase)
                    self.assertAlmostEqual(state.a**2 + state.b**2, radius**2)
                    self.assertLessEqual(state.a / state.b, 2 + 1e-12)
                    self.assertGreaterEqual(state.yc - state.b, FLOOR_Y - 1e-10)
                    self.assertLessEqual(state.yc + state.b, initial_y + radius / math.sqrt(2) + 1e-10)
                    if old_phase in ("FALLING", "COMPRESSING"):
                        self.assertGreaterEqual(state.a, old_a - 1e-12)
                        self.assertLessEqual(state.b, old_b + 1e-12)
                    else:
                        self.assertLessEqual(state.a, old_a + 1e-12)
                        self.assertGreaterEqual(state.b, old_b - 1e-12)
                    if state.phase == "COMPRESSING" or old_phase == "COMPRESSING":
                        self.assertAlmostEqual(state.yc - state.b, FLOOR_Y)
                    if old_phase == "COMPRESSING" and state.phase == "RISING":
                        self.assertAlmostEqual(state.a, 2 * state.b)
                        self.assertAlmostEqual(state.b, radius / math.sqrt(5))
                    if old_phase == "RISING" and state.phase == "FALLING":
                        completed_cycles += 1
                        self.assertEqual(state.yc, initial_y)
                        self.assertEqual(state.velocity, 0)
                        self.assertEqual(state.a, state.b)
                        if completed_cycles == 5:
                            break
                else:
                    self.fail("Animation did not complete five cycles")
                self.assertEqual(completed_cycles, 5)
                self.assertEqual(reached_phases, {"FALLING", "COMPRESSING", "RISING"})
                self.assertEqual(state.yc, initial_y)
                self.assertEqual(state.velocity, 0)
                self.assertAlmostEqual(state.b, radius / math.sqrt(2))
                self.assertEqual(state.a, state.b)
                state.step()
                self.assertEqual(state.phase, "FALLING")
                self.assertEqual(state.velocity, 5)
                self.assertEqual(state.yc, initial_y - 5)
                state.reset()
                self.assertEqual(state.phase, "FALLING")
                self.assertEqual(state.yc, initial_y)
                self.assertAlmostEqual(state.a, state.b)

    def test_rebound_launch_speed_and_deceleration(self):
        state = Animation()
        for _ in range(1000):
            if state.phase == "RISING":
                break
            state.step()
        self.assertEqual(state.phase, "RISING")
        height = state.top_y - state.yc
        self.assertLess(state.velocity, 0)
        self.assertAlmostEqual(state.velocity**2, 2 * state.acceleration * height)
        old_y, old_velocity, old_b = state.yc, state.velocity, state.b
        state.step()
        self.assertGreater(state.yc, old_y)
        self.assertGreater(state.b, old_b)
        self.assertAlmostEqual(state.velocity, old_velocity + 5)
        self.assertAlmostEqual(state.yc, old_y - old_velocity - 2.5)

    def test_compression_accelerates_from_rest(self):
        state = Animation()
        while state.phase == "FALLING":
            state.step()
        initial_b = state.b
        state.step()
        self.assertAlmostEqual(state.b, initial_b - 1)
        state.step()
        self.assertAlmostEqual(state.b, initial_b - 3)

    def test_midpoint_symmetry_continuity_and_curve_distance(self):
        for a, b in ((64, 64), (80, 40), (40, 80), (1, 1), (2, 1)):
            with self.subTest(a=a, b=b):
                outline = list(midpoint_ellipse(a, b))
                quadrant = outline[::4]
                self.assertEqual(quadrant[0], (a, 0))
                self.assertEqual(quadrant[-1], (0, b))
                for previous, current in zip(quadrant, quadrant[1:]):
                    self.assertLessEqual(current[0], previous[0])
                    self.assertGreaterEqual(current[1], previous[1])
                points = set(outline)
                self.assertIn((0, b), points)
                self.assertIn((a, 0), points)
                for x, y in points:
                    self.assertIn((-x, y), points)
                    self.assertIn((x, -y), points)
                    # Radial difference is bounded by approximately one pixel.
                    radius = math.hypot(x, y)
                    curve_radius = radius / math.sqrt(x*x/(a*a) + y*y/(b*b))
                    self.assertLessEqual(abs(radius - curve_radius), 1)
                # Check actual 8-neighbor connectivity, independent of ordering.
                pending = [next(iter(points))]
                visited = set(pending)
                while pending:
                    x, y = pending.pop()
                    for dx in (-1, 0, 1):
                        for dy in (-1, 0, 1):
                            neighbor = (x + dx, y + dy)
                            if neighbor in points and neighbor not in visited:
                                visited.add(neighbor)
                                pending.append(neighbor)
                self.assertEqual(visited, points)


if __name__ == "__main__":
    unittest.main()

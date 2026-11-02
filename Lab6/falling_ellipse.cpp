// Lab 6: repeating circle drop, compression, and rebound.
// Preserve a*a + b*b = r*r, so the initial circle radius is r/sqrt(2).
#include <GL/freeglut.h>
#include <algorithm>
#include <cmath>
#include <utility>
#include <vector>

constexpr int WIDTH = 960;
constexpr int HEIGHT = 600;
constexpr int FLOOR_Y = 45;
constexpr double R = 30.0;
constexpr int FPS = 30;
constexpr double FALL_ACCELERATION = 5.0; // pixels/frame^2
constexpr double COMPRESSION_ACCELERATION = 1.0;
constexpr int FRAME_MS = (1000 + FPS / 2) / FPS;

using Pixel = std::pair<int, int>;

std::vector<Pixel> midpointEllipse(double a, double b)
{
    // Round only for drawing. Animation keeps floating-point semiaxes.
    // Swap axes locally: x is vertical, y is horizontal. Map (x,y) back
    // to (y,x) to trace from (a,0) toward (0,b).
    const int rx = std::max(1, static_cast<int>(std::round(b)));
    const int ry = std::max(1, static_cast<int>(std::round(a)));
    const double rx2 = static_cast<double>(rx) * rx;
    const double ry2 = static_cast<double>(ry) * ry;
    int x = 0, y = ry;
    std::vector<Pixel> pixels;

    auto plotFour = [&]()
    {
        pixels.emplace_back(y, x);
        pixels.emplace_back(-y, x);
        pixels.emplace_back(y, -x);
        pixels.emplace_back(-y, -x);
    };

    // Local Region 1: midpoint (x+1, y-1/2); maps to N or NW.
    // All increments use the OLD coordinates, before moving.
    double decision = ry2 - rx2 * ry + 0.25 * rx2;
    while (ry2 * x < rx2 * y)
    {
        plotFour();
        if (decision < 0)
        {
            decision += ry2 * (2 * x + 3);
        }
        else
        {
            decision += ry2 * (2 * x + 3) + rx2 * (-2 * y + 2);
            --y;
        }
        ++x;
    }

    // Local Region 2: midpoint (x+1/2, y-1); maps to W or NW.
    decision = ry2 * (x + 0.5) * (x + 0.5) + rx2 * (y - 1) * (y - 1) - rx2 * ry2;
    while (y >= 0)
    {
        plotFour();
        if (decision < 0)
        {
            decision += ry2 * (2 * x + 2) + rx2 * (-2 * y + 3);
            ++x;
        }
        else
        {
            decision += rx2 * (-2 * y + 3);
        }
        --y;
    }
    return pixels;
}

enum class Phase
{
    Falling,
    Compressing,
    Rising
};

struct Animation
{
    double r;
    double a, b, yc;
    double velocity, acceleration, riseStartY;
    Phase phase;

    explicit Animation(double radius = R) : r(radius)
    {
        reset();
    }

    double topY() const
    {
        return HEIGHT - r / std::sqrt(2.0) - 2;
    }

    void reset()
    {
        a = b = r / std::sqrt(2.0);
        yc = topY();
        velocity = 0;
        acceleration = FALL_ACCELERATION;
        riseStartY = 0;
        phase = Phase::Falling;
    }

    void step()
    {
        // Positive velocity points down; negative velocity points up.
        if (phase == Phase::Falling)
        {
            velocity += acceleration;
            yc -= velocity;
            if (yc - b <= FLOOR_Y)
            {
                yc = FLOOR_Y + b;
                phase = Phase::Compressing;
                acceleration = COMPRESSION_ACCELERATION;
                velocity = 0; // compression starts from rest at contact
            }
        }
        else if (phase == Phase::Compressing)
        {
            velocity += acceleration;
            const double minimumB = r / std::sqrt(5.0);
            b = std::max(minimumB, b - velocity);
            a = std::sqrt(r * r - b * b);
            yc = FLOOR_Y + b;

            // At a=2b, launch upward with enough speed to reach the top.
            if (b <= minimumB)
            {
                phase = Phase::Rising;
                riseStartY = yc;
                acceleration = FALL_ACCELERATION;
                const double height = topY() - yc;
                velocity = -std::sqrt(2 * acceleration * height);
            }
        }
        else if (phase == Phase::Rising)
        {
            // Use a fractional last frame to arrive at the apex at rest.
            const double timeToTop = -velocity / acceleration;
            const double dt = std::min(1.0, timeToTop);
            yc -= velocity * dt + 0.5 * acceleration * dt * dt;
            velocity += acceleration * dt;

            // Recover the circle progressively while preserving the invariant.
            double progress = (yc - riseStartY) / (topY() - riseStartY);
            progress = std::min(1.0, std::max(0.0, progress));
            const double minimumB = r / std::sqrt(5.0);
            const double circleRadius = r / std::sqrt(2.0);
            b = minimumB + (circleRadius - minimumB) * progress;
            a = std::sqrt(r * r - b * b);

            // At the top: circle, zero velocity; fall again next frame.
            if (timeToTop <= 1.0)
            {
                reset();
            }
        }
    }
};

Animation animation;

void display()
{
    glClear(GL_COLOR_BUFFER_BIT);
    glLoadIdentity();

    glColor3f(0.45f, 0.48f, 0.52f);
    glBegin(GL_LINES);
    glVertex2i(0, FLOOR_Y);
    glVertex2i(WIDTH, FLOOR_Y);
    glEnd();

    glColor3f(0.15f, 0.8f, 1.0f);
    glPointSize(2.0f);
    const int centerY = static_cast<int>(std::round(animation.yc));
    const auto pixels = midpointEllipse(animation.a, animation.b);
    glBegin(GL_POINTS);
    for (const Pixel &pixel : pixels)
    {
        glVertex2i(WIDTH / 2 + pixel.first, centerY + pixel.second);
    }
    glEnd();
    glutSwapBuffers();
}

void reshape(int width, int height)
{
    const double scale = std::min(std::max(1, width) / static_cast<double>(WIDTH),
                                  std::max(1, height) / static_cast<double>(HEIGHT));
    const int viewportWidth = std::max(1, static_cast<int>(std::round(WIDTH * scale)));
    const int viewportHeight = std::max(1, static_cast<int>(std::round(HEIGHT * scale)));
    glViewport((width - viewportWidth) / 2, (height - viewportHeight) / 2,
               viewportWidth, viewportHeight);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    glOrtho(0, WIDTH, 0, HEIGHT, -1, 1);
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
}

void keyboard(unsigned char key, int, int)
{
    if (key == 27)
    {
        glutLeaveMainLoop();
    }
}

void animate(int)
{
    animation.step();
    glutPostRedisplay();
    glutTimerFunc(FRAME_MS, animate, 0);
}

int main(int argc, char **argv)
{
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB);
    glutInitWindowSize(WIDTH, HEIGHT);
    glutCreateWindow("Lab 6 - Falling Circle to Midpoint Ellipse (C++)");
    glutSetOption(GLUT_ACTION_ON_WINDOW_CLOSE, GLUT_ACTION_GLUTMAINLOOP_RETURNS);
    glClearColor(0.025f, 0.035f, 0.055f, 1.0f);
    glDisable(GL_DITHER);
    reshape(WIDTH, HEIGHT);
    glutDisplayFunc(display);
    glutReshapeFunc(reshape);
    glutKeyboardFunc(keyboard);
    glutTimerFunc(FRAME_MS, animate, 0);
    glutMainLoop();
    return 0;
}

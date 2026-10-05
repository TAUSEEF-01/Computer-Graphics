// Lab 4: radius-250 DDA lines with a different color for each of eight zones.
#include <GL/freeglut.h>
#include <algorithm>
#include <cmath>
#include <iostream>

constexpr int WINDOW_WIDTH = 960;
constexpr int WINDOW_HEIGHT = 540;
constexpr int RADIUS = 250;
constexpr int ANGLE_STEP = 5;
constexpr bool PRINT_POINTS = false;
constexpr double PI = 3.14159265358979323846;

const char* ZONE_NAMES[] = {
    "cyan", "magenta", "yellow", "red", "green", "orange", "black", "blue"
};

const GLfloat ZONE_COLORS[8][3] = {
    {0.0f, 1.0f, 1.0f},  // Zone 0: cyan
    {1.0f, 0.0f, 1.0f},  // Zone 1: magenta
    {1.0f, 1.0f, 0.0f},  // Zone 2: yellow
    {1.0f, 0.0f, 0.0f},  // Zone 3: red
    {0.0f, 1.0f, 0.0f},  // Zone 4: green
    {1.0f, 0.5f, 0.0f},  // Zone 5: orange
    {0.0f, 0.0f, 0.0f},  // Zone 6: black
    {0.0f, 0.0f, 1.0f}   // Zone 7: blue
};

int sign(double value) {
    if (value > 0) return 1;
    if (value < 0) return -1;
    return 0;
}

int round_coordinate(double value) {
    return static_cast<int>(value + 0.5 * sign(value));
}

int find_zone(int x0, int y0, int x1, int y1) {
    int dx = x1 - x0;
    int dy = y1 - y0;
    if (dx >= 0 && dy >= 0)
        return std::abs(dx) >= std::abs(dy) ? 0 : 1;
    if (dx < 0 && dy >= 0)
        return std::abs(dx) >= std::abs(dy) ? 3 : 2;
    if (dx < 0 && dy < 0)
        return std::abs(dx) >= std::abs(dy) ? 4 : 5;
    return std::abs(dx) >= std::abs(dy) ? 7 : 6;
}

void plot_dda_points(double x, double y, int step,
                     double x_increment, double y_increment, int zone) {
    glColor3fv(ZONE_COLORS[zone]);
    glPointSize(2.0f);
    glBegin(GL_POINTS);
    for (int i = 0; i <= step; ++i) {
        int rounded_x = static_cast<int>(x + 0.5 * sign(x));
        int rounded_y = static_cast<int>(y + 0.5 * sign(y));
        if (PRINT_POINTS) {
            std::cout << "Plotting point: (" << rounded_x << ", "
                      << rounded_y << ")\n";
        }
        glVertex2i(rounded_x, rounded_y);
        x += x_increment;
        y += y_increment;
    }
    glEnd();
}

// Right and up, shallow: x increases by 1.
void drawLine_0(int x0, int y0, int x1, int y1) {
    int dx = x1 - x0, dy = y1 - y0;
    int step = dx;
    plot_dda_points(x0, y0, step, 1,
                    step ? static_cast<double>(dy) / step : 0, 0);
}

// Right and up, steep: y increases by 1.
void drawLine_1(int x0, int y0, int x1, int y1) {
    int dx = x1 - x0, dy = y1 - y0;
    int step = dy;
    plot_dda_points(x0, y0, step, static_cast<double>(dx) / step, 1, 1);
}

// Left and up, steep: y increases by 1.
void drawLine_2(int x0, int y0, int x1, int y1) {
    int dx = x1 - x0, dy = y1 - y0;
    int step = dy;
    plot_dda_points(x0, y0, step, static_cast<double>(dx) / step, 1, 2);
}

// Left and up, shallow: x decreases by 1.
void drawLine_3(int x0, int y0, int x1, int y1) {
    int dx = x1 - x0, dy = y1 - y0;
    int step = -dx;
    plot_dda_points(x0, y0, step, -1, static_cast<double>(dy) / step, 3);
}

// Left and down, shallow: x decreases by 1.
void drawLine_4(int x0, int y0, int x1, int y1) {
    int dx = x1 - x0, dy = y1 - y0;
    int step = -dx;
    plot_dda_points(x0, y0, step, -1, static_cast<double>(dy) / step, 4);
}

// Left and down, steep: y decreases by 1.
void drawLine_5(int x0, int y0, int x1, int y1) {
    int dx = x1 - x0, dy = y1 - y0;
    int step = -dy;
    plot_dda_points(x0, y0, step, static_cast<double>(dx) / step, -1, 5);
}

// Right and down, steep: y decreases by 1.
void drawLine_6(int x0, int y0, int x1, int y1) {
    int dx = x1 - x0, dy = y1 - y0;
    int step = -dy;
    plot_dda_points(x0, y0, step, static_cast<double>(dx) / step, -1, 6);
}

// Right and down, shallow: x increases by 1.
void drawLine_7(int x0, int y0, int x1, int y1) {
    int dx = x1 - x0, dy = y1 - y0;
    int step = dx;
    plot_dda_points(x0, y0, step, 1, static_cast<double>(dy) / step, 7);
}

using DrawFunction = void (*)(int, int, int, int);
const DrawFunction DRAW_FUNCTIONS[] = {
    drawLine_0, drawLine_1, drawLine_2, drawLine_3,
    drawLine_4, drawLine_5, drawLine_6, drawLine_7
};

void drawLine(int x0, int y0, int x1, int y1) {
    int zone = find_zone(x0, y0, x1, y1);
    DRAW_FUNCTIONS[zone](x0, y0, x1, y1);
}

void display() {
    glClear(GL_COLOR_BUFFER_BIT);
    // 36 diameters, each drawn as two separately colored half-lines.
    for (int angle = 0; angle < 180; angle += ANGLE_STEP) {
        double radians = angle * PI / 180.0;
        int x = round_coordinate(RADIUS * std::cos(radians));
        int y = round_coordinate(RADIUS * std::sin(radians));
        drawLine(0, 0, x, y);
        drawLine(0, 0, -x, -y);
    }
    glutSwapBuffers();
}

// Python round() rounds ties to even; reproduce that for viewport dimensions.
int round_viewport(double value) {
    int lower = static_cast<int>(std::floor(value));
    double fraction = value - lower;
    if (fraction < 0.5) return lower;
    if (fraction > 0.5) return lower + 1;
    return lower % 2 == 0 ? lower : lower + 1;
}

void reshape(int width, int height) {
    double scale = std::min(static_cast<double>(width) / WINDOW_WIDTH,
                            static_cast<double>(height) / WINDOW_HEIGHT);
    int viewport_width = round_viewport(WINDOW_WIDTH * scale);
    int viewport_height = round_viewport(WINDOW_HEIGHT * scale);
    glViewport((width - viewport_width) / 2,
               (height - viewport_height) / 2,
               viewport_width, viewport_height);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    glOrtho(-480, 480, -270, 270, -1, 1);
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
}

int main(int argc, char** argv) {
    for (int zone = 0; zone < 8; ++zone) {
        std::cout << "Zone " << zone << ": " << ZONE_NAMES[zone]
                  << ", function: drawLine_" << zone << '\n';
    }
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB);
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT);
    glutCreateWindow("Lab 4 - Eight DDA Zones");
    glutSetOption(GLUT_ACTION_ON_WINDOW_CLOSE,
                  GLUT_ACTION_GLUTMAINLOOP_RETURNS);
    glClearColor(0.65f, 0.65f, 0.65f, 1.0f);
    glDisable(GL_DITHER);
    reshape(WINDOW_WIDTH, WINDOW_HEIGHT);
    glutDisplayFunc(display);
    glutReshapeFunc(reshape);
    glutMainLoop();
    return 0;
}

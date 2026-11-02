#define main labMain
#include "../../falling_ellipse.cpp"
#undef main
#include <iomanip>
#include <iostream>
#include <string>

int completedCycles = 0;
int glError = 0;
void smokeTick(int) {
    const Phase previous = animation.phase;
    animation.step();
    if (previous == Phase::Rising && animation.phase == Phase::Falling) {
        ++completedCycles;
    }
    display();
    glError |= glGetError();
    if (completedCycles >= 3) {
        glutLeaveMainLoop();
    } else {
        glutTimerFunc(1, smokeTick, 0);
    }
}

int main(int argc, char** argv) {
    if (argc > 1 && std::string(argv[1]) == "--smoke") {
        glutInit(&argc, argv);
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB);
        glutInitWindowSize(WIDTH, HEIGHT);
        glutCreateWindow("Lab 6 C++ rendering check");
        glutSetOption(GLUT_ACTION_ON_WINDOW_CLOSE, GLUT_ACTION_GLUTMAINLOOP_RETURNS);
        glClearColor(0.025f, 0.035f, 0.055f, 1.0f);
        reshape(WIDTH, HEIGHT);
        glutDisplayFunc(display);
        glutReshapeFunc(reshape);
        glutTimerFunc(1, smokeTick, 0);
        glutMainLoop();
        if (completedCycles != 3 || glError != 0) return 1;
        std::cout << "C++ OpenGL rendering: three complete cycles, no GL errors.\n";
        return 0;
    }
    std::cout << std::setprecision(17);
    for (double radius : {20.0, 30.0, 90.0, 150.0}) {
        Animation state(radius);
        for (int frame = 0; frame < 250; ++frame) {
            std::cout << radius << ' ' << frame << ' ' << static_cast<int>(state.phase)
                      << ' ' << state.a << ' ' << state.b << ' ' << state.yc
                      << ' ' << state.velocity << ' ' << state.acceleration << '|';
            for (const Pixel& p : midpointEllipse(state.a, state.b)) {
                std::cout << p.first << ',' << p.second << ';';
            }
            std::cout << '\n';
            state.step();
        }
    }
}

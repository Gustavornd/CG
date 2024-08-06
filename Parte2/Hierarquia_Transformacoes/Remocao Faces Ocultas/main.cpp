#include <GL/glut.h>

void init() {
    // Configura o buffer de profundidade
    glEnable(GL_DEPTH_TEST);
    glDepthFunc(GL_LESS);

    // Habilitar a remoção de faces ocultas
    glEnable(GL_CULL_FACE);
    glCullFace(GL_BACK); // Descartar as faces traseiras (padrão)
    glFrontFace(GL_CCW); // Sentido anti-horário define uma face frontal (padrão)
}

void display() {
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

    // Desenha uma cena simples com dois triângulos
    glBegin(GL_TRIANGLES);
        // Triângulo 1 (face frontal voltada para a câmera)
        glColor3f(1.0, 0.0, 0.0);
        glVertex3f(-0.5f, -0.5f, -1.0f);
        glVertex3f( 0.5f, -0.5f, -1.0f);
        glVertex3f( 0.0f,  0.5f, -1.0f);

        // Triângulo 2 (face traseira voltada para a câmera)
        glColor3f(0.0, 1.0, 0.0);
        glVertex3f( 0.5f, -0.5f,  -1.0f);
        glVertex3f(-0.5f, -0.5f,  -1.0f);
        glVertex3f( 0.0f,  0.5f,  -1.0f);
    glEnd();

    glutSwapBuffers();
}

int main(int argc, char** argv) {
    glutInit(&argc, argv);
    glutInitWindowSize(600, 600);
    glutInitWindowPosition(100, 100);

    // Solicitar um buffer de cor e um buffer de profundidade
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH);

    glutCreateWindow("Remoção de Faces Ocultas com glCullFace");

    init();

    glutDisplayFunc(display);
    glutMainLoop();

    return 0;
}

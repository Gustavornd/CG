#include <GL/glut.h>

// Define a cor de fundo com alpha (transparente)
void init() {
    glClearColor(0.0f, 0.0f, 0.0f, 1.0f); 
    glEnable(GL_BLEND);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
}

// Função para desenhar a cena
void display() {
    glClear(GL_COLOR_BUFFER_BIT);

    // Desenha um quadrado azul opaco
    glColor4f(0.0f, 0.0f, 1.0f, 1.0f);
    glBegin(GL_QUADS);
        glVertex2f(-0.5f, -0.5f);
        glVertex2f( 0.5f, -0.5f);
        glVertex2f( 0.5f,  0.5f);
        glVertex2f(-0.5f,  0.5f);
    glEnd();

    // Desenha um quadrado verde com 75% de transparência
    glColor4f(0.0f, 1.0f, 0.0f, 0.25f);
    glBegin(GL_QUADS);
        glVertex2f(-0.25f, -0.25f);
        glVertex2f( 0.75f, -0.25f);
        glVertex2f( 0.75f,  0.75f);
        glVertex2f(-0.25f,  0.75f);
    glEnd();

    glFlush();
}

int main(int argc, char** argv) {
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA);
    glutInitWindowSize(400, 400);
    glutCreateWindow("Exemplo de Transparencia com OpenGL e stb_image");

    init();
    glutDisplayFunc(display);
    glutMainLoop();
    return 0;
}

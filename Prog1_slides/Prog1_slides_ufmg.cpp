#include <GL/glut.h>
void INIT(int argc, char** argv)
{
    glutInit(&argc, argv); 
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB); 
    glutInitWindowSize(450, 450); 
    glutInitWindowPosition(50, 50);
    glutCreateWindow("Primeiros Passos em OpenGL");

    // configurando o volume de visualização 
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    glOrtho(-800.0, 800.0, -800.0, 800.0, -800.0, 800.0);  

    // mudando a cor do fundo para vermelho
    glClearColor(1.0, 0.0, 0.0, 0.0);
}

void DISPLAY(void)
{
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    glClear(GL_COLOR_BUFFER_BIT);
    glFlush();
}

int main(int argc, char** argv) 
{
    INIT(argc, argv);                                                 
    glutDisplayFunc(DISPLAY);               
    glutMainLoop();
    return 0;
}

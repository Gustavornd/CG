#include <GL/glut.h>

float angle = 0.0f;       // Ângulo de rotação dos objetos
bool wireframe = false;  // Estado do modo (sólido ou aramado)

// Função de inicialização
void init() {
    glClearColor(0.0, 0.0, 0.0, 1.0); // Cor de fundo preta
    glEnable(GL_DEPTH_TEST);          // Habilita o teste de profundidade
    glEnable(GL_LIGHTING);            // Habilita o sistema de iluminação
    glEnable(GL_LIGHT0);              // Habilita a luz 0
    glEnable(GL_COLOR_MATERIAL);      // Permite que as cores dos materiais sejam usadas
    glShadeModel(GL_SMOOTH);          // Suaviza as cores dos objetos

    // Define as propriedades da luz
    GLfloat light_ambient[] = {0.2, 0.2, 0.2, 1.0}; // Luz ambiente
    GLfloat light_diffuse[] = {1.0, 1.0, 1.0, 1.0}; // Luz difusa
    GLfloat light_specular[] = {1.0, 1.0, 1.0, 1.0}; // Luz especular
    GLfloat light_position[] = {1.0, 1.0, 1.0, 0.0}; // Posição da luz

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient);
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse);
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular);
    glLightfv(GL_LIGHT0, GL_POSITION, light_position);

    // Define as propriedades do material
    GLfloat mat_ambient[] = {0.2, 0.2, 0.2, 1.0};
    GLfloat mat_diffuse[] = {0.8, 0.8, 0.8, 1.0};
    GLfloat mat_specular[] = {1.0, 1.0, 1.0, 1.0};
    GLfloat mat_shininess[] = {50.0}; // Brilho dos materiais

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient);
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse);
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular);
    glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess);
}

// Função de exibição
void display() {
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT); // Limpa os buffers de cor e profundidade

    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();

    // Define a posição da câmera
    gluLookAt(0.0, 0.0, 5.0,   // Posição da câmera
              0.0, 0.0, 0.0,   // Ponto de observação
              0.0, 1.0, 0.0);  // Vetor de cima

    // Define o modo de desenho (sólido ou aramado)
    if (wireframe) {
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE); // Modo aramado
    } else {
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL);  // Modo sólido
    }

    // Rotaciona e desenha uma esfera usando GLU
    glColor3f(1.0, 0.0, 0.0);  // Cor vermelha
    GLUquadric* quad = gluNewQuadric();
    glPushMatrix();
    glTranslatef(-1.5, 1.0, 0.0);
    glRotatef(angle, 0.0, 1.0, 0.0); // Rotaciona a esfera
    gluSphere(quad, 0.5, 32, 32);
    glPopMatrix();

    // Rotaciona e desenha um cilindro usando GLU
    glColor3f(0.0, 1.0, 0.0);  // Cor verde
    glPushMatrix();
    glTranslatef(1.5, 1.0, 0.0);
    glRotatef(angle, 0.0, 1.0, 0.0); // Rotaciona o cilindro
    gluCylinder(quad, 0.3, 0.3, 1.0, 32, 32);
    glPopMatrix();

    // Rotaciona e desenha um disco usando GLU
    glColor3f(0.0, 0.0, 1.0);  // Cor azul
    glPushMatrix();
    glTranslatef(-1.5, -1.0, 0.0);
    glRotatef(angle, 0.0, 1.0, 0.0); // Rotaciona o disco
    gluDisk(quad, 0.2, 0.5, 32, 32);
    glPopMatrix();

    // Rotaciona e desenha um cubo usando GLUT
    glColor3f(1.0, 1.0, 0.0);  // Cor amarela
    glPushMatrix();
    glTranslatef(1.5, -1.0, 0.0);
    glRotatef(angle, 0.0, 1.0, 0.0); // Rotaciona o cubo
    glutSolidCube(1.0);
    glPopMatrix();

    // Rotaciona e desenha um bule de chá usando GLUT
    glColor3f(1.0, 0.5, 0.0);  // Cor laranja
    glPushMatrix();
    glTranslatef(0.0, 0.0, 0.0);
    glRotatef(angle, 0.0, 1.0, 0.0); // Rotaciona o bule de chá
    glutSolidTeapot(0.5);
    glPopMatrix();

    glutSwapBuffers(); // Troca os buffers para exibição suave
}

// Função de redimensionamento da janela
void reshape(int w, int h) {
    glViewport(0, 0, w, h);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluPerspective(45.0, (float)w / (float)h, 1.0, 100.0);
}

// Função de animação
void animate(int value) {
    angle += 1.0f; // Incrementa o ângulo de rotação
    if (angle > 360) {
        angle -= 360; // Mantém o ângulo dentro de 0-360 graus
    }
    glutPostRedisplay(); // Solicita a atualização da tela
    glutTimerFunc(16, animate, 0); // Define o próximo frame (aproximadamente 60 fps)
}

// Função para alternar entre sólido e aramado
void keyboard(unsigned char key, int x, int y) {
    if (key == 32) { // Tecla espaço
        wireframe = !wireframe; // Alterna o modo
    }
}

// Função principal
int main(int argc, char** argv) {
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH);
    glutInitWindowSize(800, 600);
    glutCreateWindow("Exemplo de Figuras GLU e GLUT com Iluminação e Brilho");

    init();
    glutDisplayFunc(display);
    glutReshapeFunc(reshape);
    glutKeyboardFunc(keyboard);
    glutTimerFunc(16, animate, 0); // Inicia a animação

    glutMainLoop();
    return 0;
}

/*
 * Programa mínimo de teste da OpenGL/GLUT C/C++
 * Testado com VSCODE e Msys2
 * Para compilar use -lopengl32 -lglu32  -lfreeglut
 */
#include <GL/glut.h>  // a biblioteca GLUT inclui glu.h e gl.h
 
/* Handler para o evento de repintura da janela. Chamado quando a janela aparece pela primeira vez 
   e sempre que a janela precisa ser re-exbida. */
void display() {
   glClear(GL_COLOR_BUFFER_BIT);         // limpa o buffer de desenho (limpa a tela com a cor de fundo)
 
   // Desenhar um quadrado vermelho de 1x1 centrado na origem...
   glColor3f(1.0f, 0.0f, 0.0f); // aplica a cor vermelha
   glBegin(GL_QUADS);              
      glVertex2f(-0.5f, -0.5f);    // x, y
      glVertex2f( 0.5f, -0.5f);
      glVertex2f( 0.5f,  0.5f);
      glVertex2f(-0.5f,  0.5f);
   glEnd();
 
   glFlush();  // Render now (if DisplayMode is SINGLE use glFlush otherwise use glutSwapBuffers)
}

void Init(int argc, char** argv)
{
   glutInit(&argc, argv);                 // Inicializa a GLUT
   glutCreateWindow("Alô Mundo da OpenGL"); // Cria uma janela com o título informado
   glutInitWindowSize(640, 640);   // Atribui os dimensões iniciais da janela 
   glutInitWindowPosition(50, 50); // Posiciona a janela no canto superior esquerdo afastado de (50, 50)
   glClearColor(0.0f, 0.0f, 0.0f, 1.0f); // aplica a cor de limpeza para preto opaco (este é o default)
}

/* função principal: a GLUT roda em uma aplicação de console iniciando pela main */
int main(int argc, char** argv) {
   Init(argc, argv);
   glutDisplayFunc(display); // Registra a função de desenho e re-desenho da janela (viewport)
   glutMainLoop();           // entra no loop infinito de processamento de eventos da opengl...
   return 0;
}
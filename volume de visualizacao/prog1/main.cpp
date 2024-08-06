/*
                                Introdução à

                   |---|  |--\  |---  |\   |  /---\  |
                   |   |  |__|  |___  | \  |  |      |
                   |   |  |     |     |  \ |  |  -+- |
                   \---/  |     |---  |   \|  \---|  \----

                             Volume de Visualização 
*/

#include <GL\glut.h>
bool flag_ortho = true;

int posX = 0,
    posY = 0;

void IniciarJanela(const char* nomeJanela, int largura=500, int altura=500)
{
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH );
    glutInitWindowSize(largura, altura);
    glutInitWindowPosition(50, 50);
    glutCreateWindow(nomeJanela);
    glClearColor(0.0, 0.0, 0.0, 0.0);
    glEnable(GL_DEPTH_TEST);

    // iniciar com a projeção paralela
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    glOrtho(-10, 10, -10, 10,  0.1,  100); // left, right, bottom, top, near, far
}


void Desenha(void)
{
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();

    // definir a posição e orientação da câmera
    gluLookAt(posX, posY,  -10,    // posição do centro da câmera
              0, 0,    0,    // direção para onde a camera está apontando
              0, 1,    0);   // vetor UP

    // limpar o buffer de cor e o buffer de profundidade
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT );

    // desenhar um cubo de arestas azuis
    glColor3f(1.0, 1.0, 0.0);
    glLineWidth(3);
    glutWireCube(5);
    
    glutSwapBuffers();
}

// Função callback chamada para gerenciar eventos de teclas
void Teclado (unsigned char key, int x, int y)
{
	  switch (key)
    {
      case 27:
		      exit(0);
      case ' ':
            flag_ortho = !flag_ortho;
            /********************************************************************************
             * geralmente, o tipo de projeção é estabelecido uma única vez antes do início do desenho da cena
             **********************************************************************************/
            glMatrixMode(GL_PROJECTION);
            glLoadIdentity();
            /*******************************************************************************
             Dois dos volumes de visualização possíveis de serem utilizados estão abaixo.
            Jamais use os dois ao mesmo tempo: isto causaria uma multiplicação dos
            dois volumes, produzindo um resultado inesperado.

            Nesta cena é desenhado as arestas de um cubo. Note a diferença entre os
            resultados obtidos através da utilização de cada volume.
            ********************************************************************************/

            if ( flag_ortho )
                glOrtho(-10, 10, -10, 10,  0.1,  100); // left, right, bottom, top, near, far
            else
                gluPerspective(90, 1, 0.1, 100); // fov, aspect ratio, near, far
            /********************************************************************************/
            break;
    }
    glutPostRedisplay();
}

// Função callback chamada para gerenciar eventos de teclas
void TeclasEspeciais (int key, int x, int y)
{
	  switch (key)
    {
      case GLUT_KEY_LEFT:
		      posX--;
          break;
      case GLUT_KEY_RIGHT:
		      posX++;
          break;
      case GLUT_KEY_UP:
		      posY++;
          break;
      case GLUT_KEY_DOWN:
		      posY--;
          break;
    }
    glutPostRedisplay();
}

int main(int argc, char** argv)
{
    // funções de inicialização da Janela
    glutInit(&argc, argv);
    IniciarJanela("Volume de Visualizacao");
        
    // função de desenho
    glutDisplayFunc(Desenha);
    glutKeyboardFunc(Teclado);
    glutSpecialFunc(TeclasEspeciais);

    glutMainLoop();
    return 0;
}



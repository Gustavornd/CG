
#include <GL/glut.h>

float rotacao_retangulo_1=0.0,
      rotacao_retangulo_2=0.0,
      rotacao_retangulo_3=0.0,
      rotacao_retangulo_4=0.0;

// definir algumas das cores a serem usadas no desenho
GLfloat RED[] = {1.0,0.0,0.0};
GLfloat LIGHT_GREEN[] = {0.5,1.0,0.5};
GLfloat DARK_GREEN[] = {0.0,0.5,0.0};
GLfloat BLUE[] = {0.0,0.0,1.0};
GLfloat YELLOW[] = {1.0,1.0,0.0};

/** DIMENSÕES DA WINDOW DE RECORTE */
#define ALTURA  50.0
#define LARGURA 50.0

/** DIMENSÕES DO RETANGULO */
#define COMPRIMENTO_RECT	10
#define LARGURA_RECT 	 	4
/*
  Função que desenha um Retângulo com a origem entre os vértices a e b, conforme a
ilustração abaixo:


  d ___________  c
   |           |
   *           |     <= O asterisco representa a origem do sistema. Definiremos
 a |___________| b       dessa forma para permitir um eixo de rotação mais realístico.
                         Daqui a pouco isto se tornará mais claro.

  Obs.: A origem, no programa renderizado, é representada por um pequeno ponto branco.
*/
void Retangulo(int comprimento,int largura)
{
    glBegin(GL_QUADS);
        glVertex2f(0, -largura/2);            //vertice a (ver figura)
        glVertex2f(comprimento, -largura/2);  //vertice b (ver figura)
        glVertex2f(comprimento, largura/2);   //vertice c (ver figura)
        glVertex2f(0, largura/2);             //vertice d (ver figura)
    glEnd();

    glColor3ub(255,255,255); // cor branca
    glPointSize(5);      // "dimensão" do ponto
    glBegin(GL_POINTS);
        glVertex2i(0,0);
    glEnd();
}

void Inicio(int argc,char **argv)
{
	glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH | GLUT_MULTISAMPLE);
    glutInitWindowSize(600, 600);
    glutInitWindowPosition(100, 100);
    glEnable(GLUT_MULTISAMPLE | GL_DEPTH_TEST ); // habilita a multiamostragem (redução de aliasing) e o teste de profundidade (remoção de superfícies ocultas)
    glutCreateWindow("Hierarquias");

    glClearColor(0.0,0.0,0.0,1.0); //Cor de fundo é preta
    glShadeModel( GL_SMOOTH ); // setando o método de coloração suave (interpolação)

    // Suavização de linhas
    glEnable(GL_LINE_SMOOTH);
    glHint(GL_LINE_SMOOTH_HINT, GL_NICEST);

    glMatrixMode(GL_PROJECTION);   //Carrega matriz de projeção
    glLoadIdentity();              //A matriz corrente é a identidade
    gluOrtho2D(0.0,LARGURA,0.0,ALTURA); //Visualização Ortogonal em z=0: xmin=0, xmax=LARGURA
										//                               ymin=0, ymax=ALTURA
}
void Desenha(void)
{
    // carrega a matriz de modelagem
    glMatrixMode(GL_MODELVIEW);
    // dar um reset nas matrizes de transformação
    glLoadIdentity();
    // limpar o buffer de cor e de profundidade
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT );

    // posicionar para desenhar o primeiro retangulo na metade da 
    // altura da janela de recorte no sistema de coordenadas do mundo
    // origem do sistema de coordenadas se torna o centro da altura da janela
    /*
     ___________________
    |                   |
    |                   |
    x                   |
    |                   |
    |___________________|
    */
    glTranslatef(0,ALTURA/2.0,0);
    glPushMatrix();  //Salvando estado atual de transformações (referencia r0)

//Desenhando o Retângulo 1
    glColor3fv(RED); // desenhar o primeiro retangulo na cor vermelha
    glRotatef(rotacao_retangulo_1, 0, 0, 1);
    Retangulo(COMPRIMENTO_RECT, LARGURA_RECT);
    glPushMatrix();  //Salvando estado atual de transformações (referencia r1)

//Desenhando o Retângulo 2
    glColor3fv(BLUE);
    glTranslatef(10, 0, 0);
    glRotatef(rotacao_retangulo_2, 0, 0, 1);
    Retangulo(COMPRIMENTO_RECT, LARGURA_RECT);
    glPushMatrix();  //Salvando estado atual de transformações (referencia r2)

//Desenhando o Retângulo 3
    glColor3fv(LIGHT_GREEN);
    glTranslatef(10, 0, 0);
    glRotatef(rotacao_retangulo_3+45, 0, 0, 1);
    Retangulo(COMPRIMENTO_RECT, LARGURA_RECT);
    glPopMatrix();  //Carregando estado de transformação do PushMatrix correspondente (r2)
    glPushMatrix();  //Salvando estado atual de transformações (referencia r2)

//Desenhando o Retângulo 4
    glColor3fv(DARK_GREEN);
    glTranslatef(10, 0, 0);
    glRotatef(rotacao_retangulo_4-45, 0, 0, 1);
    Retangulo(COMPRIMENTO_RECT, LARGURA_RECT);

//Voltar ao inicial...
    glPopMatrix(); //Carregando as matrizes de transformação do topo da pilha (r2)
    glPopMatrix(); //Carregando as matrizes de transformação do topo da pilha (r1)
    glPopMatrix(); //Carregando as matrizes de transformação do topo da pilha (r0)

// trocar os buffers
    glutSwapBuffers();
}



void Redimensiona(int w, int h)
{
    if (h==0) h=1;
    double ar = (double)w/h;
    glViewport(0,0,w,h);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    if (w>h) gluOrtho2D(0.0,LARGURA*ar, 0.0, ALTURA); // aumenta a largura conforme aspect ratio
    if (w<=h) gluOrtho2D(0.0,LARGURA, 0.0, ALTURA/ar); // aumenta a altura conforme aspect ratio
}



/*
  Função que administra interação do usuário com o teclado. As teclas são:
    q --> Rotaciona no sentido anti-horário o Retângulo 1
    a --> Rotaciona no sentido horário o Retângulo 1

    w --> Rotaciona no sentido anti-horário o Retângulo 2
    s --> Rotaciona no sentido horário o Retângulo 2

    e --> Rotaciona no sentido anti-horário o Retângulo 3
    d --> Rotaciona no sentido horário o Retângulo 3

    r --> Rotaciona no sentido anti-horário o Retângulo 4
    f --> Rotaciona no sentido horário o Retângulo 4
*/
void Teclado(unsigned char tecla_pressionada, int x, int y)
{
    switch(tecla_pressionada)
    {
    case 27:
        exit(0);
        break;

    case 'q':
    case 'Q':
        rotacao_retangulo_1 += 3.0;
        break;

    case 'a':
    case 'A':
        rotacao_retangulo_1 -= 3.0;
        break;

    case 'w':
    case 'W':
        rotacao_retangulo_2 += 3.0;
        break;

    case 's':
    case 'S':
        rotacao_retangulo_2 -= 3.0;
        break;

    case 'e':
    case 'E':
        rotacao_retangulo_3 += 3.0;
        break;

    case 'd':
    case 'D':
        rotacao_retangulo_3 -= 3.0;
        break;

    case 'r':
    case 'R':
        rotacao_retangulo_4 += 3.0;
        break;

    case 'f':
    case 'F':
        rotacao_retangulo_4 -= 3.0;
        break;
    case ' ': // espaço irá causar um reset
        rotacao_retangulo_1 = rotacao_retangulo_2 = rotacao_retangulo_3 = rotacao_retangulo_4 = 0;
        break;
    }
    glutPostRedisplay();
}


int main(int argc,char **argv)
{
    Inicio(argc, argv);
    glutDisplayFunc(Desenha);
    glutReshapeFunc(Redimensiona);
    glutKeyboardFunc(Teclado);
    glutMainLoop();
    return 0;
}

#include <GL/glut.h>
#include <iostream>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define PI  3.14159265358979323846

using namespace std;

double Largura = 700;
double Altura = 700;
int angle_grau = 0;

#define RAIO   50

double    posCamX = 0,
          posCamY = 0,
          posCamZ = RAIO,

          dirCamX = 0,
          dirCamY = 0,
          dirCamZ = 0,

          upCamX = 0,
          upCamY = 1,
          upCamZ = 0;

GLfloat RED[] = {1.0,0.0,0.0};
GLfloat GREEN[] = {0.0,1.0,0.0};
GLfloat BLUE[] = {0.0,0.0,1.0};
GLfloat YELLOW[] = {1.0,1.0,0.0};
GLint ANG_BRACO = 30;
GLint ANG_BRACO2 = 45;

void Init()
{
     glClearColor(0,0,0,1);
     glEnable(GLUT_MULTISAMPLE);

     // Habilitar o teste de profundidade
     glEnable(GL_DEPTH_TEST);
     glDepthFunc(GL_LESS);

     // Habilitar a remoção de faces ocultas
     glEnable(GL_CULL_FACE);
     glCullFace(GL_BACK); // Descartar as faces traseiras (padrão)
    
     glMatrixMode(GL_PROJECTION);
     glLoadIdentity();
     gluPerspective(45, Largura/Altura, 1, 100000);
}

void DesenhaRetangulo(GLint altura, GLint largura, GLfloat* cor)
{
    glPushMatrix();
    glColor3fv(cor);
    glScalef(largura, altura, 5);
    glutWireCube(1.0);
    glPopMatrix();
}

void DesenhaBraco()
{
    glColor3f(1,1,1);
    glutWireSphere(1,8,8);
    glRotatef(ANG_BRACO,0,0,1);
    glTranslatef(0,-6,0); // raio da esfera + metade do paralelepipedo
    DesenhaRetangulo(10,3,RED);
    glTranslatef(0,-6,0);
    glColor3f(1,1,1);
    glutWireSphere(1,8,8);
    glRotatef(ANG_BRACO2, 0,0,1);
    glTranslatef(0,-4.5,0);
    DesenhaRetangulo(7,3,BLUE);
    glTranslatef(0,-4.5,0);
    glColor3f(1,1,1);
    glutWireSphere(1,8,8);
    glTranslatef(0,-2,0);
    DesenhaRetangulo(2,2,RED);
}

void DesenhaTronco()
{
    glColor3fv(YELLOW);
    glScalef(10,15,5);
    glutWireCube(1.0);
}

void Display()
{
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

    gluLookAt(posCamX,posCamY, posCamZ,
              dirCamX, dirCamY, dirCamZ,
              upCamX, upCamY, upCamZ);


     //glutWireCube(10);
     glPushMatrix();
     DesenhaTronco();
     glPopMatrix();

     glPushMatrix();
     glTranslatef(5.5,7,0);
     glScalef(.5,.5,.5);
     DesenhaBraco();
     glPopMatrix(); // referência volta a ser a origem    
     





     char nome_janela[100];
     sprintf(nome_janela, "posCam[%.2f, %.2f, %.2f], Center[%.2f, %.2f, %.2f], UP[%.2f, %.2f, %.2f]", posCamX,
     posCamY, posCamZ, dirCamX, dirCamY, dirCamZ, upCamX, upCamY, upCamZ);

     glutSetWindowTitle( nome_janela );
     glutSwapBuffers();
     glFlush();
}

void Keyb(unsigned char key, int x, int y)
{
     switch( tolower(key) )
     {
             case 27:
                  exit(0);
             case 'a':
                  case 'A':
                       posCamY++;
                       break;
             case 'z':
                  case 'Z':
                       posCamY--;
                       break;
     }
     glutPostRedisplay();
}

void Keyb2(int key, int x, int y)
{
     switch( key)
     {
             case GLUT_KEY_LEFT: // deslocamento de 2 graus
                  angle_grau = (angle_grau-2)%360;
                  posCamX = RAIO*sin( angle_grau*PI/180.0);
                  posCamZ = RAIO*cos( angle_grau*PI/180.0);
                  break;
             case GLUT_KEY_RIGHT:
                  angle_grau = (angle_grau+2)%360;
                  posCamX = RAIO*sin( angle_grau*PI/180.0);
                  posCamZ = RAIO*cos( angle_grau*PI/180.0);
                  break;
             case GLUT_KEY_UP:
                  posCamZ++;
                  break;
             case GLUT_KEY_DOWN:
                  posCamZ--;
                  break;
             case GLUT_KEY_PAGE_UP:
                    ANG_BRACO2+=4;
                    break;
             case GLUT_KEY_PAGE_DOWN:
                    ANG_BRACO2-=4;
                    break;
     }
     glutPostRedisplay();
}

void RedimensionaJanela(GLsizei x, GLsizei y)
{
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();


    if ( y == 0 ) y=1;

    glViewport(0,0,x,y);
    
    gluPerspective(45, GLfloat(x)/y, 1, 100000);
    
    
}

int main(int argc, char** argv)
{
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGBA | GLUT_MULTISAMPLE );
    glutInitWindowSize(Largura, Altura);
    glutInitWindowPosition(50,50);
    glutCreateWindow("Teste Visualizacao");
    Init();
    glutDisplayFunc(Display);
    glutKeyboardFunc(Keyb);
    glutSpecialFunc(Keyb2);
    glutReshapeFunc(RedimensionaJanela);
    glutMainLoop();
    return 0;
}

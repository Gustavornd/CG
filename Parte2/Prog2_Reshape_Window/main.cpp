#include <GL/glut.h>

void changeSize(int w, int h) {

	// avoid division by zero
	if (h == 0)		
		h = 1;
	float aspect_ratio =  (float)w / h;

	glMatrixMode(GL_PROJECTION); // Change to Projection Matrix

	glLoadIdentity(); // Reset Matrix
	glViewport(0, 0, w, h); // Set the viewport to be the entire window
	gluPerspective(45, aspect_ratio, 1, 100); // Set the correct perspective. 
											  // width and height will be changed using the new aspect_ratio and fov parameters

}

void renderScene(void) 
{
	glMatrixMode(GL_MODELVIEW); // Change to Modelview matrix

	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

	glBegin(GL_TRIANGLES);
		glVertex3f(-2.0, -2.0, -5.0);
		glVertex3f( 2.0,  0.0, -5.0);
		glVertex3f( 0.0,  2.0, -5.0);
	glEnd();
	glutSwapBuffers();
}

void init(int argc, char **argv)
{
	glutInit(&argc, argv);
	glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGBA);
	glutInitWindowPosition(100,100);
	glutInitWindowSize(800,600);
	glutCreateWindow("Alterando o tamanho da viewport e mantendo a proporcao");
	glMatrixMode(GL_PROJECTION); // Change to Projection Matrix

	glLoadIdentity(); // Reset Matrix
	glViewport(0, 0, 800, 600); // Set the viewport to be the entire window
	gluPerspective(45, 800.0/600.0, 1, 100); // Set the correct perspective. 
											  // width and height will be changed using the new aspect_ratio and fov parameters
	
}

#include<iostream>

int main(int argc, char **argv) {

	// init GLUT and create window
	init(argc, argv);	

	// register callbacks
	glutDisplayFunc(renderScene);
	//glutReshapeFunc(changeSize);

	// enter GLUT event processing loop
	glutMainLoop();

	return 1;
}
##############################################################################
# Exemplo de makefile para um projeto C++ com OpenGL/freeglut
# Para simplificar, todos os arquivos estão em um mesmo diretório
##############################################################################
# Arquivo principal: main.cpp
##############################################################################


# definição de variáveis auxiliares do makefile
MAIN = programa_hierarquia
OBJECTS	= $(MAIN).o
FLAGS = -Wall -Wextra -std=c++20 -pedantic-errors
OPENGL_FLAG = -lopengl32 -lglu32 -lfreeglut
MATH = -lm
DEBUG = -g
CC = g++

# regra de compilação do projeto completo
all: main.exe

# regra para geração do arquivo executavel
main.exe: $(OBJECTS)
	$(CC) $(OBJECTS) $(FLAGS) $(OPENGL_FLAG)

# regra de compilação do objeto main.o
main.o: $(MAIN).cpp
	$(CC) -c $(MAIN).cpp -o $(MAIN).o 

# regra para limpeza do projeto (excluir arquivos .o e .exe). 
# (OBS.: SO windows)
clean:
	rm -rf $(OBJECTS)
	rm -rf *.exe

# regra para compilar todo o projeto (se necessário) e, posteriormente, executar
# (OBS.: SO windows)
run: all
	./$(MAIN).exe
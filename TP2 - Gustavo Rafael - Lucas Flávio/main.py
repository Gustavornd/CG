from hashlib import new
import sys
from PySide6.QtCore import QCoreApplication, QPointF, QRectF
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QGraphicsScene, QListWidgetItem, QListWidget
from PySide6.QtGui import QIcon, QPen, QPolygonF, QColor, QBrush
from tela import Ui_MainWindow
import numpy as np

from transformadas import translacao_y, translacao_x, rotacao, zoom, transformacao_translacao_objeto_y, transformacao_translacao_objeto_x, transformacao_rotacao_objeto, transformacao_zoom_objeto
from objects import Ponto, Reta, Poligono, Window, ViewPort
from xmlReader import ImportXML

WIDTH_PEN = 3
IND_MATRIZ = np.array([[1, 0, 0], [0,1,0], [0,0,1]])

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self) -> None:
        super(MainWindow, self).__init__()

        self.setupUi(self)
        self.setWindowTitle('TP2 - Gustavo Rafael - Lucas Flavio') # Configuração do título da janela
        appIcon = QIcon(u"") # Definição do ícone da aplicação
        self.setWindowIcon(appIcon)

        # Inicialização das variáveis principais do programa
        self.project = ImportXML()
        self.Window = Window([0,0], [10,10])
        self.Viewport = ViewPort([10,10], [630, 470])
        self.Objects = None
        self.current_object = None
        self.current_object_point = None
        self.PPC = IND_MATRIZ

        ####################################################
        # Configuração da tela
        self.setFixedSize(1256, 892)
        self.objectslist.setSortingEnabled(True)
        
        ####################################################
        # MENU ACTIONS
        # Open File Action
        self.btn_open.setStatusTip("Abrir arquivo xml.")
        self.btn_open.triggered.connect(self.openFile)
        # Save File Action
        self.btn_savefile.setStatusTip("Salvar objetos.")
        self.btn_savefile.triggered.connect(self.saveFile)
        ####################################################

        ####################################################
        # WINDOW ACTIONS
        self.escala_translacao.setText('1')
        # Translações
        self.btn_win_up.clicked.connect(lambda: self.moving_window('up') )
        self.btn_win_down.clicked.connect(lambda: self.moving_window('down') )
        self.btn_win_left.clicked.connect(lambda: self.moving_window('left') )
        self.btn_win_right.clicked.connect(lambda: self.moving_window('right') )
        # Rotações
        self.btn_rot_left.clicked.connect(lambda: self.moving_window('rot_left') )
        self.btn_rot_right.clicked.connect(lambda: self.moving_window('rot_right') )
        # Reset
        self.btn_reset_window.clicked.connect(self.reset_window)
        # Zoom
        self.btn_win_zoom_in.clicked.connect(lambda: self.zoom_window('in'))
        self.btn_win_zoom_out.clicked.connect(lambda: self.zoom_window('out'))
        ####################################################

        ####################################################
        # OBJECTS LIST ACTIONS
        # Selecionar objeto
        self.objectslist.itemPressed.connect(self.clickedObject)
        # Deletar objeto - Double click in object
        self.objectslist.itemDoubleClicked.connect(self.deleteObject)
        # Create Object
        self.create_new_object.clicked.connect(self.createObject)
        # Update Object
        self.update_new_object.clicked.connect(self.updateObject)
        # Deixar objecto
        self.btn_leave_obj.clicked.connect(self.deixarObjetoSelecionado)
        
        self.escala_translacao_obj.setText('1')

        # Translações
        self.btn_obj_up.clicked.connect(lambda: self.movingObject('up') )
        self.btn_obj_down.clicked.connect(lambda: self.movingObject('down') )
        self.btn_obj_left.clicked.connect(lambda: self.movingObject('left') )
        self.btn_obj_right.clicked.connect(lambda: self.movingObject('right') )
        # Rotações
        self.btn_obj_rot_left.clicked.connect(lambda: self.movingObject('rot_left') )
        self.btn_obj_rot_right.clicked.connect(lambda: self.movingObject('rot_right') )
        # Zoom
        self.btn_obj_zoom_in.clicked.connect(lambda: self.zoomObject('in'))
        self.btn_obj_zoom_out.clicked.connect(lambda: self.zoomObject('out'))
        
        ####################################################
        # OBJECT SELECTED ACTIONS
        # Seleciona ponto do objeto
        self.list_itens_object.itemPressed.connect(self.select_point_current_object)
        # Remove ponto do objeto
        self.list_itens_object.itemDoubleClicked.connect(self.removePointObject)
        # Adiciona ponto no objeto
        self.btn_add_point_object.clicked.connect(self.addPointObject)
        # Atualiza ponto do objeto
        self.btn_update_point_object.clicked.connect(self.updatePointObject)
        ####################################################

        self.render()

    
    def render(self):
        # Definindo valores mínimos e máximos das coordenadas do objeto
        self.coordx_select_point_object.setMinimum(self.Window.get_wmin()[0])
        self.coordy_select_point_object.setMinimum(self.Window.get_wmin()[1])
        self.coordx_select_point_object.setMaximum(self.Window.get_wmax()[0])
        self.coordy_select_point_object.setMaximum(self.Window.get_wmax()[1])

        self.view_objects = QGraphicsScene()
        self.view_objects.clear()
        self.display_viewport()
        self.show_objects()
        self.viewport.setScene(self.view_objects)
        

    def list_objects(self):
        # Limpa a lista de objetos e pontos, e reseta as seleções
        self.objectslist.clear()
        self.list_itens_object.clear()
        self.current_object = None
        self.current_object_point = None

        # Adiciona objetos à lista se existirem
        if self.Objects is not None:
            for obj_i in self.Objects:
                obj = QListWidgetItem()
                obj.setText(str(obj_i))
                obj.setData(1, obj_i)
                self.objectslist.addItem(obj)
        

    # Evento quando um objeto é clicado na lista
    def clickedObject(self, item):
        self.list_itens_object.clear()
        self.current_object = item
        print("Objeto Clicado: ", item.data(1))
        self.listPointsCurrentObject(item)
    
   
    # Remove um objeto da lista quando clicado duas vezes
    def deleteObject(self, item):
        row = self.objectslist.row(item)
        item = self.objectslist.takeItem(row)
        print("Remove object: ", item.data(1))
        self.list_itens_object.clear()
        self.current_object = None
        self.current_object_point = None
        self.current_object_row.setText("")
        self.render()

   
    # Lista os pontos do objeto selecionado
    def listPointsCurrentObject(self, item):
        objeto = item.data(1)

        row = self.objectslist.row(item)
        self.current_object_row.setText("Obj " + str(row))

        for p_i in objeto.get_points():
            obj = QListWidgetItem()
            obj.setText(str(p_i))
            obj.setData(1, p_i)
            self.list_itens_object.addItem(obj)


    # Seleciona um ponto específico do objeto para edição
    def select_point_current_object(self, item):
        self.current_object_point = item
        ponto = item.data(1)
        self.coordx_select_point_object.setValue(ponto.get_x())
        self.coordy_select_point_object.setValue(ponto.get_y())
    

    # Atualiza o objeto selecionado
    def updateObject(self):
        if self.current_object is not None:
            row = self.objectslist.row(self.current_object)
            item = self.objectslist.takeItem(row)
            self.current_object = None
            self.createObject()


    # Cria um novo objeto baseado nos pontos adicionados
    def createObject(self):
        if self.current_object is None:
            num_points = self.list_itens_object.count()
            obj = None

            if num_points == 1:
                # O objeto é um ponto
                obj = self.list_itens_object.takeItem(0)
                print("Adicionando novo ponto.")
            elif num_points == 2:
                # O objeto é uma reta
                reta = Reta()
                for ponto_i in range(2):
                    obj_list = self.list_itens_object.item(ponto_i)
                    ponto = obj_list.data(1)
                    reta.add_point(ponto)
                obj = QListWidgetItem()
                obj.setText(str(reta))
                obj.setData(1, reta)
                print("Adicionando nova reta.")
            elif num_points > 2:
                # O objeto é um poligono
                poli = Poligono()
                for ponto_i in range(self.list_itens_object.count()):
                    obj_list = self.list_itens_object.item(ponto_i)
                    ponto = obj_list.data(1)
                    poli.add_point(ponto)
                obj = QListWidgetItem()
                obj.setText(str(poli))
                obj.setData(1, poli)
                print("Adicionando novo poligono.")

            # Adiciona o objeto criado à lista de objetos
            self.objectslist.addItem(obj)
            self.current_object_row.setText("")
            self.list_itens_object.clear()
            self.deixarPontoObjetoSelecionado()
            self.render()

    # Movimenta o objeto de acordo com a ação recebida           
    def movingObject(self, tr):
        if self.current_object is not None:
            print("Movendo objeto...")
            escala = 0

            if tr in ['up', 'left', 'right', 'down']:
                escala = float(self.escala_translacao_obj.text())

            new_obj = None

            match tr:
                case 'up' | 'down':
                    if tr == 'up':
                        print(f'Move {escala} pixels do objeto para cima')
                        new_obj = transformacao_translacao_objeto_y(self.current_object.data(1), escala)
                    else:
                        print(f'Move {escala} pixels do objeto para baixo')
                        new_obj = transformacao_translacao_objeto_y(self.current_object.data(1), -escala)

                case 'left' | 'right':
                    if tr == 'left':
                        print(f'Move {escala} pixels do objeto para esquerda')
                        new_obj = transformacao_translacao_objeto_x(self.current_object.data(1), -escala)
                    else:
                        print(f'Move {escala} pixels do objeto para direita')
                        new_obj = transformacao_translacao_objeto_x(self.current_object.data(1), escala)

                case 'rot_right' | 'rot_left':
                    print('Rotacao do objeto 10º')
                    new_obj = transformacao_rotacao_objeto(self.current_object.data(1), tr)
            
            if new_obj is not None:
                self.deleteObject(self.current_object)
                obj = QListWidgetItem()
                obj.setText(str(new_obj))
                obj.setData(1, new_obj)
                self.objectslist.addItem(obj)
                self.clickedObject(obj)

            self.render()
        

    # Realiza zoom na window de acordo com a ação recebida
    def zoomObject(self, tipo):
        if self.current_object is not None:
            print("Zoom ", tipo)
            new_obj = None

            if tipo == 'in':
                new_obj = transformacao_zoom_objeto(self.current_object.data(1), tipo, self.Window)
            else:
                new_obj = transformacao_zoom_objeto(self.current_object.data(1), tipo, self.Window)

            if new_obj is not None:
                self.deleteObject(self.current_object)
                obj = QListWidgetItem()
                obj.setText(str(new_obj))
                obj.setData(1, new_obj)
                self.objectslist.addItem(obj)
                self.clickedObject(obj)
            self.render()


    # Adiciona um ponto ao objeto em criação
    def addPointObject(self):
        if self.current_object is not None:
            print("Adicionando ponto ao objeto existente!")
            if str(type(self.current_object.data(1))) != "<class 'objects.Poligono'>":
                return
        
        x = self.coordx_select_point_object.value()
        y = self.coordy_select_point_object.value()
        ponto = Ponto(x, y)
        obj = QListWidgetItem()
        obj.setText(str(ponto))
        obj.setData(1, ponto)
        print(f"Novo ponto: {obj.data(1)}")
        self.list_itens_object.addItem(obj)
        self.deixarPontoObjetoSelecionado()


    # Atualiza as coordenadas de um ponto selecionado no objeto
    def updatePointObject(self):
        if self.current_object_point is not None:
            row = self.list_itens_object.row(self.current_object_point)
            item = self.list_itens_object.takeItem(row)
            x = self.coordx_select_point_object.value()
            y = self.coordy_select_point_object.value()
            ponto = Ponto(x, y)
            obj = QListWidgetItem()
            obj.setText(str(ponto))
            obj.setData(1, ponto)
            print("Update do ponto: ", obj.data(1))
            self.list_itens_object.addItem(obj)
            self.deixarPontoObjetoSelecionado()

    
    # Remove um ponto do objeto em criação
    def removePointObject(self, item):
        if self.current_object is not None:
            if str(type(self.current_object.data(1))) != "<class 'objects.Poligono'>":
                print("Operação não possível para retas e pontos!")
                return

        if self.current_object is None:
            print("Remove point object: ", item.data(1))
            row = self.list_itens_object.row(item)
            item = self.list_itens_object.takeItem(row)
            return

        if self.list_itens_object.count()-1 >= 3:
            print("Remove point object: ", item.data(1))
            row = self.list_itens_object.row(item)
            item = self.list_itens_object.takeItem(row)
            self.current_object_point = None
        else:
            print("Remover este ponto fará deixar de ser polígono!")
        self.deixarPontoObjetoSelecionado()
        
    # Deixa o ponto selecionado dentro do objeto e não permite mais edições
    def deixarPontoObjetoSelecionado(self):
        self.current_object_point = None
        self.coordx_select_point_object.setValue(0.0)
        self.coordy_select_point_object.setValue(0.0)

    # Deixa o objeto selecionado na lista e não permite mais edições
    def deixarObjetoSelecionado(self):
        self.current_object = None
        self.deixarPontoObjetoSelecionado()
        self.current_object_row.setText("")
        self.list_itens_object.clear()


    # Movimenta a window de acordo com a ação recebida
    def moving_window(self, tr):
        escala = 0

        if tr in ['up', 'left', 'right', 'down']:
            escala = float(self.escala_translacao.text())
        print("-"*100)
        match tr:
            case 'up':
                print(f'Move {escala} pixels da window para cima')
                self.PPC = translacao_y(escala, self.PPC)
            case 'down':
                print(f'Move {escala} pixels da window para baixo')
                self.PPC = translacao_y(-escala, self.PPC)
            case 'left':
                print(f'Move {escala} pixels da window para esquerda')
                self.PPC = translacao_x(-escala, self.PPC)
            case 'right':
                print(f'Move {escala} pixels da window para direita')
                self.PPC = translacao_x(escala, self.PPC)
            case 'rot_right':
                print('Rotacao da window 10º para direita')
                self.PPC = rotacao(self.PPC, 'right', self.Window)
            case 'rot_left':
                print('Rotacao da window 10º para esquerda')
                self.PPC = rotacao(self.PPC, 'left', self.Window)

        print(self.PPC)
        self.render()


    # Reseta a window para os valores iniciais
    def reset_window(self):
        self.PPC = np.array([[1, 0, 0], [0,1,0], [0,0,1]])
        self.render()


    def zoom_window(self, type):
        print("-"*100)
        print(f"Aplicando Zoom {type} na window.")
        self.PPC = zoom(self.PPC, type, self.Window)
        self.render()


    def apply_PPC(self, p):
        return np.dot(self.PPC, p)


    # Exibe a viewport na cena
    def display_viewport(self):
        vpmax = None
        vpmin = None
        wmin = None
        wmax = None
        
        if self.Viewport is None:
            vpmin = [0, 0]
            vpmax = [640, 480]
        else:
            vpmax = self.Viewport.get_vpmax()
            vpmin = self.Viewport.get_vpmin()
        
        w, h = self.dimensao_viewport()
        print("Área da ViewPort: ", 0, 0, w, h)

        # Adicionando limite da viewport
        janelavp = QRectF()
        janelavp.setRect(0, 0, w, h)

        self.view_objects.addRect(janelavp)
        self.view_objects.update(janelavp)
        
    
    def dimensao_viewport(self):
        if self.Viewport is not None:
            vpmin = self.Viewport.get_vpmin()
            vpmax = self.Viewport.get_vpmax()
            w = (vpmin[0] + vpmax[0]) - 2*vpmin[0]
            h = (vpmin[1] + vpmax[1]) - 2*vpmin[0]
            return w, h
        return 620, 460            


    # Exibe os objetos na viewport
    def show_objects(self):
        if self.Window is not None:
            wmin = self.Window.get_wmin()
            wmax = self.Window.get_wmax()

            vpmin = self.Viewport.get_vpmin()
            vpmax = self.Viewport.get_vpmax()
            print(f"Exibindo {self.objectslist.count()} objetos...")
            
            for row_item in range(self.objectslist.count()):
                
                obj_list = self.objectslist.item(row_item)
                obj = obj_list.data(1)
                str_type = str(type(obj))

                if str_type == "<class 'objects.Ponto'>": 
                    obj = self.display_ponto(obj, wmin, wmax, vpmin, vpmax)
                elif str_type == "<class 'objects.Reta'>": 
                    obj = self.display_reta(obj, wmin, wmax, vpmin, vpmax)
                elif str_type == "<class 'objects.Poligono'>": 
                    obj = self.display_poligono(obj, wmin, wmax, vpmin, vpmax)
                
            
    # Função para exibição de um Ponto
    def display_ponto(self, obj, wmin, wmax, vpmin, vpmax):
        xw = obj.get_x()
        yw = obj.get_y()
        p = [xw, yw, 1]
        coords = self.apply_PPC(p)


        xvp = self.convert_x_to_xvp(coords[0], wmin, wmax, vpmin, vpmax)
        yvp = self.convert_y_to_yvp(coords[1], wmin, wmax, vpmin, vpmax)

        print(f"Ponto: {coords}.")

        green_pen = QPen()
        green_pen.setColor(QColor(0, 0, 255))
        green_pen.setWidth(WIDTH_PEN + 2)
        green_brush = QBrush()
        green_brush.setColor(QColor(0, 0, 255))

        self.view_objects.addEllipse(xvp, yvp, 1, 1, green_pen, green_brush)
        return obj
    
    
    # Função para exibição de uma Reta
    def display_reta(self, obj, wmin, wmax, vpmin, vpmax):
        points = obj.get_list_points()

        p1 = [points[0][0], points[0][1], 1]
        coords_p1 = self.apply_PPC(p1)
        p2 = [points[1][0], points[1][1], 1]
        coords_p2 = self.apply_PPC(p2)

        xvp1 = self.convert_x_to_xvp(coords_p1[0], wmin, wmax, vpmin, vpmax)
        yvp1 = self.convert_y_to_yvp(coords_p1[1], wmin, wmax, vpmin, vpmax)
        
        xvp2 = self.convert_x_to_xvp(coords_p2[0], wmin, wmax, vpmin, vpmax)
        yvp2 = self.convert_y_to_yvp(coords_p2[1], wmin, wmax, vpmin, vpmax)

        print(f"Reta: {coords_p1} - {coords_p2}.")

        red_pen = QPen()
        red_pen.setColor(QColor(255, 0, 0))
        red_pen.setWidth(WIDTH_PEN)

        self.view_objects.addLine(xvp1, yvp1, xvp2, yvp2, red_pen)
        return obj
    
    
    # Função para exibição de um Poligono
    def display_poligono(self, obj, wmin, wmax, vpmin, vpmax):
        points = obj.get_list_points()
        poligono = QPolygonF()

        blue_pen = QPen()
        blue_pen.setColor(QColor(0, 0, 255))
        blue_pen.setWidth(WIDTH_PEN)

        print("Poligono: [", end="")
        pontos = []

        for p in points:
            ponto = QPointF()
            coords_p = [p[0], p[1], 1]
            coords_p = self.apply_PPC(coords_p)
            xvp = self.convert_x_to_xvp(coords_p[0], wmin, wmax, vpmin, vpmax)
            yvp = self.convert_y_to_yvp(coords_p[1], wmin, wmax, vpmin, vpmax)
            ponto.setX(xvp)
            ponto.setY(yvp)


            print(f"{coords_p} ", end="")
            poligono.append(ponto)
        
        print("]")

        
        self.view_objects.addPolygon(poligono, blue_pen)
        return obj

    
    def convert_x_to_xvp(self, XW, wmin, wmax, vpmin, vpmax):
        return ( (XW - wmin[0])/(wmax[0] - wmin[0]) ) * ( vpmax[0] - vpmin[0] )


    def convert_y_to_yvp(self, YW, wmin, wmax, vpmin, vpmax):
        return ( 1 - ((YW - wmin[1])/(wmax[1] - wmin[1])) ) * ( vpmax[1] - vpmin[1] )


    # Abre um arquivo XML e carrega os objetos
    def openFile(self):
        print("Open XML File... ", end="")
        file_path = QFileDialog().getOpenFileName(parent=self, caption='Open XML File', filter='*.xml')
        if len(file_path[0]) > 0:
            self.project = ImportXML()
            self.project.open_xml(file_path[0])
            self.project.read_objects()
            self.Objects = self.project.get_objects()
            self.Window = self.project.get_window()
            self.Viewport = self.project.get_viewport()
            self.PPC = IND_MATRIZ
            self.list_objects()
            print("OK!")
            self.render()
        else:
            print("Erro!")


    # Salva os objetos no formato XML
    def saveFile(self):
        file_path = QFileDialog().getSaveFileName(parent=self, caption='Salvar Arquivo')
        print("Salvando coordenadas...", end="")

        file_xml = "<?xml version=\"1.0\" ?> \n<dados>\n"
        file_xml += self.Viewport.get_xml()
        file_xml += self.Window.get_xml()

        for obj_i in range(self.objectslist.count()):
            obj = self.objectslist.item(obj_i)
            file_xml += obj.data(1).get_xml()
        file_xml += "</dados>\n"

        if len(file_path[0]) > 0:
            file = open(file_path[0], "w")
            file.write(file_xml)
            file.close()
            print("OK!")
        else:
            print("Erro!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

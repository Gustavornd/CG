import xml.etree.ElementTree as AT
import PyQt5 # type: ignore
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsLineItem, QGraphicsPolygonItem, QGraphicsEllipseItem # type: ignore
from PyQt5.QtCore import Qt, QPointF # type: ignore
from PyQt5.QtGui import QPolygonF # type: ignore
from PyQt5 import QtGui # type: ignore


class Window:
    def __init__(self, xwmin, ywmin, xwmax, ywmax):
        self.xwmin = xwmin
        self.ywmin = ywmin
        self.xwmax = xwmax
        self.ywmax = ywmax


class Ponto2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Reta2D:
    def __init__(self, ponto1, ponto2):
        self.ponto1 = ponto1
        self.ponto2 = ponto2


class Poligono2D:
    def __init__(self, pontos):
        self.pontos = pontos



class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.window = None
        self.objetos_transformados = []
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.setCentralWidget(self.view)
        self.read_xml()
        self.transform_objects()
        self.display_objects()

    def read_xml(self):
        # Leitura do arquivo XML
        tree = AT.parse('entrada.xml')
        root = tree.getroot()

        # Leitura dos dados da viewport
        viewport_data = root.find('viewport')
        vpmin = viewport_data.find('vpmin')
        vpmax = viewport_data.find('vpmax')

        vpmin_x = float(vpmin.attrib['x'])
        vpmin_y = float(vpmin.attrib['y'])
        vpmax_x = float(vpmax.attrib['x'])
        vpmax_y = float(vpmax.attrib['y'])

        # Leitura dos dados da window
        window_data = root.find('window')
        wmin = window_data.find('wmin')
        wmax = window_data.find('wmax')

        wmin_x = float(wmin.attrib['x'])
        wmin_y = float(wmin.attrib['y'])
        wmax_x = float(wmax.attrib['x'])
        wmax_y = float(wmax.attrib['y'])

        self.window = Window(wmin_x, wmin_y, wmax_x, wmax_y)
        self.vpmin_x, self.vpmin_y, self.vpmax_x, self.vpmax_y = vpmin_x, vpmin_y, vpmax_x, vpmax_y

        # Armazena os objetos lidos no XML
        self.objetos_transformados = []
        for child in root:
            if child.tag == 'ponto':
                x = float(child.attrib['x'])
                y = float(child.attrib['y'])
                self.objetos_transformados.append(Ponto2D(x, y))
            elif child.tag == 'reta':
                ponto1 = child.find('ponto[1]')
                ponto2 = child.find('ponto[2]')
                x1 = float(ponto1.attrib['x'])
                y1 = float(ponto1.attrib['y'])
                x2 = float(ponto2.attrib['x'])
                y2 = float(ponto2.attrib['y'])
                self.objetos_transformados.append(Reta2D(Ponto2D(x1, y1), Ponto2D(x2, y2)))
            elif child.tag == 'poligono':
                pontos = []
                for ponto in child.findall('ponto'):
                    x = float(ponto.attrib['x'])
                    y = float(ponto.attrib['y'])
                    pontos.append(Ponto2D(x, y))
                self.objetos_transformados.append(Poligono2D(pontos))

    def transform_objects(self):
        # Dimensões da window e viewport
        w_width = self.window.xwmax - self.window.xwmin
        w_height = self.window.ywmax - self.window.ywmin
        vp_width = self.vpmax_x - self.vpmin_x
        vp_height = self.vpmax_y - self.vpmin_y

        # Limpar a lista de objetos transformados
        transformed_objects = []

        for obj in self.objetos_transformados:
            if isinstance(obj, Ponto2D):
                x_vp = ((obj.x - self.window.xwmin) / w_width) * vp_width + self.vpmin_x
                y_vp = ((self.window.ywmax - obj.y) / w_height) * vp_height + self.vpmin_y
                transformed_objects.append(Ponto2D(x_vp, y_vp))
            elif isinstance(obj, Reta2D):
                x1_vp = ((obj.ponto1.x - self.window.xwmin) / w_width) * vp_width + self.vpmin_x
                y1_vp = ((self.window.ywmax - obj.ponto1.y) / w_height) * vp_height + self.vpmin_y
                x2_vp = ((obj.ponto2.x - self.window.xwmin) / w_width) * vp_width + self.vpmin_x
                y2_vp = ((self.window.ywmax - obj.ponto2.y) / w_height) * vp_height + self.vpmin_y
                transformed_objects.append(Reta2D(Ponto2D(x1_vp, y1_vp), Ponto2D(x2_vp, y2_vp)))
            elif isinstance(obj, Poligono2D):
                pontos_vp = []
                for ponto in obj.pontos:
                    x_vp = ((ponto.x - self.window.xwmin) / w_width) * vp_width + self.vpmin_x
                    y_vp = ((self.window.ywmax - ponto.y) / w_height) * vp_height + self.vpmin_y
                    pontos_vp.append(Ponto2D(x_vp, y_vp))
                transformed_objects.append(Poligono2D(pontos_vp))

        # Atualiza a lista de objetos transformados
        self.objetos_transformados = transformed_objects

    def display_objects(self):
        # Limpa a cena antes de desenhar
        self.scene.clear()

        for obj in self.objetos_transformados:
            if isinstance(obj, Ponto2D):
                item = QGraphicsEllipseItem(obj.x - 2, obj.y - 2, 4, 4)
                item.setBrush(Qt.black)
                self.scene.addItem(item)
            elif isinstance(obj, Reta2D):
                item = QGraphicsLineItem(obj.ponto1.x, obj.ponto1.y, obj.ponto2.x, obj.ponto2.y)
                self.scene.addItem(item)
            elif isinstance(obj, Poligono2D):
                pontos = [QPointF(ponto.x, ponto.y) for ponto in obj.pontos]
                poligono = QGraphicsPolygonItem()
                poligono.setPolygon(QPolygonF(pontos))
                self.scene.addItem(poligono)

    def generate_output_file(self, filename):
        root_output = AT.Element('saida')

        for obj in self.objetos_transformados:
            if isinstance(obj, Ponto2D):
                ponto = AT.SubElement(root_output, 'ponto')
                ponto.attrib['x'] = str(obj.x)
                ponto.attrib['y'] = str(obj.y)
            elif isinstance(obj, Reta2D):
                reta = AT.SubElement(root_output, 'reta')
                ponto1 = AT.SubElement(reta, 'ponto')
                ponto1.attrib['x'] = str(obj.ponto1.x)
                ponto1.attrib['y'] = str(obj.ponto1.y)
                ponto2 = AT.SubElement(reta, 'ponto')
                ponto2.attrib['x'] = str(obj.ponto2.x)
                ponto2.attrib['y'] = str(obj.ponto2.y)
            elif isinstance(obj, Poligono2D):
                poligono = AT.SubElement(root_output, 'poligono')
                for ponto in obj.pontos:
                    ponto_xml = AT.SubElement(poligono, 'ponto')
                    ponto_xml.attrib['x'] = str(ponto.x)
                    ponto_xml.attrib['y'] = str(ponto.y)

        tree_output = AT.ElementTree(root_output)
        tree_output.write(filename)


if __name__ == '__main__':
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec_()

import xml.etree.ElementTree as ET
import PyQt5  # type: ignore
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsLineItem,
    QGraphicsPolygonItem,
    QGraphicsEllipseItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
    QInputDialog,
    QDialog,
    QFormLayout,
    QLineEdit,
    QDialogButtonBox,
)  # type: ignore
from PyQt5.QtCore import Qt, QPointF  # type: ignore
from PyQt5.QtGui import QPolygonF  # type: ignore


class Window:
    def __init__(self, xwmin, ywmin, xwmax, ywmax):
        self.xwmin = xwmin
        self.ywmin = ywmin
        self.xwmax = xwmax
        self.ywmax = ywmax

    def move(self, dx, dy):
        self.xwmin += dx
        self.xwmax += dx
        self.ywmin += dy
        self.ywmax += dy

    def scale(self, factor):
        center_x = (self.xwmin + self.xwmax) / 2
        center_y = (self.ywmin + self.ywmax) / 2
        half_width = (self.xwmax - self.xwmin) * factor / 2
        half_height = (self.ywmax - self.ywmin) * factor / 2
        self.xwmin = center_x - half_width
        self.xwmax = center_x + half_width
        self.ywmin = center_y - half_height
        self.ywmax = center_y + half_height

    def rotate(self, angle):
        from math import radians, cos, sin

        angle = radians(angle)
        center_x = (self.xwmin + self.xwmax) / 2
        center_y = (self.ywmin + self.ywmax) / 2

        def rotate_point(x, y):
            x_new = cos(angle) * (x - center_x) - sin(angle) * (y - center_y) + center_x
            y_new = sin(angle) * (x - center_x) + cos(angle) * (y - center_y) + center_y
            return x_new, y_new

        corners = [
            (self.xwmin, self.ywmin),
            (self.xwmax, self.ywmin),
            (self.xwmax, self.ywmax),
            (self.xwmin, self.ywmax),
        ]
        rotated_corners = [rotate_point(x, y) for x, y in corners]
        x_values = [x for x, y in rotated_corners]
        y_values = [y for x, y in rotated_corners]
        self.xwmin, self.xwmax = min(x_values), max(x_values)
        self.ywmin, self.ywmax = min(y_values), max(y_values)


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

        self.setup_ui()
        self.read_xml()
        self.transform_objects()
        self.display_objects()

    def setup_ui(self):
        main_layout = QHBoxLayout()

        control_layout = QVBoxLayout()

        self.add_point_button = QPushButton("Add Point")
        self.add_line_button = QPushButton("Add Line")
        self.add_polygon_button = QPushButton("Add Polygon")
        self.move_up_button = QPushButton("Move Up")
        self.move_down_button = QPushButton("Move Down")
        self.move_left_button = QPushButton("Move Left")
        self.move_right_button = QPushButton("Move Right")
        self.zoom_in_button = QPushButton("Zoom In")
        self.zoom_out_button = QPushButton("Zoom Out")
        self.rotate_left_button = QPushButton("Rotate Left")
        self.rotate_right_button = QPushButton("Rotate Right")

        self.add_point_button.clicked.connect(self.add_point)
        self.add_line_button.clicked.connect(self.add_line)
        self.add_polygon_button.clicked.connect(self.add_polygon)
        self.move_up_button.clicked.connect(lambda: self.move_window(0, -0.5))
        self.move_down_button.clicked.connect(lambda: self.move_window(0, 0.5))
        self.move_left_button.clicked.connect(lambda: self.move_window(-0.5, 0))
        self.move_right_button.clicked.connect(lambda: self.move_window(0.5, 0))
        self.zoom_in_button.clicked.connect(lambda: self.zoom_window(0.9))
        self.zoom_out_button.clicked.connect(lambda: self.zoom_window(1.1))
        self.rotate_left_button.clicked.connect(lambda: self.rotate_window(-10))
        self.rotate_right_button.clicked.connect(lambda: self.rotate_window(10))

        control_layout.addWidget(self.add_point_button)
        control_layout.addWidget(self.add_line_button)
        control_layout.addWidget(self.add_polygon_button)
        control_layout.addWidget(self.move_up_button)
        control_layout.addWidget(self.move_down_button)
        control_layout.addWidget(self.move_left_button)
        control_layout.addWidget(self.move_right_button)
        control_layout.addWidget(self.zoom_in_button)
        control_layout.addWidget(self.zoom_out_button)
        control_layout.addWidget(self.rotate_left_button)
        control_layout.addWidget(self.rotate_right_button)

        controls = QWidget()
        controls.setLayout(control_layout)

        main_layout.addWidget(controls)
        main_layout.addWidget(self.view)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def read_xml(self):
        # Leitura do arquivo XML
        tree = ET.parse('entrada.xml')
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

    def add_point(self):
        x, ok_x = QInputDialog.getDouble(self, "Input X Coordinate", "X:", 0, -1000, 1000, 2)
        y, ok_y = QInputDialog.getDouble(self, "Input Y Coordinate", "Y:", 0, -1000, 1000, 2)
        if ok_x and ok_y:
            new_point = Ponto2D(x, y)
            self.objetos_transformados.append(new_point)
            self.transform_objects()
            self.display_objects()

    def add_line(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Line")

        layout = QFormLayout(dialog)
        x1_input = QLineEdit(dialog)
        y1_input = QLineEdit(dialog)
        x2_input = QLineEdit(dialog)
        y2_input = QLineEdit(dialog)

        layout.addRow("X1:", x1_input)
        layout.addRow("Y1:", y1_input)
        layout.addRow("X2:", x2_input)
        layout.addRow("Y2:", y2_input)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)

        if dialog.exec_() == QDialog.Accepted:
            x1 = float(x1_input.text())
            y1 = float(y1_input.text())
            x2 = float(x2_input.text())
            y2 = float(y2_input.text())
            new_line = Reta2D(Ponto2D(x1, y1), Ponto2D(x2, y2))
            self.objetos_transformados.append(new_line)
            self.transform_objects()
            self.display_objects()

    def add_polygon(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Polygon")

        layout = QFormLayout(dialog)
        vertices_input = QLineEdit(dialog)

        layout.addRow("Vertices (format: x1,y1 x2,y2 x3,y3 ...):", vertices_input)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)

        if dialog.exec_() == QDialog.Accepted:
            vertices_str = vertices_input.text().split()
            vertices = []
            for vertex_str in vertices_str:
                x, y = map(float, vertex_str.split(','))
                vertices.append(Ponto2D(x, y))
            new_polygon = Poligono2D(vertices)
            self.objetos_transformados.append(new_polygon)
            self.transform_objects()
            self.display_objects()

    def move_window(self, dx, dy):
        self.window.move(dx, dy)
        self.transform_objects()
        self.display_objects()

    def zoom_window(self, factor):
        self.window.scale(factor)
        self.transform_objects()
        self.display_objects()

    def rotate_window(self, angle):
        self.window.rotate(angle)
        self.transform_objects()
        self.display_objects()

    def generate_output_file(self, filename):
        root_output = ET.Element("saida")

        for obj in self.objetos_transformados:
            if isinstance(obj, Ponto2D):
                ponto = ET.SubElement(root_output, "ponto")
                ponto.attrib["x"] = str(obj.x)
                ponto.attrib["y"] = str(obj.y)
            elif isinstance(obj, Reta2D):
                reta = ET.SubElement(root_output, "reta")
                ponto1 = ET.SubElement(reta, "ponto")
                ponto1.attrib["x"] = str(obj.ponto1.x)
                ponto1.attrib["y"] = str(obj.ponto1.y)
                ponto2 = ET.SubElement(reta, "ponto")
                ponto2.attrib["x"] = str(obj.ponto2.x)
                ponto2.attrib["y"] = str(obj.ponto2.y)
            elif isinstance(obj, Poligono2D):
                poligono = ET.SubElement(root_output, "poligono")
                for ponto in obj.pontos:
                    ponto_xml = ET.SubElement(poligono, "ponto")
                    ponto_xml.attrib["x"] = str(ponto.x)
                    ponto_xml.attrib["y"] = str(ponto.y)

        tree_output = ET.ElementTree(root_output)
        tree_output.write(filename)


if __name__ == "__main__":
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec_()

import numpy as np

# Classe base
class Object():
    
    def __init__(self) -> None:
        pass

# Classe que define um ponto
class Ponto(Object):
    
    def __init__(self, x=0, y=0) -> None:
        super().__init__()
        self.x = x
        self.y = y
    
    def get_points(self):
        return [self]
    
    def get_x(self):
        return self.x

    def get_y(self):
        return self.y
    
    def set_points(self, points):
        self.x = points[0].get_x()
        self.y = points[0].get_y()
    
    def get_centro(self):
        return [self.x, self.y]
    
    def get_xml(self):
        return "<ponto x=\""+str(self.x)+"\" y=\""+str(self.y)+"\"/>\n"
        
    def __repr__(self):
        return f'Ponto:({np.round(self.x, 2)}, {np.round(self.y,2)})'
    
# Classe que define uma Reta
class Reta(Object):
    
    def __init__(self) -> None:
        super().__init__()
        self.points = []
    
    def get_points(self):
        return self.points
    
    def add_point(self, point):
        self.points.append(point)

    def get_list_points(self):
        points_list = []

        for p in self.points:
            ponto = []
            ponto.append(p.get_x())
            ponto.append(p.get_y())
            points_list.append(ponto)

        return points_list
    
    def set_points(self, points):
        self.points = points
    
    def get_centro(self):
        pontos = self.get_list_points()
        x = y = c = 0
        for p in pontos:
            x += p[0]
            y += p[1]
            c += 1
        return [x/c, y/c]
    
    def get_xml(self):
        string_xml = "<reta>\n"
        for p in self.points:
            string_xml += p.get_xml()
        return string_xml + "</reta>\n\n"

    def __repr__(self):
        return f'Reta:[{self.points[0]}, {self.points[1]}]'
    
# Classe que define um poligono
class Poligono(Object):
    
    def __init__(self) -> None:
        super().__init__()
        self.points = []

    def get_points(self):
        return self.points

    def get_list_points(self):
        points_list = []

        for p in self.points:
            ponto = []
            ponto.append(p.get_x())
            ponto.append(p.get_y())
            points_list.append(ponto)

        return points_list
    
    def add_point(self, point):
        self.points.append(point)
    
    def set_points(self, points):
        self.points = points
    
    def get_centro(self):
        pontos = self.get_list_points()
        x = y = c = 0
        for p in pontos:
            x += p[0]
            y += p[1]
            c += 1
        return [x/c, y/c]
    
    def get_xml(self):
        string_xml = "<poligono>\n"
        for p in self.points:
            string_xml += p.get_xml()
        return string_xml + "</poligono>\n\n"

    def __repr__(self):
        return f'Poligono:{str(self.points)}'

#Classe que define uma Viewport
class ViewPort():

    def __init__(self, vpmin=[], vpmax=[]):
        self.vpmin = vpmin
        self.vpmax = vpmax
    
    def get_vpmin(self):
        return self.vpmin
    
    def get_vpmax(self):
        return self.vpmax
    
    # Função para formatar a representaçção da Viewport no arquivo de Saida XML
    def get_xml(self):
        string_xml = "<viewport>\n" + \
            "<vpmin x=\""+str(self.vpmin[0])+"\" y=\""+str(self.vpmin[1])+"\"/>\n" + \
                "<vpmax x=\""+str(self.vpmax[0])+"\" y=\""+str(self.vpmax[1])+"\"/>\n" + \
                    "</viewport>\n\n"
        return string_xml
        
    def __repr__(self):
        return f'VpMin = {self.vpmin} | VpMax = {self.vpmax}'
        

# Classe que define uma Window. 
class Window():

    def __init__(self, wmin=[], wmax=[]) -> None:
        self.wmin = wmin
        self.wmax = wmax
        self.before = [self.wmin, self.wmax]

    def get_wmin(self):
        return self.wmin

    def get_wmax(self):
        return self.wmax
    
    def set_wmin(self, wmin):
        self.wmin = wmin

    def set_wmax(self, wmax):
        self.wmax = wmax
    
    def __repr__(self):
        return f'WMin = {self.wmin} | WMax = {self.wmax}'
    
    def reset(self):
        self.wmin = self.before[0]
        self.wmax = self.before[1]
    
    def retorna_centro(self):
        x = ( self.wmin[0] + self.wmax[0] ) / 2
        y = ( self.wmin[1] + self.wmax[1] ) / 2
        return x, y
    
    # Função para formatar a representaçção da Window no arquivo de Saida XML
    def get_xml(self):
        string_xml = "<window>\n" + \
            "<wmin x=\""+str(self.wmin[0])+"\" y=\""+str(self.wmin[1])+"\"/>\n" + \
                "<wmax x=\""+str(self.wmax[0])+"\" y=\""+str(self.wmax[1])+"\"/>\n" + \
                    "</window>\n\n"
        return string_xml
    
    def get_centro(self):
        return self.retorna_centro()
from objects import Ponto, Reta, Poligono, Window, ViewPort


import xml.etree.ElementTree as ET
import os

class ImportXML():

    def __init__(self) -> None:
        self.url_file = None
        self.tree = None
        self.root = None
        self.objects = []
        self.window = None
        self.viewport = None


    def open_xml(self, url):
        try:
            self.url_file = url
            self.tree = ET.parse(url)
            self.root = self.tree.getroot()
        except:
             print('ERROR: This file path does not exist !!!')
             

    def read_objects(self):
        if self.root is not None:
            for obj in self.root:

                    if obj.tag == 'viewport':
                        vp = ViewPort()
                        vp.vpmin = [float(obj[0].get('x')), float(obj[0].get('y'))]
                        vp.vpmax = [float(obj[1].get('x')), float(obj[1].get('y'))]
                        self.viewport = vp

                    elif obj.tag == 'window':
                        win = Window()
                        win.wmin = [float(obj[0].get('x')), float(obj[0].get('y'))]
                        win.wmax = [float(obj[1].get('x')), float(obj[1].get('y'))]
                        self.window = win

                    elif obj.tag == 'ponto':
                        point = Ponto()
                        point.x = float(obj.get('x'))
                        point.y = float(obj.get('y'))
                        self.objects.append(point)

                    elif obj.tag == 'reta':
                        reta = Reta()
                        for obj_child in obj:
                            point = Ponto()
                            point.x = float(obj_child.get('x'))
                            point.y = float(obj_child.get('y'))
                            reta.add_point(point)
                        self.objects.append(reta)
                        
                    elif obj.tag == 'poligono':
                        poligono = Poligono()
                        for obj_child in obj:
                            point = Ponto()
                            point.x = float(obj_child.get('x'))
                            point.y = float(obj_child.get('y'))
                            poligono.add_point(point)
                        self.objects.append(poligono)

    def get_window(self):
        return self.window
    

    def get_viewport(self):
        return self.viewport

    
    def get_objects(self):
        return self.objects


    def get_num_objects(self):
        return len(self.objects)
        
    def __str__(self) -> str:
        return (f'Read {len(self.objects)} objects.')
    


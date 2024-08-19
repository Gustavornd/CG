import numpy as np
from objects import Ponto, Reta, Poligono, Window, ViewPort

def translacao_y(escala:float, m):
    M_TRANS_Y = np.array([[1, 0, 0], [0, 1, escala], [0, 0, 1]])
    return np.dot(m, M_TRANS_Y)


def translacao_x(escala:float, m):
    M_TRANS_X = np.array([[1, 0, escala], [0, 1, 0], [0, 0, 1]])
    return np.dot(m, M_TRANS_X)


def rotacao(m, dir, window):
    angle = -10 if dir == 'left' else 10
    centro = window.retorna_centro()
    leva_ao_centro = np.array([[1, 0, -centro[0]], [0, 1, -centro[1]], [0, 0, 1]])
    cos_theta = np.cos(np.radians(-angle))
    sin_theta = np.sin(np.radians(-angle))
    rotaciona = np.array([[cos_theta, -sin_theta, 0], [sin_theta, cos_theta, 0], [0,0,1]])
    volta_do_centro = np.array([[1, 0, centro[0]], [0, 1, centro[1]], [0, 0, 1]])
    TRANSFORMACAO = np.dot(volta_do_centro, np.dot(rotaciona, leva_ao_centro))
    return np.dot(m, TRANSFORMACAO)


def zoom(m, type, window):
    centro = window.get_centro()
    leva_ao_centro = np.array([[1, 0, -centro[0]], [0, 1, -centro[1]], [0, 0, 1]])
    volta_do_centro = np.array([[1, 0, centro[0]], [0, 1, centro[1]], [0, 0, 1]])
    escala = None
    e = 1.05
    if type == 'in':
        escala = np.array([[e, 0, 0 ], [0, e, 0], [0, 0, 1]])
    else:
        escala = np.array([[1/e, 0, 0 ], [0, 1/e, 0], [0, 0, 1]]) # Escala inversa
    TRANSFORMACAO = np.dot(volta_do_centro, np.dot(leva_ao_centro, escala))
    return np.dot(m, TRANSFORMACAO)


def transformacao_translacao_objeto_y(obj, escala):

    str_type = str(type(obj))

    if str_type == "<class 'objects.Ponto'>":
        ponto = np.array([obj.get_x(), obj.get_y(), 1])
        ponto_new = translacao_y_ponto(escala, ponto)
        return Ponto(ponto_new[0], ponto_new[1])

    elif str_type in [ "<class 'objects.Reta'>", "<class 'objects.Poligono'>" ]:
        pontos = obj.get_points()
        new_points = []
        for p in pontos:
            new_points.append(transformacao_translacao_objeto_y(p, escala))
        
        if str_type == "<class 'objects.Reta'>":
            r = Reta()
            r.set_points(new_points)
            return r
        
        p = Poligono()
        p.set_points(new_points)
        return p
    

def transformacao_translacao_objeto_x(obj, escala):

    str_type = str(type(obj))

    if str_type == "<class 'objects.Ponto'>":
        ponto = np.array([obj.get_x(), obj.get_y(), 1])
        ponto_new = translacao_x_ponto(escala, ponto)
        return Ponto(ponto_new[0], ponto_new[1])

    elif str_type in [ "<class 'objects.Reta'>", "<class 'objects.Poligono'>" ]:
        pontos = obj.get_points()
        new_points = []
        for p in pontos:
            new_points.append(transformacao_translacao_objeto_x(p, escala))
        
        if str_type == "<class 'objects.Reta'>":
            r = Reta()
            r.set_points(new_points)
            return r
        
        p = Poligono()
        p.set_points(new_points)
        return p


def transformacao_rotacao_objeto(obj, dir):
    str_type = str(type(obj))

    if str_type == "<class 'objects.Ponto'>":
        ponto = np.array([obj.get_x(), obj.get_y(), 1])
        return Ponto(ponto[0], ponto[1])

    elif str_type in [ "<class 'objects.Reta'>", "<class 'objects.Poligono'>" ]:
        pontos = obj.get_points()
        new_points = []
        for p_i in range(len(pontos)):
            p = pontos[p_i].get_centro()
            ponto = [p[0], p[1], 1]
            new_ponto = rotacao_ponto(ponto, dir, obj)
            new_points.append(Ponto(new_ponto[0], new_ponto[1]))
        
        if str_type == "<class 'objects.Reta'>":
            r = Reta()
            r.set_points(new_points)
            return r
        
        p = Poligono()
        p.set_points(new_points)
        return p


def translacao_y_ponto(escala:float, m):
    M_TRANS_Y = np.array([[1, 0, 0], [0, 1, escala], [0, 0, 1]])
    return np.dot(M_TRANS_Y, m)


def translacao_x_ponto(escala:float, m):
    M_TRANS_X = np.array([[1, 0, escala], [0, 1, 0], [0, 0, 1]])
    return np.dot(M_TRANS_X, m)


def rotacao_ponto(m, dir, obj):
    angle = -10 if dir == 'rot_left' else 10
    centro = obj.get_centro()
    leva_ao_centro = np.array([[1, 0, -centro[0]], [0, 1, -centro[1]], [0, 0, 1]])
    cos_theta = np.cos(np.radians(-angle))
    sin_theta = np.sin(np.radians(-angle))
    rotaciona = np.array([[cos_theta, -sin_theta, 0], [sin_theta, cos_theta, 0], [0,0,1]])
    volta_do_centro = np.array([[1, 0, centro[0]], [0, 1, centro[1]], [0, 0, 1]])
    TRANSFORMACAO = np.dot(volta_do_centro, np.dot(rotaciona, leva_ao_centro))
    return np.dot(TRANSFORMACAO, m)


def transformacao_zoom_objeto(obj, tipo, window):
    str_type = str(type(obj))

    if str_type == "<class 'objects.Ponto'>":
        ponto = np.array([obj.get_x(), obj.get_y(), 1])
        return Ponto(ponto[0], ponto[1])

    elif str_type in [ "<class 'objects.Reta'>", "<class 'objects.Poligono'>" ]:
        pontos = obj.get_points()
        new_points = []
        for p_i in range(len(pontos)):
            p = pontos[p_i].get_centro()
            ponto = [p[0], p[1], 1]
            new_ponto = zoom_ponto(ponto, tipo, obj)
            new_points.append(Ponto(new_ponto[0], new_ponto[1]))
        
        if str_type == "<class 'objects.Reta'>":
            r = Reta()
            r.set_points(new_points)
            return r
        
        p = Poligono()
        p.set_points(new_points)
        return p


def zoom_ponto(m, tipo, obj):
    centro = obj.get_centro()
    leva_ao_centro = np.array([[1, 0, -centro[0]], [0, 1, -centro[1]], [0, 0, 1]])
    volta_do_centro = np.array([[1, 0, centro[0]], [0, 1, centro[1]], [0, 0, 1]])
    escala = None
    e = 1.05
    if tipo == 'in':
        escala = np.array([[e, 0, 0 ], [0, e, 0], [0, 0, 1]])
    else:
        escala = np.array([[1/e, 0, 0 ], [0, 1/e, 0], [0, 0, 1]]) # Escala inversa
    TRANSFORMACAO = np.dot(volta_do_centro, np.dot(leva_ao_centro, escala))
    return np.dot(TRANSFORMACAO, m)

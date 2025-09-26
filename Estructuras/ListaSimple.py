from Estructuras.NodoCelda import NodoCelda

class ListaSimple:
    def __init__(self):
        self.primero = None

    def insertar(self, nodo_celda):
        if not self.primero:
            self.primero = nodo_celda
        else:
            actual = self.primero
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nodo_celda

    def __iter__(self):
        actual = self.primero
        while actual:
            yield actual
            actual = actual.siguiente
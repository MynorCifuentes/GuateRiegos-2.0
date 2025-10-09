from Estructuras.Nodo import Nodo

class ListaDobleCircular:
    def __init__(self):
        self.primero = None

    def insertar(self, nodo_celda):
        if not self.primero:
            self.primero = nodo_celda
            nodo_celda.siguiente = nodo_celda
            nodo_celda.anterior = nodo_celda
        else:
            ultimo = self.primero.anterior
            ultimo.siguiente = nodo_celda
            nodo_celda.anterior = ultimo
            nodo_celda.siguiente = self.primero
            self.primero.anterior = nodo_celda

    def __iter__(self):
        actual = self.primero
        if actual:
            while True:
                yield actual
                actual = actual.siguiente
                if actual == self.primero:
                    break
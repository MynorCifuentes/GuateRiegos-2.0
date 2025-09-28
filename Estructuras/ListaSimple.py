from Estructuras.Nodo import Nodo

class ListaSimple:
    def __init__(self):
        self.primero = None
        
    def insertar(self, nuevo_nodo):
        if not self.primero:
            self.primero = nuevo_nodo
        else:
            actual = self.primero
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo

    def agregar_al_final(self, dato):
        nuevo_nodo = Nodo(dato)
        if not self.primero:
            self.primero = nuevo_nodo
        else:
            actual = self.primero
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
            
    def buscar(self, dato_buscado):
        actual = self.primero
        while actual:
            if actual.dato == dato_buscado:
                return True
            actual = actual.siguiente
        return False

    def contar_nodos(self):
        contador = 0
        actual = self.primero
        while actual:
            contador += 1
            actual = actual.siguiente
        return contador

    def __iter__(self):
        actual = self.primero
        while actual:
            yield actual.dato
            actual = actual.siguiente
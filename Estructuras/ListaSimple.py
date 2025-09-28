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
            
    def contar_nodos(self):
        contador = 0
        actual = self.primero
        while actual:
            contador += 1
            actual = actual.siguiente
        return contador
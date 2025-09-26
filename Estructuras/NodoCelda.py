class NodoCelda:
    def __init__(self, info=None):
        self.info = info
        self.siguiente = None    # Para lista doble: siguiente hilera o columna
        self.anterior = None    # Para lista doble: anterior hilera o columna
        # Para matriz de plantas (lista de listas), solo se usan siguiente/anterior para hileras,
        # y para columnas solo siguiente.
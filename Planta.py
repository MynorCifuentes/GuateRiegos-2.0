class Planta:
    def __init__(self, hilera, posicion, litrosAgua, gramosFertilizante, tipo):
        self.hilera = hilera
        self.posicion = posicion
        self.litrosAgua = litrosAgua
        self.gramosFertilizante = gramosFertilizante
        self.tipo = tipo

    def __str__(self):
        return (f"Planta(hilera={self.hilera}, posicion={self.posicion}, litrosAgua={self.litrosAgua}, "
                f"gramosFertilizante={self.gramosFertilizante}, tipo={self.tipo})")
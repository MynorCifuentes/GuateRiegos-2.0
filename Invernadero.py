from Estructuras.ListaDobleCircular import ListaDobleCircular
from Estructuras.ListaSimple import ListaSimple
from Estructuras.NodoCelda import NodoCelda

class Invernadero:
    def __init__(self, nombre, numeroHileras, plantasXhilera):
        self.nombre = nombre
        self.numeroHileras = numeroHileras
        self.plantasXhilera = plantasXhilera
        self.hileras = ListaDobleCircular()    # Cada hilera es un NodoCelda con lista simple de plantas/columnas
        self.asignacionDrones = ListaSimple()  # Lista simple de asignación de drones
        self.planesRiego = ListaSimple()       # Lista simple de planes de riego

    def __str__(self):
        return f"Invernadero(nombre={self.nombre}, hileras={self.numeroHileras}, plantasXhilera={self.plantasXhilera})"
from Estructuras.ListaSimple import ListaSimple
class Invernadero:
    def __init__(self, nombre, numero_hileras, plantas_x_hilera):
        self.nombre = nombre
        self.numero_hileras = numero_hileras
        self.plantas_x_hilera = plantas_x_hilera
        self.lista_plantas = ListaSimple()
        self.asignacion_drones = ListaSimple() # Lista de (dron_id, hilera)
        self.planes_riego = ListaSimple()
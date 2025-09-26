class AsignacionDron:
    def __init__(self, id_dron, hilera):
        self.id_dron = id_dron
        self.hilera = hilera

    def __str__(self):
        return f"AsignacionDron(id_dron={self.id_dron}, hilera={self.hilera})"
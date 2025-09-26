class Dron:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre

    def __str__(self):
        return f"Dron(id={self.id}, nombre={self.nombre})"
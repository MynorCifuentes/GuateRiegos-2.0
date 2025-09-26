class PlanRiego:
    def __init__(self, nombre, secuencia):
        self.nombre = nombre
        self.secuencia = secuencia

    def __str__(self):
        return f"PlanRiego(nombre={self.nombre}, secuencia={self.secuencia})"
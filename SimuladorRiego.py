from Estructuras.NodoCelda import NodoCelda
from Estructuras.ListaSimple import ListaSimple

class SimuladorRiego:
    def __init__(self, gestor, invernadero, plan_riego):
        self.gestor = gestor
        self.invernadero = invernadero  # Objeto Invernadero
        self.plan_riego = plan_riego    # Objeto PlanRiego
        self.tiempo_total = 0  # para simular el tiempo total
        self.log = ListaSimple()

    def buscar_dron_por_hilera(self, hilera):
        asignacion = self.invernadero.asignacionDrones.primero
        while asignacion:
            if asignacion.info.hilera == str(hilera):
                return asignacion.info
            asignacion = asignacion.siguiente
        return None

    def buscar_dron_objeto(self, id_dron):
        actual = self.gestor.drones.primero
        while actual:
            if actual.info.id == id_dron:
                return actual.info
            actual = actual.siguiente
            if actual == self.gestor.drones.primero:
                break
        return None

    def buscar_planta(self, hilera, posicion):
        hilera_actual = self.invernadero.hileras.primero
        contador = 1
        while hilera_actual:
            if contador == hilera:
                planta_actual = hilera_actual.columnas.primero
                while planta_actual:
                    if int(planta_actual.info.posicion) == posicion:
                        return planta_actual.info
                    planta_actual = planta_actual.siguiente
            hilera_actual = hilera_actual.siguiente
            contador += 1
            if hilera_actual == self.invernadero.hileras.primero:
                break
        return None

    def resetear_drones(self):
        asignacion = self.invernadero.asignacionDrones.primero
        while asignacion:
            dron = self.buscar_dron_objeto(asignacion.info.id_dron)
            if dron:
                dron.posicion_actual = 1
                dron.agua_usada = 0
                dron.fertilizante_usado = 0
            asignacion = asignacion.siguiente

    def simular(self):
        self.tiempo_total = 0
        self.log = ListaSimple()
        self.resetear_drones()
        pasos = self.plan_riego.secuencia.split(",")
        for paso in pasos:
            hilera_str, planta_str = paso.split("-")
            hilera = int(hilera_str[1:])  # "H1" -> 1
            posicion = int(planta_str[1:])  # "P2" -> 2

            asignacion = self.buscar_dron_por_hilera(hilera)
            dron = self.buscar_dron_objeto(asignacion.id_dron)
            planta = self.buscar_planta(hilera, posicion)

            movimiento = abs(dron.posicion_actual - posicion)
            self.tiempo_total += movimiento
            if movimiento > 0:
                self.log.insertar(NodoCelda(
                    f"{dron.nombre}: mueve de P{dron.posicion_actual} a P{posicion} ({movimiento}s)"
                ))
            dron.posicion_actual = posicion

            self.tiempo_total += 1
            dron.agua_usada += int(planta.litrosAgua)
            dron.fertilizante_usado += int(planta.gramosFertilizante)
            self.log.insertar(NodoCelda(
                f"{dron.nombre}: riega/fertiliza H{hilera}-P{posicion} (1s)"
            ))

    def obtener_log(self):
        actual = self.log.primero
        resultado = ListaSimple()
        while actual:
            resultado.insertar(NodoCelda(actual.info))
            actual = actual.siguiente
        return resultado

    def obtener_consumo(self):
        # Devuelve una ListaSimple de strings, uno por cada dron asignado
        consumos = ListaSimple()
        asignacion = self.invernadero.asignacionDrones.primero
        while asignacion:
            dron = self.buscar_dron_objeto(asignacion.info.id_dron)
            if dron:
                texto = f"Dron: {dron.nombre} - {dron.agua_usada} L agua, {dron.fertilizante_usado} g fertilizante"
                consumos.insertar(NodoCelda(texto))
            asignacion = asignacion.siguiente
        return consumos

    def resumen(self):
        return f"Tiempo total: {self.tiempo_total} segundos"
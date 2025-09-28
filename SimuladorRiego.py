import re
from Estructuras.NodoCelda import NodoCelda
from Estructuras.ListaSimple import ListaSimple

class SimuladorRiego:
    def __init__(self, gestor, invernadero, plan_riego):
        self.gestor = gestor
        self.invernadero = invernadero  # Objeto Invernadero
        self.plan_riego = plan_riego    # Objeto PlanRiego
        self.tiempo_total = 0
        self.log = ListaSimple()

    def buscar_dron_por_hilera(self, hilera):
        asignacion = self.invernadero.asignacionDrones.primero
        while asignacion:
            if str(asignacion.info.hilera) == str(hilera):
                return asignacion.info
            asignacion = asignacion.siguiente
        return None

    def buscar_dron_objeto(self, id_dron):
        actual = self.gestor.drones.primero
        if not actual:
            return None
        first = actual
        while True:
            if actual.info.id == id_dron:
                return actual.info
            actual = actual.siguiente
            if actual == first:
                break
        return None

    def buscar_planta(self, hilera, posicion):
        hilera_actual = self.invernadero.hileras.primero
        if not hilera_actual:
            return None
        contador = 1
        first = hilera_actual
        while True:
            if contador == hilera:
                planta_actual = hilera_actual.columnas.primero
                while planta_actual:
                    if int(planta_actual.info.posicion) == posicion:
                        return planta_actual.info
                    planta_actual = planta_actual.siguiente
            hilera_actual = hilera_actual.siguiente
            contador += 1
            if hilera_actual == first:
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

        # Normaliza y parsea robustamente la secuencia, tolerando espacios y saltos de línea
        sec = (self.plan_riego.secuencia or "").replace("\n", " ").strip()
        if not sec:
            self.log.insertar(NodoCelda("Plan vacío: no hay pasos para simular."))
            return

        pasos = [p.strip() for p in sec.split(",") if p.strip()]
        patron = re.compile(r"^[Hh]\s*(\d+)\s*-\s*[Pp]\s*(\d+)$")

        for paso in pasos:
            m = patron.match(paso)
            if not m:
                # Loguea y continúa sin romper la simulación
                self.log.insertar(NodoCelda(f"Paso inválido en plan: '{paso}' (omitido)"))
                continue

            hilera = int(m.group(1))
            posicion = int(m.group(2))

            asignacion = self.buscar_dron_por_hilera(hilera)
            if not asignacion:
                self.log.insertar(NodoCelda(f"No hay dron asignado para Hilera {hilera} (paso {paso})."))
                continue

            dron = self.buscar_dron_objeto(asignacion.id_dron)
            if not dron:
                self.log.insertar(NodoCelda(f"No se encontró el dron con id {asignacion.id_dron} (paso {paso})."))
                continue

            planta = self.buscar_planta(hilera, posicion)
            if not planta:
                self.log.insertar(NodoCelda(f"No se encontró la planta H{hilera}-P{posicion} (paso {paso})."))
                continue

            # Movimiento
            movimiento = abs(getattr(dron, "posicion_actual", 1) - posicion)
            self.tiempo_total += movimiento
            if movimiento > 0:
                self.log.insertar(NodoCelda(
                    f"{dron.nombre}: mueve de P{getattr(dron,'posicion_actual',1)} a P{posicion} ({movimiento}s)"
                ))
            dron.posicion_actual = posicion

            # Riego/fertilizado
            self.tiempo_total += 1
            dron.agua_usada = getattr(dron, "agua_usada", 0) + int(planta.litrosAgua)
            dron.fertilizante_usado = getattr(dron, "fertilizante_usado", 0) + int(planta.gramosFertilizante)
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
        consumos = ListaSimple()
        asignacion = self.invernadero.asignacionDrones.primero
        while asignacion:
            dron = self.buscar_dron_objeto(asignacion.info.id_dron)
            if dron:
                texto = f"Dron: {dron.nombre} - {getattr(dron,'agua_usada',0)} L agua, {getattr(dron,'fertilizante_usado',0)} g fertilizante"
                consumos.insertar(NodoCelda(texto))
            asignacion = asignacion.siguiente
        return consumos

    def resumen(self):
        return f"Tiempo total: {self.tiempo_total} segundos"
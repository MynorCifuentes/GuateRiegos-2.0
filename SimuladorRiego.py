from Estructuras.ListaSimple import ListaSimple, Nodo

class InstruccionDron:
    def __init__(self, tiempo, dron_id, accion):
        self.tiempo = tiempo
        self.dron_id = dron_id
        self.accion = accion

class EstadisticaDron:
    def __init__(self, dron_id):
        self.dron_id = dron_id
        self.litros_agua = 0
        self.gramos_fertilizante = 0

class EstadoDron:
    def __init__(self, dron_id):
        self.dron_id = dron_id
        self.posicion = 0
        self.instrucciones = ListaSimple()  # Lista de InstruccionDron

class ParHileraDron:
    def __init__(self, hilera, dron_id):
        self.hilera = hilera
        self.dron_id = dron_id

class PasoPlan:
    def __init__(self, hilera, posicion):
        self.hilera = hilera
        self.posicion = posicion

class SimuladorRiego:
    def __init__(self, invernadero, plan):
        self.invernadero = invernadero
        self.plan = plan
        self.instrucciones_por_tiempo = ListaSimple()  # ListaSimple de ListaSimple (una por segundo)
        self.estadisticas = ListaSimple()  # ListaSimple de EstadisticaDron
        self.tiempo_total = 0

    def simular(self):
        # Lista de pares hilera-dron (no dict nativo)
        lista_hilera_dron = ListaSimple()
        asignacion_actual = self.invernadero.asignacion_drones.primero
        while asignacion_actual:
            dato = asignacion_actual.dato
            lista_hilera_dron.agregar_al_final(ParHileraDron(int(dato.hilera), dato.dron_id))
            asignacion_actual = asignacion_actual.siguiente

        # Crear estados y estadísticas de drones
        estados_dron = ListaSimple()
        estadisticas_dron = ListaSimple()
        actual = lista_hilera_dron.primero
        while actual:
            dron_id = actual.dato.dron_id
            estados_dron.agregar_al_final(EstadoDron(dron_id))
            estadisticas_dron.agregar_al_final(EstadisticaDron(dron_id))
            actual = actual.siguiente

        # Parsear el plan y guardarlo como ListaSimple de PasoPlan
        pasos_nodos = ListaSimple()
        patron = self.plan.patron
        inicio = 0
        fin = 0
        longitud = len(patron)
        while fin < longitud:
            # Buscar la siguiente coma o fin de string
            while fin < longitud and patron[fin] != ',':
                fin += 1
            paso = patron[inicio:fin].strip()
            if paso:
                if '-' in paso:
                    hilera_s, posicion_s = paso.split('-')
                    hilera = int(hilera_s[1:])
                    posicion = int(posicion_s[1:])
                    pasos_nodos.agregar_al_final(PasoPlan(hilera, posicion))
            fin += 1
            inicio = fin

        # Ejecutar el plan
        tiempo = 1
        paso_actual = pasos_nodos.primero
        while paso_actual:
            hilera = paso_actual.dato.hilera
            posicion = paso_actual.dato.posicion

            # Buscar dron asignado a la hilera
            dron_id = None
            actual_hilera_dron = lista_hilera_dron.primero
            while actual_hilera_dron:
                if actual_hilera_dron.dato.hilera == hilera:
                    dron_id = actual_hilera_dron.dato.dron_id
                    break
                actual_hilera_dron = actual_hilera_dron.siguiente

            # Buscar estado del dron
            estado_actual = estados_dron.primero
            estado_obj = None
            while estado_actual:
                if estado_actual.dato.dron_id == dron_id:
                    estado_obj = estado_actual.dato
                    break
                estado_actual = estado_actual.siguiente

            # Movimientos (solo con variables, no listas)
            movs = abs(posicion - estado_obj.posicion)
            mov_dir = "Adelante" if posicion > estado_obj.posicion else "Atrás"
            for m in range(movs):
                nueva_pos = estado_obj.posicion + (m+1) if mov_dir == "Adelante" else estado_obj.posicion - (m+1)
                accion = f"{mov_dir} (H{hilera}P{nueva_pos})"
                estado_obj.instrucciones.agregar_al_final(InstruccionDron(tiempo, dron_id, accion))
                tiempo += 1
            estado_obj.posicion = posicion

            # Acción de regar
            estado_obj.instrucciones.agregar_al_final(InstruccionDron(tiempo, dron_id, "Regar"))
            tiempo += 1

            # Sumar consumo de agua/fertilizante
            planta_actual = None
            actual_planta = self.invernadero.lista_plantas.primero
            while actual_planta:
                p = actual_planta.dato
                if p.hilera == hilera and p.posicion == posicion:
                    planta_actual = p
                    break
                actual_planta = actual_planta.siguiente
            if planta_actual:
                estadistica = estadisticas_dron.primero
                while estadistica:
                    if estadistica.dato.dron_id == dron_id:
                        estadistica.dato.litros_agua += planta_actual.litros_agua
                        estadistica.dato.gramos_fertilizante += planta_actual.gramos_fertilizante
                        break
                    estadistica = estadistica.siguiente

            paso_actual = paso_actual.siguiente

        # Construir tabla de instrucciones por tiempo usando solo ListaSimple
        tiempo_max = 0
        actual_estado = estados_dron.primero
        while actual_estado:
            instr = actual_estado.dato.instrucciones.primero
            prev_t = 0
            while instr:
                prev_t = instr.dato.tiempo
                instr = instr.siguiente
            if prev_t > tiempo_max:
                tiempo_max = prev_t
            actual_estado = actual_estado.siguiente

        for t in range(1, tiempo_max + 2):
            fila = ListaSimple()
            actual_estado = estados_dron.primero
            while actual_estado:
                dron_id = actual_estado.dato.dron_id
                instr = actual_estado.dato.instrucciones.primero
                accion = "Esperar"
                prev_t = 0
                last_accion = None
                while instr:
                    if instr.dato.tiempo == t:
                        accion = instr.dato.accion
                        break
                    prev_t = instr.dato.tiempo
                    last_accion = instr.dato.accion
                    instr = instr.siguiente
                else:
                    # Si ya terminó sus instrucciones, FIN
                    if last_accion == "Regar" and prev_t < t:
                        accion = "FIN"
                fila.agregar_al_final((dron_id, accion))
                actual_estado = actual_estado.siguiente
            self.instrucciones_por_tiempo.agregar_al_final(fila)

        self.estadisticas = estadisticas_dron
        self.tiempo_total = tiempo_max

    def get_instrucciones(self):
        filas = ListaSimple()
        actual = self.instrucciones_por_tiempo.primero
        while actual:
            fila = ListaSimple()
            actual_accion = actual.dato.primero
            while actual_accion:
                fila.agregar_al_final(actual_accion.dato)
                actual_accion = actual_accion.siguiente
            filas.agregar_al_final(fila)
            actual = actual.siguiente
        return filas

    def get_estadisticas(self):
        stats = ListaSimple()
        actual = self.estadisticas.primero
        while actual:
            stats.agregar_al_final(actual.dato)
            actual = actual.siguiente
        return stats
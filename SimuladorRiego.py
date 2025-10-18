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
        self.movimientos = ListaSimple()  # ListaSimple de posiciones pendientes
        self.acciones = ListaSimple()     # ListaSimple de acciones de riego pendientes
        self.instrucciones = ListaSimple()  # ListaSimple de InstruccionDron

class ParHileraDron:
    def __init__(self, hilera, dron_id):
        self.hilera = hilera
        self.dron_id = dron_id

class PasoPlan:
    def __init__(self, hilera, posicion):
        self.hilera = hilera
        self.posicion = posicion

class AccionRiego:
    def __init__(self, hilera, posicion, litro_actual, litros_totales, gramos_fertilizante):
        self.hilera = hilera
        self.posicion = posicion
        self.litro_actual = litro_actual
        self.litros_totales = litros_totales
        self.gramos_fertilizante = gramos_fertilizante

class SimuladorRiego:
    def __init__(self, invernadero, plan):
        self.invernadero = invernadero
        self.plan = plan
        self.instrucciones_por_tiempo = ListaSimple()  # ListaSimple de ListaSimple 
        self.estadisticas = ListaSimple()  # ListaSimple de EstadisticaDron
        self.tiempo_total = 0

    def buscar_estado_dron(self, lista_estados, dron_id):
        actual = lista_estados.primero
        while actual:
            if actual.dato.dron_id == dron_id:
                return actual.dato
            actual = actual.siguiente
        return None

    def buscar_estadistica_dron(self, lista_estadisticas, dron_id):
        actual = lista_estadisticas.primero
        while actual:
            if actual.dato.dron_id == dron_id:
                return actual.dato
            actual = actual.siguiente
        return None

    def buscar_par_hilera_dron(self, lista_pars, hilera):
        actual = lista_pars.primero
        while actual:
            if actual.dato.hilera == hilera:
                return actual.dato.dron_id
            actual = actual.siguiente
        return None

    def simular(self):
        # 1. Cargar la asignación de drones por hilera
        lista_hilera_dron = ListaSimple()
        asignacion_actual = self.invernadero.asignacion_drones.primero
        while asignacion_actual:
            dato = asignacion_actual.dato
            lista_hilera_dron.agregar_al_final(ParHileraDron(int(dato.hilera), dato.dron_id))
            asignacion_actual = asignacion_actual.siguiente

        # 2. Crear estados y estadísticas de drones
        estados_dron = ListaSimple()
        estadisticas_dron = ListaSimple()
        actual = lista_hilera_dron.primero
        while actual:
            dron_id = actual.dato.dron_id
            estados_dron.agregar_al_final(EstadoDron(dron_id))
            estadisticas_dron.agregar_al_final(EstadisticaDron(dron_id))
            actual = actual.siguiente

        # 3. Parsear el plan y guardarlo como ListaSimple de PasoPlan
        pasos_nodos = ListaSimple()
        patron = self.plan.patron
        inicio = 0
        fin = 0
        longitud = len(patron)
        while fin < longitud:
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

        # 4. Prepara la cola global de riegos en el orden del plan
        cola_riegos = ListaSimple()
        actual_paso = pasos_nodos.primero
        while actual_paso:
            paso = actual_paso.dato
            dron_id = self.buscar_par_hilera_dron(lista_hilera_dron, paso.hilera)
            # Buscar la planta para saber litros
            planta_actual = None
            actual_planta = self.invernadero.lista_plantas.primero
            while actual_planta:
                p = actual_planta.dato
                if p.hilera == paso.hilera and p.posicion == paso.posicion:
                    planta_actual = p
                    break
                actual_planta = actual_planta.siguiente
            if planta_actual:
                for l in range(planta_actual.litros_agua):
                    cola_riegos.agregar_al_final((dron_id, paso.hilera, paso.posicion, l+1, planta_actual.litros_agua, planta_actual.gramos_fertilizante))
            actual_paso = actual_paso.siguiente

        # 5. Inicializa los movimientos y acciones pendientes de cada dron
        actual_estado = estados_dron.primero
        while actual_estado:
            estado = actual_estado.dato
            # Por cada paso del plan que corresponda a este dron
            actual_paso2 = pasos_nodos.primero
            pos_actual = estado.posicion
            while actual_paso2:
                paso = actual_paso2.dato
                dron_id = self.buscar_par_hilera_dron(lista_hilera_dron, paso.hilera)
                if dron_id == estado.dron_id:
                    # Movimientos
                    movimientos = []
                    if paso.posicion > pos_actual:
                        for pos in range(pos_actual+1, paso.posicion+1):
                            movimientos.append(pos)
                    elif paso.posicion < pos_actual:
                        for pos in range(pos_actual-1, paso.posicion-1, -1):
                            movimientos.append(pos)
                    for m in movimientos:
                        estado.movimientos.agregar_al_final(m)
                    pos_actual = paso.posicion
                    # Acciones riego
                    planta_actual = None
                    actual_planta = self.invernadero.lista_plantas.primero
                    while actual_planta:
                        p = actual_planta.dato
                        if p.hilera == paso.hilera and p.posicion == paso.posicion:
                            planta_actual = p
                            break
                        actual_planta = actual_planta.siguiente
                    if planta_actual:
                        for l in range(planta_actual.litros_agua):
                            estado.acciones.agregar_al_final(AccionRiego(paso.hilera, paso.posicion, l+1, planta_actual.litros_agua, planta_actual.gramos_fertilizante))
                actual_paso2 = actual_paso2.siguiente
            actual_estado = actual_estado.siguiente

        # 6. Paso a paso del simulador
        tiempo = 1
        # Para saber si cada dron terminó
        drones_fin = ListaSimple()
        actual_estado = estados_dron.primero
        while actual_estado:
            drones_fin.agregar_al_final((actual_estado.dato.dron_id, False))
            actual_estado = actual_estado.siguiente

        riego_global = cola_riegos.primero  # Nodo de la cola global de riegos
        while True:
            fila = ListaSimple()
            actual_estado = estados_dron.primero
            todos_fin = True
            # 1. Movimientos en paralelo
            while actual_estado:
                estado = actual_estado.dato
                dron_id = estado.dron_id
                fin = False
                # Verifica si ya terminó
                actual_fin = drones_fin.primero
                while actual_fin:
                    if actual_fin.dato[0] == dron_id:
                        fin = actual_fin.dato[1]
                        break
                    actual_fin = actual_fin.siguiente
                if fin:
                    fila.agregar_al_final((dron_id, "FIN"))
                    actual_estado = actual_estado.siguiente
                    continue
                todos_fin = False

                # Si tiene movimientos pendientes, avanza uno por tick
                if estado.movimientos.primero:
                    mov_nodo = estado.movimientos.primero
                    pos_dest = mov_nodo.dato
                    mov_dir = "Adelante" if pos_dest > estado.posicion else "Atrás"
                    accion = f"{mov_dir} (H{dron_id}P{pos_dest})"
                    estado.posicion = pos_dest
                    estado.instrucciones.agregar_al_final(InstruccionDron(tiempo, dron_id, accion))
                    fila.agregar_al_final((dron_id, accion))
                    # Elimina movimiento realizado
                    estado.movimientos.primero = mov_nodo.siguiente
                # Si está en posición y es su turno de riego, lo hace solo si es el siguiente del plan global
                elif estado.acciones.primero:
                    if riego_global and riego_global.dato[0] == dron_id:
                        # Es el turno de este dron de regar
                        _, hilera, posicion, litro_actual, litros_totales, gramos_fert = riego_global.dato
                        accion = f"Regar ({litro_actual}/{litros_totales} L)"
                        estado.instrucciones.agregar_al_final(InstruccionDron(tiempo, dron_id, accion))
                        fila.agregar_al_final((dron_id, accion))
                        # Sumar consumo de agua/fertilizante solo en el último litro
                        if litro_actual == litros_totales:
                            estadistica = self.buscar_estadistica_dron(estadisticas_dron, dron_id)
                            if estadistica:
                                estadistica.litros_agua += litros_totales
                                estadistica.gramos_fertilizante += gramos_fert
                        # Avanza el riego global solo si se ejecutó el rieg
                        # Elmina acción riego realizada
                        estado.acciones.primero = estado.acciones.primero.siguiente
                        # Avanza el nodo global de riego
                        riego_global = riego_global.siguiente
                    else:
                        fila.agregar_al_final((dron_id, "Esperar"))
                        estado.instrucciones.agregar_al_final(InstruccionDron(tiempo, dron_id, "Esperar"))
                else:
                    # Ya terminó sus instrucciones
                    fila.agregar_al_final((dron_id, "FIN"))
                    estado.instrucciones.agregar_al_final(InstruccionDron(tiempo, dron_id, "FIN"))
                    # Marca el dron como terminado
                    actual_fin = drones_fin.primero
                    while actual_fin:
                        if actual_fin.dato[0] == dron_id:
                            actual_fin.dato = (dron_id, True)
                            break
                        actual_fin = actual_fin.siguiente
                actual_estado = actual_estado.siguiente
            self.instrucciones_por_tiempo.agregar_al_final(fila)
            tiempo += 1
            if todos_fin:
                break

        # Copia estadísticas finales 
        self.estadisticas = ListaSimple()
        actual = estadisticas_dron.primero
        while actual:
            self.estadisticas.agregar_al_final(actual.dato)
            actual = actual.siguiente
        self.tiempo_total = tiempo - 1

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
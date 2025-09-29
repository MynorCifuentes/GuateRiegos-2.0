from graphviz import Digraph

def graficar_tda_simulador(simulador, tiempo, ruta_salida='static/grafo_tda.png'):
    dot = Digraph(comment='Estado de los TDAs en tiempo t', format='png')
    dot.attr(rankdir='LR')

    # Por cada dron, muestra su lista de instrucciones hasta tiempo t
    actual_estado = simulador.estadisticas.primero
    while actual_estado:
        dron_id = actual_estado.dato.dron_id
        dot.node(f'dron_{dron_id}', f'Dron: {dron_id}', shape='box', style='filled', fillcolor='lightblue')
        actual_estado = actual_estado.siguiente

    actual_estado = simulador.estadisticas.primero
    while actual_estado:
        dron_id = actual_estado.dato.dron_id
        # Busca el estado del dron correspondiente para instrucciones
        actual_estado_dron = simulador.instrucciones_por_tiempo.primero
        t = 1
        prev_accion = None
        while actual_estado_dron and t <= tiempo:
            fila = actual_estado_dron.dato
            actual_accion = fila.primero
            while actual_accion:
                dron, accion = actual_accion.dato
                if dron == dron_id and accion and accion.lower() != "esperar":
                    dot.node(f"{dron_id}_t{t}", f"{accion} (t={t})", shape='ellipse')
                    if prev_accion:
                        dot.edge(prev_accion, f"{dron_id}_t{t}")
                    else:
                        dot.edge(f'dron_{dron_id}', f"{dron_id}_t{t}")
                    prev_accion = f"{dron_id}_t{t}"
                actual_accion = actual_accion.siguiente
            actual_estado_dron = actual_estado_dron.siguiente
            t += 1
        actual_estado = actual_estado.siguiente

    dot.render(ruta_salida, format='png', cleanup=True)
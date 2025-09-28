from graphviz import Digraph
from Estructuras.ListaSimple import ListaSimple
from Estructuras.NodoCelda import NodoCelda

class TDAVisualizer:
    def __init__(self):
        self.dot = Digraph(comment='Estado de TDAs')
        self.dot.attr(rankdir='LR')

    def visualizar_listas(self, invernadero, tiempo_actual):
        self.dot.clear()
        nodos_creados = ListaSimple()
        
        # Visualizar Lista Doble Circular de Hileras
        with self.dot.subgraph(name='cluster_hileras') as h:
            h.attr(label='Hileras (Lista Doble Circular)')
            prev_node = None
            actual = invernadero.hileras.primero
            if actual:
                first = actual
                while True:
                    node_id = f"h{id(actual)}"
                    h.node(node_id, f"Hilera {actual.info}")
                    nodos_creados.insertar(NodoCelda(node_id))
                    
                    if prev_node:
                        h.edge(prev_node, node_id)
                        h.edge(node_id, prev_node, dir='back')
                    
                    # Visualizar plantas de la hilera
                    with h.subgraph(name=f'cluster_{node_id}') as p:
                        p.attr(label=f'Plantas Hilera {actual.info}')
                        planta_actual = actual.columnas.primero
                        prev_planta = None
                        while planta_actual:
                            planta_id = f"p{id(planta_actual)}"
                            p.node(planta_id, f"{planta_actual.info.tipo}\nPos:{planta_actual.info.posicion}")
                            nodos_creados.insertar(NodoCelda(planta_id))
                            if prev_planta:
                                p.edge(prev_planta, planta_id)
                            prev_planta = planta_id
                            planta_actual = planta_actual.siguiente
                    
                    prev_node = node_id
                    actual = actual.siguiente
                    if actual == first:
                        # Cerrar el círculo
                        primer_nodo = nodos_creados.primero.info
                        h.edge(node_id, primer_nodo)
                        h.edge(primer_nodo, node_id, dir='back')
                        break
        
        # Visualizar estado actual de los drones
        with self.dot.subgraph(name='cluster_drones') as d:
            d.attr(label=f'Estado Drones (t={tiempo_actual}s)')
            asignacion = invernadero.asignacionDrones.primero
            while asignacion:
                d.node(f"d{asignacion.info.id_dron}", 
                      f"Dron {asignacion.info.id_dron}\nHilera: {asignacion.info.hilera}")
                asignacion = asignacion.siguiente

        return self.dot

    def guardar_grafico(self, tiempo):
        self.dot.render(f'estado_tdas_t{tiempo}', format='png', cleanup=True)
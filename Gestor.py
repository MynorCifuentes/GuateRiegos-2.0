import xml.etree.ElementTree as ET
from Estructuras.ListaDobleCircular import ListaDobleCircular
from Estructuras.ListaSimple import ListaSimple
from Estructuras.NodoCelda import NodoCelda
from Dron import Dron
from Planta import Planta
from AsignacionDron import AsignacionDron
from PlanRiego import PlanRiego
from Invernadero import Invernadero

class Gestor:
    def __init__(self):
        self.drones = ListaDobleCircular()
        self.invernaderos = ListaDobleCircular()

    def leer_xml(self, ruta_archivo):
        try:
            tree = ET.parse(ruta_archivo)
            root = tree.getroot()

            # Drones: lista doble circular
            for dron in root.find('listaDrones').findall('dron'):
                id_dron = dron.get('id')
                nombre_dron = dron.get('nombre')
                objeto_dron = Dron(id_dron, nombre_dron)
                self.drones.insertar(NodoCelda(objeto_dron))

            # Invernaderos: lista doble circular
            for inv in root.find('listaInvernaderos').findall('invernadero'):
                nombre = inv.get('nombre')
                numero_hileras = int(inv.find('numeroHileras').text)
                plantas_x_hilera = int(inv.find('plantasXhilera').text)
                invernadero = Invernadero(nombre, numero_hileras, plantas_x_hilera)

                # Hileras (lista doble circular)
                for nh in range(1, numero_hileras + 1):
                    hilera_nodo = NodoCelda(info=f"Hilera {nh}")
                    hilera_nodo.columnas = ListaSimple()
                    # Plantas de la hilera (lista simple)
                    for planta in inv.find('listaPlantas').findall('planta'):
                        if int(planta.get('hilera')) == nh:
                            pos = planta.get('posicion')
                            litrosAgua = planta.get('litrosAgua')
                            gramosFertilizante = planta.get('gramosFertilizante')
                            tipo = planta.text.strip()
                            objeto_planta = Planta(nh, pos, litrosAgua, gramosFertilizante, tipo)
                            hilera_nodo.columnas.insertar(NodoCelda(objeto_planta))
                    invernadero.hileras.insertar(hilera_nodo)

                # Asignación drones (lista simple)
                for asignacion in inv.find('asignacionDrones').findall('dron'):
                    id_dron = asignacion.get('id')
                    hilera = asignacion.get('hilera')
                    objeto_asignacion = AsignacionDron(id_dron, hilera)
                    invernadero.asignacionDrones.insertar(NodoCelda(objeto_asignacion))

                # Planes de riego (lista simple)
                for plan in inv.find('planesRiego').findall('plan'):
                    nombre_plan = plan.get('nombre')
                    secuencia = plan.text.strip()
                    objeto_plan = PlanRiego(nombre_plan, secuencia)
                    invernadero.planesRiego.insertar(NodoCelda(objeto_plan))

                self.invernaderos.insertar(NodoCelda(invernadero))

            return True, "Archivo leído y almacenado en las estructuras personalizadas"
        except Exception as e:
            return False, f"Error al leer el archivo: {str(e)}"

    def mostrar_drones(self):
        actual = self.drones.primero
        if actual:
            while True:
                print(actual.info)
                actual = actual.siguiente
                if actual == self.drones.primero:
                    break

    def mostrar_invernaderos(self):
        actual = self.invernaderos.primero
        if actual:
            while True:
                print(actual.info)
                actual = actual.siguiente
                if actual == self.invernaderos.primero:
                    break

    def mostrar_plantas_por_hilera(self, invernadero_nodo):
        # Muestra las plantas de cada hilera en un invernadero dado
        hilera_actual = invernadero_nodo.info.hileras.primero
        if hilera_actual:
            contador = 1
            while True:
                print(f"Hilera {contador}:")
                planta_actual = hilera_actual.columnas.primero
                while planta_actual:
                    print(f"  {planta_actual.info}")
                    planta_actual = planta_actual.siguiente
                hilera_actual = hilera_actual.siguiente
                contador += 1
                if hilera_actual == invernadero_nodo.info.hileras.primero:
                    break
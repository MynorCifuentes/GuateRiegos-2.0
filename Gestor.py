import xml.etree.ElementTree as ET
from Estructuras.ListaSimple import ListaSimple
from Dron import Dron
from Planta import Planta
from AsignacionDron import AsignacionDron
from PlanRiego import PlanRiego
from Invernadero import Invernadero

class Gestor:
    def __init__(self, ruta_xml):
        self.ruta_xml = ruta_xml
        self.drones = self.cargar_drones()
        self.invernaderos = self.cargar_invernaderos()

    def cargar_drones(self):
        lista_drones = ListaSimple()
        try:
            tree = ET.parse(self.ruta_xml)
            root = tree.getroot()
            for dron_xml in root.find('listaDrones').findall('dron'):
                dron = Dron(
                    id = dron_xml.attrib.get('id'),
                    nombre = dron_xml.attrib.get('nombre')
                )
                lista_drones.agregar_al_final(dron)
        except Exception as e:
            print("Error al cargar drones:", e)
        return lista_drones

    def cargar_invernaderos(self):
        lista_invernaderos = ListaSimple()
        try:
            tree = ET.parse(self.ruta_xml)
            root = tree.getroot()
            for inv_xml in root.find('listaInvernaderos').findall('invernadero'):
                nombre = inv_xml.attrib.get('nombre')
                numero_hileras = int(inv_xml.find('numeroHileras').text)
                plantas_x_hilera = int(inv_xml.find('plantasXhilera').text)
                obj_invernadero = Invernadero(nombre, numero_hileras, plantas_x_hilera)
                # Plantas
                for planta_xml in inv_xml.find('listaPlantas').findall('planta'):
                    planta = Planta(
                        hilera = int(planta_xml.attrib.get('hilera')),
                        posicion = int(planta_xml.attrib.get('posicion')),
                        litros_agua = int(planta_xml.attrib.get('litrosAgua')),
                        gramos_fertilizante = int(planta_xml.attrib.get('gramosFertilizante')),
                        nombre = planta_xml.text.strip()
                    )
                    obj_invernadero.lista_plantas.agregar_al_final(planta)
                # Asignacion drones
                for dron_xml in inv_xml.find('asignacionDrones').findall('dron'):
                    asignacion = AsignacionDron(
                        dron_id = dron_xml.attrib.get('id'),
                        hilera = dron_xml.attrib.get('hilera')
                    )
                    obj_invernadero.asignacion_drones.agregar_al_final(asignacion)
                # Planes de riego
                for plan_xml in inv_xml.find('planesRiego').findall('plan'):
                    plan = PlanRiego(
                        nombre = plan_xml.attrib.get('nombre'),
                        patron = plan_xml.text.strip()
                    )
                    obj_invernadero.planes_riego.agregar_al_final(plan)
                lista_invernaderos.agregar_al_final(obj_invernadero)
        except Exception as e:
            print("Error al cargar invernaderos:", e)
        return lista_invernaderos
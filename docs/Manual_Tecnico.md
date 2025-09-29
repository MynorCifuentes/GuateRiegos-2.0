# Manual Técnico

## Estructura General del Proyecto

- **Lenguaje Principal:** Python (Flask para backend web)
- **Frontend:** HTML + Bootstrap
- **Estructuras de datos:** Listas simples implementadas manualmente.
- **Carpetas Principales:**
  - `Estructuras/`: Implementaciones personalizadas de listas y nodos.
  - `templates/`: HTML para las vistas.
  - Archivos de lógica principal (`Gestor.py`, `SimuladorRiego.py`, etc).

---

## Principales Clases y Algoritmos

### 1. Carga y Parseo del Archivo XML

```python
import xml.etree.ElementTree as ET

tree = ET.parse(xml_path)
root = tree.getroot()
for inv_xml in root.findall('invernadero'):
    obj_invernadero = Invernadero(...)
    # Plantas
    for planta_xml in inv_xml.find('plantas').findall('planta'):
        planta = Planta(
            hilera = int(planta_xml.attrib.get('hilera')),
            posicion = int(planta_xml.attrib.get('posicion')),
            litros_agua = int(planta_xml.attrib.get('litrosAgua')),
            gramos_fertilizante = int(planta_xml.attrib.get('gramosFertilizante')),
            nombre = planta_xml.text.strip()
        )
        obj_invernadero.lista_plantas.agregar_al_final(planta)
    # Asignación drones
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
```

---

### 2. Estructura de Datos: Lista Simple y Nodo

```python
class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

class ListaSimple:
    def __init__(self):
        self.primero = None

    def agregar_al_final(self, dato):
        nuevo = Nodo(dato)
        if not self.primero:
            self.primero = nuevo
        else:
            actual = self.primero
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo
```

---

### 3. Asignación de Drones a Hileras

```python
class AsignacionDron:
    def __init__(self, dron_id, hilera):
        self.dron_id = dron_id
        self.hilera = hilera
```

```python
for dron_xml in inv_xml.find('asignacionDrones').findall('dron'):
    asignacion = AsignacionDron(
        dron_id = dron_xml.attrib.get('id'),
        hilera = dron_xml.attrib.get('hilera')
    )
    obj_invernadero.asignacion_drones.agregar_al_final(asignacion)
```

---

### 4. Simulación del Proceso de Riego

```python
for paso in plan.pasos:
    # Buscar dron asignado a la hilera
    dron = buscar_dron_para_hilera(paso.hilera)
    # Crear instrucción
    instruccion = InstruccionDron(tiempo_actual, dron.id, accion)
    estado_dron = obtener_estado_dron(dron.id)
    estado_dron.instrucciones.agregar_al_final(instruccion)
    # Actualizar estadísticas del dron
    estadistica = obtener_estadistica_dron(dron.id)
    estadistica.litros_agua += planta.litros_agua
    estadistica.gramos_fertilizante += planta.gramos_fertilizante
    tiempo_actual += 1
```

---

### 5. Generación de Reporte HTML

```python
def generar_reporte_html(invernadero, plan, estadisticas, instrucciones):
    html = "<h2>Reporte de Simulación</h2>"
    html += "<table>...</table>"
    # Construir tablas e información relevante
    return html
```

---

### 6. Generación de Archivo XML de Resultados

```python
import xml.etree.ElementTree as ET

root = ET.Element("resultados")
for invernadero in invernaderos:
    inv_elem = ET.SubElement(root, "invernadero", nombre=invernadero.nombre)
    # Agrega estadísticas e instrucciones según estructura
tree = ET.ElementTree(root)
tree.write("salida.xml")
```

---

### 7. Estado en Tiempo “t”

```python
def obtener_estado_en_t(instrucciones, t):
    estado_t = []
    for dron in drones:
        acciones = [inst for inst in instrucciones if inst.tiempo <= t and inst.dron_id == dron.id]
        estado_t.append(acciones[-1] if acciones else None)
    return estado_t
```

---

## Extensibilidad

- Para nuevos reportes, crea funciones similares a `generar_reporte_html`.
- Para nuevos tipos de planes de riego, extiende la clase `PlanRiego` y ajusta el flujo de simulación.

---

## Ejecución y Despliegue

1. Instala dependencias:
   ```sh
   pip install -r requirements.txt
   ```
2. Ejecuta la aplicación:
   ```sh
   python app.py
   ```
3. Accede desde tu navegador a: http://localhost:5000

---

## Resolución de Problemas

- Si hay errores al cargar archivos, revisa la estructura del XML.
- Asegúrate de tener todas las dependencias instaladas.
- Consulta mensajes en consola para identificar problemas específicos.

---

## Créditos

Desarrollado por Mynor Cifuentes.

Para soporte consulta el [repositorio en GitHub](https://github.com/MynorCifuentes/IPC2_Proyecto2_201318644).
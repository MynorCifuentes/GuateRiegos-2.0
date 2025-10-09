# Manual Técnico – GuateRiegos 2.0

## 1. Descripción General

**GuateRiegos 2.0** es una aplicación web desarrollada en Python y el framework Flask.  
Simula el proceso automatizado de riego y fertilización en invernaderos, permitiendo la carga de configuraciones XML, selección de planes, ejecución de simulaciones y generación de reportes HTML/XML.


## 2. Instalación de Dependencias

**Recomendación:** Usar un entorno virtual (venv).

### En Windows

```bat
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### En Ubuntu/Linux

```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
sudo apt-get install graphviz
```

**Dependencias principales:**  
Tu archivo `requirements.txt` ya incluye todas las dependencias necesarias:

```
blinker==1.9.0
certifi==2025.8.3
charset-normalizer==3.4.3
click==8.3.0
colorama==0.4.6
Flask==3.1.2
git-filter-repo==2.47.0
graphviz==0.21
idna==3.10
itsdangerous==2.2.0
Jinja2==3.1.6
MarkupSafe==3.0.2
requests==2.32.5
urllib3==2.5.0
Werkzeug==3.1.3
```

**Nota:** En Ubuntu/Linux necesitas instalar el paquete de sistema `graphviz` además de la librería Python.



## 3. Principales Funciones y Estructuras

### 3.1. Carga y gestión de invernaderos (`Gestor.py`)

```python
import xml.etree.ElementTree as ET

class Gestor:
    def cargar_invernaderos(self):
        lista_invernaderos = ListaSimple()
        tree = ET.parse(self.ruta_xml)
        root = tree.getroot()
        for inv_xml in root.find('listaInvernaderos').findall('invernadero'):
            nombre = inv_xml.attrib.get('nombre')
            obj_invernadero = Invernadero(nombre, ...)
            # Plantas, drones, planes...
            lista_invernaderos.agregar_al_final(obj_invernadero)
        return lista_invernaderos
```



### 3.2. Simulación del proceso de riego (`SimuladorRiego.py`)

```python
class SimuladorRiego:
    def simular(self):
        # Crea lista de pares hilera-dron
        # Agrega instrucciones y estadísticas
        for paso in plan.pasos:
            dron = buscar_dron_para_hilera(paso.hilera)
            estado_dron = obtener_estado_dron(dron.id)
            estado_dron.instrucciones.agregar_al_final(InstruccionDron(...))
        self.estadisticas = estadisticas_dron
        self.tiempo_total = tiempo_max
```



### 3.3. Generación de reporte HTML (`reporte.html`)

```html
<h2 class="mb-3" style="color:#800000;">Reporte de Simulación</h2>
<h4>Invernadero: {{ invernadero.nombre }}</h4>
<table class="table table-bordered">
    <thead>
        <tr>
            <th>ID Dron</th>
            <th>Litros de Agua</th>
            <th>Gramos de Fertilizante</th>
        </tr>
    </thead>
    <tbody>
    {% for estadistica in estadisticas %}
        <tr>
            <td>{{ estadistica.dron_id }}</td>
            <td>{{ estadistica.litros_agua }}</td>
            <td>{{ estadistica.gramos_fertilizante }}</td>
        </tr>
    {% endfor %}
    </tbody>
</table>
```



### 3.4. Visualización de instrucciones por tiempo (`simulacion.html`)

```html
<h5>Instrucciones por Tiempo</h5>
<table class="table table-sm table-striped">
    <thead>
        <tr>
            <th>Tiempo (s)</th>
            {% for estadistica in estadisticas %}
            <th>Dron {{ estadistica.dron_id }}</th>
            {% endfor %}
        </tr>
    </thead>
    <tbody>
    {% set t = 1 %}
    {% for fila in instrucciones %}
        <tr>
            <td>{{ t }}</td>
            {% for accion in fila %}
                <td>{{ accion[1] }}</td>
            {% endfor %}
        </tr>
        {% set t = t + 1 %}
    {% endfor %}
    </tbody>
</table>
```



### 3.5. Graficación de TDAs (`graficar_tda.py`)

```python
from graphviz import Digraph

def graficar_tda_simulador(simulador, tiempo, ruta_salida='static/grafo_tda.png'):
    dot = Digraph(comment='Estado de los TDAs en tiempo t', format='png')
    dot.attr(rankdir='LR')
    # Añade nodos y aristas por drone/instrucción
    dot.render(ruta_salida, format='png', cleanup=True)
```



### 3.6. Listas Simples y Dobles (`Estructuras/ListaSimple.py`)

```python
class ListaSimple:
    def agregar_al_final(self, dato):
        nuevo_nodo = Nodo(dato)
        if not self.primero:
            self.primero = nuevo_nodo
        else:
            actual = self.primero
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
```



### 3.7. Estructura de Nodo (`Estructuras/Nodo.py`)

```python
class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None
        self.anterior = None
```



## 4. Templates HTML Importantes

- **base.html:** Contiene los bloques principales de la interfaz.
- **index.html:** Página principal y carga de XML.
- **invernadero.html:** Detalle y selección de plan.
- **simulacion.html:** Resultados y opciones avanzadas.
- **reporte.html:** Reporte detallado para cada simulación.
- **grafo_tda.html:** Visualización de grafos de TDAs.

---

## 5. Diagrama de Clases y Diagramas de Actividad


- **Diagrama de Clases:**  
  ![Diagrama de Clases](/docs/DiagramaClases.png)

- **Diagrama de Actividad – Simulación:**  
  ![Actividad Simulacion](/docs/DiagramaActividad.png)

- **Diagrama de Actividad – Asignación de Drones:**  
  ![Actividad Asignacion Drones](/docs/DiagramaActividad2.png)

---

## 6. Ejecución

### Windows

```bat
venv\Scripts\activate
python App.py
```

### Ubuntu/Linux

```sh
source venv/bin/activate
python3 App.py
```

La aplicación correrá en [http://localhost:5000](http://localhost:5000)

---

## 7. Notas para Extensión y Mantenimiento

- Para agregar nuevos reportes, crea funciones similares a las de generación HTML/XML.
- Para nuevos tipos de planes, extiende la clase `PlanRiego` y ajusta la lógica en `SimuladorRiego`.
- Los diagramas y grafos pueden actualizarse fácilmente agregando nodos/aristas en `graficar_tda.py`.

---

## 8. Referencias y Créditos

Desarrollado por Mynor Cifuentes.  
Consulta la [documentación online en GitHub](https://github.com/MynorCifuentes/IPC2_Proyecto2_201318644) para más detalles y soporte.

Para reportar errores o sugerencias puedes hacerlos a través de los issues del repositorio:
[Issues GuateRiegos 2.0](https://github.com/MynorCifuentes/IPC2_Proyecto2_201318644/issues).

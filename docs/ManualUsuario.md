# Manual de Usuario

## Introducción

Esta aplicación web permite simular el proceso de riego y fertilización automatizada en invernaderos utilizando drones. El sistema asigna drones a hileras y ejecuta planes de riego definidos en archivos XML de configuración. El usuario puede cargar archivos, seleccionar invernaderos y planes, simular procesos, visualizar estadísticas y generar reportes.

---

## Requisitos

- Navegador web moderno (Chrome, Firefox, Edge, etc.).
- Archivo de configuración XML válido y estructurado según las especificaciones del sistema.
- Acceso a la URL donde está desplegada la aplicación (ejemplo: http://localhost:5000).

---

## Primeros Pasos

1. Abre tu navegador y accede a la URL de la aplicación.
2. Se mostrará la página principal del simulador de riego automatizado.

---

## Funcionalidades Principales

### 1. Cargar archivo de configuración XML

- Haz clic en el botón “Cargar archivo XML”.
- Selecciona el archivo XML desde tu equipo.
- Presiona el botón “Cargar”.
- Si el archivo es válido, aparecerá una lista de invernaderos disponibles.

### 2. Seleccionar invernadero y plan de riego

- En la lista, haz clic en el nombre del invernadero que deseas simular.
- Se mostrarán los detalles del invernadero (cantidad de hileras, plantas por hilera, etc.).
- Selecciona un plan de riego de la lista desplegable y presiona el botón “Simular”.

### 3. Visualizar simulación y reportes

- Después de simular, verás instrucciones por tiempo y estadísticas para cada dron.
- Opciones disponibles:
  - Ver reporte detallado (botón correspondiente).
  - Generar archivo de salida XML con resultados.
  - Ver grafo de estructuras de datos (estado de TDAs).

### 4. Analizar estado en un tiempo específico (“t”)

- Ingresa un valor de tiempo en segundos en el campo correspondiente y presiona el botón “Ver estado”.
- Se mostrará el estado de los drones y las instrucciones ejecutadas hasta ese tiempo.

### 5. Ayuda y documentación

- Haz clic en el botón “Ayuda” para ver información sobre el uso, datos del estudiante y enlace a la documentación online.

---

## Consejos de Uso

- Verifica que tu archivo XML siga la estructura requerida.
- Puedes probar diferentes planes de riego y comparar resultados.
- Consulta el apartado de ayuda ante cualquier duda.

---

## Solución de Problemas

- Si la carga del archivo falla, asegúrate de que el XML tenga la estructura y datos correctos.
- En caso de errores inesperados, recarga la página y repite el proceso.
- Para soporte adicional, revisa la ayuda o la documentación enlazada.

---

## Contacto

Desarrollado por Mynor Cifuentes.
Para más información, consulta la [documentación en GitHub](https://github.com/MynorCifuentes/IPC2_Proyecto2_201318644).
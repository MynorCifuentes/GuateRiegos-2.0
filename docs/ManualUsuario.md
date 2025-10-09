# Manual de Usuario – GuateRiegos 2.0



## Introducción

GuateRiegos 2.0 es una aplicación web diseñada para simular y analizar el proceso automatizado de riego y fertilización en invernaderos usando drones.


## Requisitos Previos

- Navegador web moderno (Chrome, Firefox, Edge, etc.).
- Archivo XML de configuración válido, estructurado según el formato del sistema.
- Acceso a la URL de la aplicación (ejemplo: http://localhost:5000).



## 1. Pantalla Principal y Carga de Archivo XML

Al ingresar a la aplicación, verás la pantalla principal con el botón para cargar el archivo de configuración XML.

![alt text](/imagenes/image-5.png)  
*Pantalla principal mostrando el botón de carga de archivo XML y la lista de invernaderos cargados.*



## 2. Selección de Invernadero

Tras cargar el archivo, la aplicación muestra la lista de invernaderos disponibles. Haz clic en el nombre de un invernadero para ver sus detalles.

![alt text](/imagenes/image-6.png)    
*Vista de los invernaderos listados y selección de uno para simular.*



## 3. Detalles del Invernadero y Selección de Plan de Riego

En pantalla verás los datos básicos del invernadero: número de hileras, plantas por hilera, lista de plantas y los planes de riego disponibles. Selecciona un plan y presiona "Simular".



## 4. Simulación del Proceso

Al simular, se muestran los siguientes resultados:

- Estadísticas por dron: litros de agua y gramos de fertilizante utilizados.
- Tabla de instrucciones por tiempo para cada dron.
- Botones para ver el reporte detallado, generar archivo XML de salida y ver el grafo de estructuras en tiempo t.

![alt text](/imagenes/image-7.png)   
*Resultados de la simulación: estadísticas, tabla de instrucciones y opciones avanzadas.*



## 5. Visualización de Reporte Detallado

Al hacer clic en “Ver reporte detallado”, accedes a un informe con tablas de eficiencia de drones y las instrucciones ejecutadas. Este reporte puede descargarse o visualizarse en HTML.



## 6. Generación de Archivo XML de Resultados

Mediante el botón correspondiente, puedes generar y descargar el archivo de salida XML con todos los resultados de la simulación.



## 7. Análisis en Tiempo Específico “t” y Grafo de Estructuras

En la sección de simulación puedes definir un valor "t" (segundos) para ver el estado de los drones y las instrucciones ejecutadas hasta ese momento. Además, en la opción "Ver grafo de TDAs" se muestra la estructura de datos interna del sistema en ese instante, ideal para análisis y depuración.



## 8. Ayuda y Documentación

Haz clic en “Ayuda” para acceder a información sobre el uso, datos del estudiante y enlace a la documentación del proyecto.



## 9. Sugerencias de Buenas Prácticas

- Verifica que el archivo XML cumpla el formato requerido antes de cargarlo.
- Realiza simulaciones con diferentes planes de riego para comparar resultados.
- Utiliza el análisis en tiempo “t” para entender el comportamiento de los drones durante la simulación.
- Consulta los reportes y grafos para identificar oportunidades de optimización.



## 10. Solución de Problemas

- Si la carga del archivo falla, revisa la estructura y los datos del XML.
- En caso de errores inesperados, recarga la página y repite el proceso.
- Consulta los mensajes en la interfaz para identificar el tipo de error y tomar acciones correctivas.


## Contacto y Soporte

Desarrollado por Mynor Cifuentes.  
Para soporte adicional y sugerencias, consulta la [documentación online en GitHub](https://github.com/MynorCifuentes/IPC2_Proyecto2_201318644).

Para reportar errores o sugerencias puedes hacerlos a través de los issues del repositorio:
[Issues GuateRiegos 2.0](https://github.com/MynorCifuentes/IPC2_Proyecto2_201318644/issues).


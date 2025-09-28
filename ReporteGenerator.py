from Estructuras.ListaSimple import ListaSimple
from Estructuras.NodoCelda import NodoCelda

class ReporteGenerator:
    def __init__(self):
        self.template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Reporte de Invernaderos</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                table { border-collapse: collapse; width: 100%; margin: 10px 0; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f4f4f4; }
                .invernadero { margin-bottom: 30px; }
                .plan { margin-bottom: 20px; }
                .estadisticas { margin: 20px 0; }
            </style>
        </head>
        <body>
        """

    def generar_reporte(self, datos_invernaderos: ListaSimple) -> str:
        contenido = self.template
        
        actual_inv = datos_invernaderos.primero
        while actual_inv:
            inv_data = actual_inv.info
            contenido += f'<div class="invernadero">\n'
            contenido += f'<h2>{inv_data["nombre"]}</h2>\n'
            
            actual_plan = inv_data["planes"].primero
            while actual_plan:
                plan_data = actual_plan.info
                contenido += self._generar_seccion_plan(plan_data)
                actual_plan = actual_plan.siguiente
            
            contenido += '</div>\n'
            actual_inv = actual_inv.siguiente
        
        contenido += '</body></html>'
        
        # Guardar el reporte
        ruta_archivo = 'ReporteInvernaderos.html'
        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            f.write(contenido)
        
        return ruta_archivo

    def _generar_seccion_plan(self, plan_data):
        contenido = f'<div class="plan">\n'
        contenido += f'<h3>Plan: {plan_data["nombre"]}</h3>\n'
        
        # Tabla de asignaciones
        contenido += '<h4>Asignación de Drones</h4>\n'
        contenido += '<table>\n<tr><th>Hilera</th><th>Dron</th></tr>\n'
        
        actual_asig = plan_data["asignaciones"].primero
        while actual_asig:
            asig = actual_asig.info
            contenido += f'<tr><td>{asig["hilera"]}</td><td>{asig["dron"]}</td></tr>\n'
            actual_asig = actual_asig.siguiente
        contenido += '</table>\n'
        
        # Instrucciones
        contenido += '<h4>Instrucciones por Tiempo</h4>\n'
        contenido += '<pre>\n'
        actual_inst = plan_data["instrucciones"].primero
        while actual_inst:
            contenido += f'{actual_inst.info}\n'
            actual_inst = actual_inst.siguiente
        contenido += '</pre>\n'
        
        # Estadísticas
        contenido += '<div class="estadisticas">\n'
        contenido += f'<h4>Tiempo óptimo: {plan_data["tiempo_optimo"]} segundos</h4>\n'
        contenido += '<h5>Consumo por Dron:</h5>\n<ul>\n'
        
        actual_est = plan_data["estadisticas"].primero
        while actual_est:
            est = actual_est.info
            contenido += f'<li>{est["dron"]}: {est["agua"]}L agua, {est["fertilizante"]}g fertilizante</li>\n'
            actual_est = actual_est.siguiente
        contenido += '</ul>\n</div>\n'
        
        contenido += '</div>\n'
        return contenido
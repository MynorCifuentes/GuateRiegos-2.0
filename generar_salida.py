def generar_salida_xml(gestor, nombre_archivo="salida.xml"):
    from SimuladorRiego import SimuladorRiego

    def escape(s):
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    xml = '<?xml version="1.0" encoding="UTF-8" ?>\n<datosSalida>\n    <listaInvernaderos>\n'
    actual_inv = gestor.invernaderos.primero
    while actual_inv:
        invernadero = actual_inv.dato
        xml += f'        <invernadero nombre="{escape(invernadero.nombre)}">\n'
        actual_plan = invernadero.planes_riego.primero
        while actual_plan:
            plan = actual_plan.dato
            simulador = SimuladorRiego(invernadero, plan)
            simulador.simular()
            xml += f'            <plan nombre="{escape(plan.nombre)}">\n'
            xml += f'                <tiempoOptimoSegundos>{simulador.tiempo_total}</tiempoOptimoSegundos>\n'

            # Suma de litros y gramos de todos los drones
            total_agua = 0
            total_fertilizante = 0
            actual_est = simulador.get_estadisticas().primero
            while actual_est:
                total_agua += actual_est.dato.litros_agua
                total_fertilizante += actual_est.dato.gramos_fertilizante
                actual_est = actual_est.siguiente
            xml += f'                <aguaRequeridaLitros>{total_agua}</aguaRequeridaLitros>\n'
            xml += f'                <fertilizanteRequeridoGramos>{total_fertilizante}</fertilizanteRequeridoGramos>\n'

            # Eficiencia de drones
            xml += '                <eficienciaDronesRegadores>\n'
            actual_est = simulador.get_estadisticas().primero
            while actual_est:
                est = actual_est.dato
                xml += f'                    <dron nombre="{escape(est.dron_id)}" litrosAgua="{est.litros_agua}" gramosFertilizante="{est.gramos_fertilizante}" />\n'
                actual_est = actual_est.siguiente
            xml += '                </eficienciaDronesRegadores>\n'

            # Instrucciones por tiempo: SOLO DRONES ACTIVOS EN CADA TIEMPO
            xml += '                <instrucciones>\n'
            actual_tiempo = simulador.instrucciones_por_tiempo.primero
            t = 1
            while actual_tiempo:
                fila = actual_tiempo.dato
                actual_accion = fila.primero
                hay_accion = False
                # Primer barrido: verificar si al menos un dron tiene acción distinta de "Esperar" o está en "Fin"
                tmp_accion = fila.primero
                while tmp_accion:
                    _, accion = tmp_accion.dato
                    accion_norm = accion.strip().lower()
                    if accion_norm != "esperar" and accion_norm != "":
                        hay_accion = True
                        break
                    tmp_accion = tmp_accion.siguiente
                if hay_accion:
                    xml += f'                    <tiempo segundos="{t}">\n'
                    actual_accion = fila.primero
                    while actual_accion:
                        dron_id, accion = actual_accion.dato
                        accion_norm = accion.strip().lower()
                        if accion_norm != "esperar" and accion_norm != "":
                            # Normaliza cualquier variante de "fin"
                            if accion_norm == "fin":
                                accion_xml = "Fin"
                            else:
                                accion_xml = accion
                            xml += f'                        <dron nombre="{escape(dron_id)}" accion="{escape(accion_xml)}" />\n'
                        actual_accion = actual_accion.siguiente
                    xml += f'                    </tiempo>\n'
                actual_tiempo = actual_tiempo.siguiente
                t += 1
            xml += '                </instrucciones>\n'
            xml += '            </plan>\n'
            actual_plan = actual_plan.siguiente
        xml += '        </invernadero>\n'
        actual_inv = actual_inv.siguiente
    xml += '    </listaInvernaderos>\n</datosSalida>\n'
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write(xml)
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from Gestor import Gestor
from SimuladorRiego import SimuladorRiego
from Estructuras.ListaSimple import ListaSimple
from Estructuras.NodoCelda import NodoCelda
import os

app = Flask(__name__)
app.secret_key = "secret_key_123"

gestor = None
cargado = False

def contar_nodos(lista):
    """Cuenta los nodos en una lista."""
    contador = 0
    actual = lista.primero
    while actual:
        contador += 1
        actual = actual.siguiente
    return contador

@app.route("/")
def index():
    return render_template("index.html", cargado=cargado)

@app.route("/ayuda")
def ayuda():
    return render_template("ayuda.html")

@app.route("/cargar", methods=["GET", "POST"])
def cargar():
    global gestor, cargado
    mensaje = ""
    
    if request.method == "POST":
        if "archivo" not in request.files:
            flash("No se seleccionó ningún archivo", "error")
            return redirect(request.url)
            
        archivo = request.files["archivo"]
        if archivo.filename == "":
            flash("No se seleccionó ningún archivo", "error")
            return redirect(request.url)
            
        if archivo and archivo.filename.endswith('.xml'):
            gestor = Gestor()
            ruta_guardado = os.path.join(os.getcwd(), "entrada.xml")
            archivo.save(ruta_guardado)
            ok, mensaje = gestor.leer_xml(ruta_guardado)
            cargado = ok
            if ok:
                flash("Archivo cargado exitosamente", "success")
                return redirect(url_for("simular"))
            else:
                flash(f"Error al cargar archivo: {mensaje}", "error")
    
    return render_template("cargar.html", mensaje=mensaje, cargado=cargado)

@app.route("/simular")
def simular():
    if not cargado or not gestor:
        flash("No hay datos cargados para simular", "warning")
        return redirect(url_for("index"))

    # Obtener parámetros de la URL
    selected_inv_id = request.args.get("invernadero")
    selected_plan_id = request.args.get("plan")
    
    # Crear lista de invernaderos para mostrar
    invernaderos_vista = ListaSimple()
    actual = gestor.invernaderos.primero
    if actual:
        first = actual
        seen_names = set()  # Evitar duplicados
        indice = 0
        while True:
            if actual.info.nombre not in seen_names:
                invernaderos_vista.insertar(NodoCelda((actual.info.nombre, indice)))
                seen_names.add(actual.info.nombre)
            actual = actual.siguiente
            indice += 1
            if actual == first:
                break
    
    # Si se seleccionó un invernadero
    invernadero_actual = None
    planes_vista = None
    resultado = None
    log_lista = None
    consumos_lista = None
    
    if selected_inv_id is not None and selected_inv_id != "":
        # Encontrar el invernadero seleccionado
        actual = gestor.invernaderos.primero
        for _ in range(int(selected_inv_id)):
            actual = actual.siguiente
        invernadero_actual = actual.info
        
        # Crear lista de planes para el invernadero seleccionado
        planes_vista = ListaSimple()
        plan_actual = invernadero_actual.planesRiego.primero
        indice = 0
        planes_registrados = set()  # Evitar duplicados
        while plan_actual:
            if plan_actual.info.nombre not in planes_registrados:
                planes_vista.insertar(NodoCelda((plan_actual.info.nombre, indice)))
                planes_registrados.add(plan_actual.info.nombre)
            plan_actual = plan_actual.siguiente
            indice += 1
        
        # Si se seleccionó un plan
        if selected_plan_id is not None and selected_plan_id != "":
            # Encontrar el plan seleccionado
            plan_actual = invernadero_actual.planesRiego.primero
            for _ in range(int(selected_plan_id)):
                plan_actual = plan_actual.siguiente
            
            # Simular el plan
            simulador = SimuladorRiego(gestor, invernadero_actual, plan_actual.info)
            simulador.simular()
            
            # Guardar resultados
            resultado = f"Simulación completada en {simulador.tiempo_total} segundos"
            log_lista = simulador.log
            
            # Generar lista de consumos
            consumos_lista = ListaSimple()
            asignacion = invernadero_actual.asignacionDrones.primero
            while asignacion:
                dron = simulador.buscar_dron_objeto(asignacion.info.id_dron)
                if dron:
                    info = f"Dron {dron.nombre}: {dron.agua_usada}L agua, {dron.fertilizante_usado}g fertilizante"
                    consumos_lista.insertar(NodoCelda(info))
                asignacion = asignacion.siguiente

    return render_template("simular.html",
        cargado=cargado,
        invernaderos=invernaderos_vista,
        invernaderos_len=contar_nodos(invernaderos_vista),
        planes=planes_vista,
        planes_len=contar_nodos(planes_vista) if planes_vista else 0,
        selected_invernadero=selected_inv_id,
        selected_plan=selected_plan_id,
        resultado=resultado,
        log=log_lista,
        log_len=contar_nodos(log_lista) if log_lista else 0,
        consumos=consumos_lista,
        consumos_len=contar_nodos(consumos_lista) if consumos_lista else 0
    )

@app.route("/reporte")
def reporte():
    if not cargado or not gestor:
        flash("No hay datos cargados para generar el reporte", "warning")
        return redirect(url_for("index"))

    # Generar reporte
    with open("ReporteInvernaderos.html", "w", encoding="utf-8") as f:
        f.write("<html><head><title>Reporte</title></head><body>")
        f.write("<h1>Reporte de Invernaderos</h1>")

        actual = gestor.invernaderos.primero
        if actual:
            first = actual
            while True:
                f.write(f"<h2>Invernadero: {actual.info.nombre}</h2>")
                plan_actual = actual.info.planesRiego.primero
                while plan_actual:
                    f.write(f"<h3>Plan: {plan_actual.info.nombre}</h3>")
                    plan_actual = plan_actual.siguiente
                actual = actual.siguiente
                if actual == first:
                    break
        
        f.write("</body></html>")
    
    return send_file("ReporteInvernaderos.html")

if __name__ == '__main__':
    app.run(debug=True)
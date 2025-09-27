from flask import Flask, render_template, request, redirect, url_for, flash
from Gestor import Gestor
from SimuladorRiego import SimuladorRiego
from Estructuras.ListaSimple import ListaSimple
from Estructuras.NodoCelda import NodoCelda
import os

app = Flask(__name__)
app.secret_key = "secret_key_123"  # Necesario para Flash

# Instancias globales
gestor = Gestor()
cargado = False

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/cargar", methods=["GET", "POST"])
def cargar():
    global cargado
    mensaje = ""
    if request.method == "POST":
        if "archivo" in request.files:
            archivo = request.files["archivo"]
            if archivo.filename != "":
                ruta_guardado = os.path.join(os.getcwd(), "entrada.xml")
                archivo.save(ruta_guardado)
                ok, mensaje = gestor.leer_xml(ruta_guardado)
                cargado = ok
                if ok:
                    flash("Archivo cargado y procesado correctamente.", "success")
                    return redirect(url_for("simular"))
                else:
                    flash(f"Error: {mensaje}", "danger")
    return render_template("cargar.html", mensaje=mensaje, cargado=cargado)

@app.route("/simular", methods=["GET", "POST"])
def simular():
    global cargado
    mensaje = ""
    invernaderos = None
    planes = None
    selected_invernadero = None
    selected_plan = None
    resultado = None
    log = None
    consumos = None

    if not cargado:
        mensaje = "Por favor, carga una configuración primero."
        return render_template("simular.html", mensaje=mensaje, cargado=cargado)

    # Lista de invernaderos
    invernaderos = ListaSimple()
    actual = gestor.invernaderos.primero
    idx = 0
    if actual:
        while True:
            invernaderos.insertar(NodoCelda((actual.info.nombre, idx)))
            idx += 1
            actual = actual.siguiente
            if actual == gestor.invernaderos.primero:
                break

    # Selección de invernadero y plan
    idx_inv = request.args.get("invernadero")
    idx_plan = request.args.get("plan")
    if idx_inv is not None and idx_inv != "":
        idx_inv = int(idx_inv)
        actual = gestor.invernaderos.primero
        for _ in range(idx_inv):
            actual = actual.siguiente
        selected_invernadero = actual

        # Lista de planes
        planes = ListaSimple()
        actual_plan = selected_invernadero.info.planesRiego.primero
        idx_p = 0
        while actual_plan:
            planes.insertar(NodoCelda((actual_plan.info.nombre, idx_p)))
            idx_p += 1
            actual_plan = actual_plan.siguiente

        if idx_plan is not None and idx_plan != "":
            idx_plan = int(idx_plan)
            actual_plan = selected_invernadero.info.planesRiego.primero
            for _ in range(idx_plan):
                actual_plan = actual_plan.siguiente
            selected_plan = actual_plan

            simulador = SimuladorRiego(gestor, selected_invernadero.info, selected_plan.info)
            simulador.simular()
            resultado = simulador.resumen()
            log = simulador.obtener_log()
            consumos = simulador.obtener_consumo()

    return render_template(
        "simular.html",
        mensaje=mensaje,
        cargado=cargado,
        invernaderos=invernaderos,
        planes=planes,
        selected_invernadero=idx_inv,
        selected_plan=idx_plan,
        resultado=resultado,
        log=log,
        consumos=consumos
    )

@app.route("/reporte")
def reporte():
    return render_template("reporte.html")

@app.route("/ayuda")
def ayuda():
    return render_template("ayuda.html")

if __name__ == "__main__":
    app.run(debug=True)
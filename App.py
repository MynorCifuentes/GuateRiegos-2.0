from flask import Flask, render_template, request, redirect, url_for, flash
from Gestor import Gestor
from SimuladorRiego import SimuladorRiego
from Estructuras.ListaSimple import ListaSimple
from Estructuras.NodoCelda import NodoCelda
import os

app = Flask(__name__)
app.secret_key = "secret_key_123"

gestor = Gestor()
cargado = False

def longitud_lista_simple(lista: ListaSimple) -> int:
    """Cuenta nodos en una ListaSimple (termina cuando siguiente es None)."""
    count = 0
    actual = getattr(lista, "primero", None)
    while actual:
        count += 1
        actual = actual.siguiente
    return count

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
    invernaderos_len = 0
    planes = None
    planes_len = 0
    selected_invernadero = None
    selected_plan = None
    resultado = None
    log = None
    log_len = 0
    consumos = None
    consumos_len = 0

    if not cargado:
        mensaje = "Por favor, carga una configuración primero."
        return render_template("simular.html", mensaje=mensaje, cargado=cargado)

    # Construir una ListaSimple (lineal) de (nombre, índice) para la vista
    invernaderos = ListaSimple()
    actual_circ = gestor.invernaderos.primero
    idx = 0
    if actual_circ:
        first = actual_circ
        while True:
            invernaderos.insertar(NodoCelda((actual_circ.info.nombre, idx)))
            idx += 1
            actual_circ = actual_circ.siguiente
            if actual_circ == first:
                break
    invernaderos_len = longitud_lista_simple(invernaderos)

    # Selección de invernadero/plan
    idx_inv = request.args.get("invernadero")
    idx_plan = request.args.get("plan")

    if idx_inv is not None and idx_inv != "":
        idx_inv = int(idx_inv)
        # Navegar en la lista circular original del gestor según índice
        actual_circ = gestor.invernaderos.primero
        for _ in range(idx_inv):
            actual_circ = actual_circ.siguiente
        selected_invernadero = actual_circ

        # Construir ListaSimple lineal de planes del invernadero seleccionado
        planes = ListaSimple()
        actual_plan = selected_invernadero.info.planesRiego.primero
        pidx = 0
        while actual_plan:
            planes.insertar(NodoCelda((actual_plan.info.nombre, pidx)))
            pidx += 1
            actual_plan = actual_plan.siguiente
        planes_len = longitud_lista_simple(planes)

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
            log_len = longitud_lista_simple(log)
            consumos_len = longitud_lista_simple(consumos)

    return render_template(
        "simular.html",
        mensaje=mensaje,
        cargado=cargado,
        invernaderos=invernaderos,
        invernaderos_len=invernaderos_len,
        planes=planes,
        planes_len=planes_len,
        selected_invernadero=request.args.get("invernadero"),
        selected_plan=request.args.get("plan"),
        resultado=resultado,
        log=log,
        log_len=log_len,
        consumos=consumos,
        consumos_len=consumos_len
    )

@app.route("/reporte")
def reporte():
    return render_template("reporte.html")

@app.route("/ayuda")
def ayuda():
    return render_template("ayuda.html")

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for
from Gestor import Gestor
from SimuladorRiego import SimuladorRiego
from Estructuras.ListaSimple import ListaSimple
from Estructuras.NodoCelda import NodoCelda

app = Flask(__name__)
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
                archivo.save("entrada.xml")
                ok, mensaje = gestor.leer_xml("entrada.xml")
                cargado = ok
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

    # Construir lista de invernaderos
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

    # Selección de invernadero
    idx_inv = request.args.get("invernadero")
    idx_plan = request.args.get("plan")
    if idx_inv is not None:
        idx_inv = int(idx_inv)
        actual = gestor.invernaderos.primero
        for _ in range(idx_inv):
            actual = actual.siguiente
        selected_invernadero = actual

        # Construir lista de planes
        planes = ListaSimple()
        actual_plan = selected_invernadero.info.planesRiego.primero
        idx_p = 0
        while actual_plan:
            planes.insertar(NodoCelda((actual_plan.info.nombre, idx_p)))
            idx_p += 1
            actual_plan = actual_plan.siguiente

        if idx_plan is not None:
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
    # Solo indicado sin implementacion
    return render_template("reporte.html")

@app.route("/ayuda")
def ayuda():
    return render_template("ayuda.html")

if __name__ == "__main__":
    app.run(debug=True)
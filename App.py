import os
from flask import Flask, render_template, redirect, url_for, request, flash
from werkzeug.utils import secure_filename
from Gestor import Gestor
from SimuladorRiego import SimuladorRiego

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xml'}

app = Flask(__name__)
app.secret_key = 'guateriegos-secret'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
DEFAULT_XML = 'entrada.xml'
GESTOR = Gestor(DEFAULT_XML)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    global GESTOR
    if request.method == 'POST':
        if 'archivo_xml' not in request.files:
            flash('No se seleccionó ningún archivo.', 'danger')
            return redirect(request.url)
        file = request.files['archivo_xml']
        if file.filename == '':
            flash('No se seleccionó ningún archivo.', 'danger')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            GESTOR = Gestor(path)
            flash(f'Archivo "{filename}" cargado con éxito.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Solo se permiten archivos XML.', 'danger')
            return redirect(request.url)

    # NO listas nativas, solo ListaSimple
    invernaderos = GESTOR.invernaderos
    return render_template('index.html', invernaderos=invernaderos)

@app.route('/invernadero/<nombre>', methods=['GET', 'POST'])
def detalle_invernadero(nombre):
    actual = GESTOR.invernaderos.primero
    invernadero = None
    while actual:
        if actual.dato.nombre == nombre:
            invernadero = actual.dato
            break
        actual = actual.siguiente
    if not invernadero:
        flash('Invernadero no encontrado.', 'danger')
        return redirect(url_for('index'))

    plan_seleccionado = None
    if request.method == 'POST':
        plan_nombre = request.form.get("plan_seleccionado")
        actual_plan = invernadero.planes_riego.primero
        while actual_plan:
            if actual_plan.dato.nombre == plan_nombre:
                plan_seleccionado = actual_plan.dato
                break
            actual_plan = actual_plan.siguiente
        if plan_seleccionado:
            return redirect(url_for('simular', nombre_invernadero=nombre, nombre_plan=plan_nombre))

    return render_template('invernadero.html', invernadero=invernadero)

@app.route('/simular/<nombre_invernadero>/<nombre_plan>')
def simular(nombre_invernadero, nombre_plan):
    actual = GESTOR.invernaderos.primero
    invernadero = None
    while actual:
        if actual.dato.nombre == nombre_invernadero:
            invernadero = actual.dato
            break
        actual = actual.siguiente
    if not invernadero:
        flash('Invernadero no encontrado.', 'danger')
        return redirect(url_for('index'))

    actual_plan = invernadero.planes_riego.primero
    plan = None
    while actual_plan:
        if actual_plan.dato.nombre == nombre_plan:
            plan = actual_plan.dato
            break
        actual_plan = actual_plan.siguiente
    if not plan:
        flash('Plan de riego no encontrado.', 'danger')
        return redirect(url_for('detalle_invernadero', nombre=nombre_invernadero))

    simulador = SimuladorRiego(invernadero, plan)
    simulador.simular()
    instrucciones = simulador.get_instrucciones()     # ListaSimple de ListaSimple de (dron_id, accion)
    estadisticas = simulador.get_estadisticas()       # ListaSimple de EstadisticaDron
    tiempo_total = simulador.tiempo_total

    # PASAMOS SOLO ListaSimple's, NUNCA listas nativas
    return render_template('simulacion.html',
                           invernadero=invernadero,
                           plan=plan,
                           instrucciones=instrucciones,
                           estadisticas=estadisticas,
                           tiempo_total=tiempo_total)

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, request, render_template, redirect, url_for, flash
from Gestor import Gestor
import os

app = Flask(__name__)
app.secret_key = 'super-secret-key'  # Necesario para mensajes flash

gestor = Gestor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cargar', methods=['GET', 'POST'])
def cargar():
    
    if request.method == 'POST':
        archivo = request.files.get('archivo')
        if not archivo:
            flash('No se recibió el archivo', 'danger')
            return redirect(url_for('cargar'))
        ruta = os.path.join('./', archivo.filename)
        archivo.save(ruta)
        exito, mensaje = gestor.leer_xml(ruta)[:2]
        if exito:
            flash(mensaje, 'success')
        else:
            flash(mensaje, 'danger')
        return redirect(url_for('cargar'))
    return render_template('cargar.html')

@app.route('/simular')
def simular():
    return render_template('simular.html')

@app.route('/reporte')
def reporte():
    return render_template('reporte.html')

@app.route('/ayuda')
def ayuda():
    return render_template('ayuda.html')

@app.route('/mostrar-drones', methods=['GET'])
def mostrar_drones():
    import io, sys
    buffer = io.StringIO()
    sys.stdout = buffer
    gestor.mostrar_drones()
    sys.stdout = sys.__stdout__
    return buffer.getvalue(), 200

@app.route('/mostrar-invernaderos', methods=['GET'])
def mostrar_invernaderos():
    import io, sys
    buffer = io.StringIO()
    sys.stdout = buffer
    gestor.mostrar_invernaderos()
    sys.stdout = sys.__stdout__
    return buffer.getvalue(), 200

@app.route('/mostrar-plantas-por-hilera/<int:idx>', methods=['GET'])
def mostrar_plantas_por_hilera(idx):
    import io, sys
    buffer = io.StringIO()
    sys.stdout = buffer
    actual = gestor.invernaderos.primero
    contador = 0
    encontrado = None
    if actual:
        while True:
            if contador == idx:
                encontrado = actual
                break
            actual = actual.siguiente
            contador += 1
            if actual == gestor.invernaderos.primero:
                break
    if encontrado:
        gestor.mostrar_plantas_por_hilera(encontrado)
    else:
        print("No existe ese invernadero")
    sys.stdout = sys.__stdout__
    return buffer.getvalue(), 200

if __name__ == '__main__':
    app.run(debug=True)
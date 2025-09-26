from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cargar', methods=['GET', 'POST'])
def cargar():
    if request.method == 'POST':
        archivo = request.files['archivo']
        if archivo:
            # Procesa el archivo aquí
            flash('Archivo cargado correctamente')
            return redirect(url_for('index'))
    return render_template('cargar.html')

@app.route('/simular', methods=['GET', 'POST'])
def simular():
    # Aquí agregas la lógica para seleccionar invernadero, plan y simular
    return render_template('simular.html')

@app.route('/reporte')
def reporte():
    # Genera y muestra el reporte HTML
    return render_template('reporte.html')

@app.route('/ayuda')
def ayuda():
    # Muestra información del estudiante y documentación
    return render_template('ayuda.html')

if __name__ == '__main__':
    app.run(debug=True)
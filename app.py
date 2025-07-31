from flask import Flask, render_template, request, send_file, redirect, url_for, session, jsonify
from werkzeug.utils import secure_filename
import os, zipfile
from datetime import datetime
from config import USUARIOS, RUTA_COMPARTIDA
from utilidades.explorar_archivos import obtener_listado_archivos

app = Flask(__name__)
app.secret_key = 'kairos123'

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']
        if usuario in USUARIOS and USUARIOS[usuario]['password'] == contrasena:
            session['usuario'] = usuario
            session['es_admin'] = USUARIOS[usuario]['admin']
            return redirect(url_for('index'))
        return render_template('login.html', error='Credenciales inválidas')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/inicio')
def index():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', usuario=session['usuario'], es_admin=session['es_admin'])

@app.route('/api/archivos')
def api_archivos():
    archivos = obtener_listado_archivos()
    return jsonify(archivos)

@app.route('/descargar/<path:filename>')
def descargar(filename):
    ruta_archivo = os.path.join(RUTA_COMPARTIDA, filename)
    return send_file(ruta_archivo, as_attachment=True)

@app.route('/descargar_masivo', methods=['POST'])
def descargar_masivo():
    seleccionados = request.json.get('archivos', [])
    zip_path = "/mnt/data/descarga_kairos.zip"
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for archivo in seleccionados:
            ruta = os.path.join(RUTA_COMPARTIDA, archivo)
            if os.path.isfile(ruta):
                zipf.write(ruta, os.path.basename(ruta))
    return send_file(zip_path, as_attachment=True)

@app.route('/subir', methods=['POST'])
def subir():
    if not session.get('es_admin'):
        return "No autorizado", 403
    if 'archivo' not in request.files:
        return "No se envió archivo", 400
    archivo = request.files['archivo']
    if archivo.filename == '':
        return "Archivo sin nombre", 400
    filename = secure_filename(archivo.filename)
    archivo.save(os.path.join(RUTA_COMPARTIDA, filename))
    return "Archivo subido correctamente"

if __name__ == '__main__':
    app.run(debug=True)

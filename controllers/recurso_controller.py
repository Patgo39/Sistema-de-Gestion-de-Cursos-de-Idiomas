import os
from flask import Blueprint, request, redirect, flash, session, current_app, url_for, render_template
from werkzeug.utils import secure_filename
from dao.recurso_dao import RecursoDao
recursos_bp = Blueprint('recursos', __name__)

@recursos_bp.route('/subir_recurso', methods=['GET', 'POST'])
def subir_recurso():
    if 'usuario' not in session:
        return redirect(url_for('auth.iniciar_sesion'))
    if request.method == 'GET':
        return render_template('RegistroUsuarioIH.html')
        pass
    if request.method == 'POST':
        archivo = request.files.get('archivo')
        nombre_recurso = request.form.get('nombre_recurso')
        descripcion = request.form.get('descripcion')

        id_docente = session['usuario']

        if archivo and archivo.filename != '':
            filename = secure_filename(archivo.filename)
            ruta_guardado = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            archivo.save(ruta_guardado)

            RecursoDao.guardar_recurso(nombre_recurso, filename, descripcion, id_docente)
            flash('Recurso guardado con éxito', 'success')

            return redirect(url_for('auth.tablero_docente'))
        else:
            flash('Archivo no encontrado o inválido', 'danger')
            return redirect(url_for('recursos.subir_recurso'))




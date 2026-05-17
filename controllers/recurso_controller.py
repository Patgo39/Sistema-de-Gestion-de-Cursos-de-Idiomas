import os
from flask import Blueprint, request, redirect, flash, session, current_app, url_for, render_template
from werkzeug.utils import secure_filename
from dao.recurso_dao import RecursoDao
from dao.curso_dao import CursoDao

recursos_bp = Blueprint('recursos', __name__)


@recursos_bp.route('/subir_recurso/<int:id_curso>', methods=['GET', 'POST'])
def subir_recurso(id_curso):
    '''
    Metodo para subir recurso(controlador)
    Si es POST pide los datos para subir el recurso ala base de datos mediante el recurso_dao
    Si GET muestra el html para subir recurso
    :param id_curso:
    :return:
    '''
    if 'usuario' not in session:
        return redirect(url_for('auth.iniciar_sesion'))

    if request.method == 'GET':
        return render_template('SubirRecursoIH.html', id_curso=id_curso)

    if request.method == 'POST':
        archivo = request.files.get('archivo')
        nombre_formulario= request.form.get('nombre_recurso')
        descripcion_formulario = request.form.get('descripcion')

        if archivo and archivo.filename != '':
            filename = secure_filename(archivo.filename)

            if not os.path.exists(current_app.config['UPLOAD_FOLDER']):
                os.makedirs(current_app.config['UPLOAD_FOLDER'])

            ruta_guardado = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            archivo.save(ruta_guardado)

            RecursoDao.guardar_recurso(
                titulo=nombre_formulario,
                filename=filename,
                descripcion= descripcion_formulario,
                id_curso=id_curso
            )

            flash('Recurso guardado con éxito', 'success')
            return redirect(url_for('docente.tablero_docente'))
        else:
            flash('Archivo no encontrado o inválido', 'danger')
            return redirect(url_for('recursos.subir_recurso', id_curso=id_curso))
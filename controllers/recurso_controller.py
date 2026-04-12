import os
from flask import request, redirect, flash, session, current_app
from werkzeug.utils import secure_filename
from dao.recurso_dao import RecursoDao
recursos_bp = Blueprint('recursos', __name__)
@recursos_bp.route('/subir_recurso', methods=['POST'])
def subir_recurso():
    if 'id_usuario' not in session:
        return redirect('/login')
    archivo = request.files.get('archivo')
    nombre_recurso=request.form['nombre_recurso']
    descripcion = request.form['descripcion']
    id_docente=session['id_docente']
    if archivo and archivo.filename != '':
        filename=secure_filename(archivo.filename)
        ruta_guardado = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        archivo.save(ruta_guardado)
        RecursoDao.guardar_recurso(nombre_recurso, filename, descripcion, id_docente )
        flash('Recurso guardado', 'success')
    else:
        flash('Archivo no encontrado', 'danger')

    return redirect('/subir_recurso')




from flask import Blueprint, render_template, request, redirect, flash, session, url_for

from dao.curso_dao import CursoDao

alumno_bp = Blueprint('alumno', __name__)

@alumno_bp.route('/tablero_alumno', methods=['GET'])
def tablero_alumno():
    '''
    Muestra el tablero de alumno con base en su username y id de usuario
    :return: redirect del tablero de alumno con base de su username y id de usuario
    '''
    if 'username' not in session or session.get('rol').lower() != 'alumno':
        flash("Acceso denegado. Debes iniciar sesión como alumno.")
        return redirect(url_for('auth.iniciar_sesion'))

    nombre = session.get('username')
    id_usuario = session.get('usuario')
    cursos_inscritos=CursoDao.obtener_cursos_por_alumno(id_usuario)
    return render_template('alumno/tablero_alumno.html', nombre=nombre, cursos=cursos_inscritos)

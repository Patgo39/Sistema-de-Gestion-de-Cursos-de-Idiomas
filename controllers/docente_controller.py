from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from dao.curso_dao import CursoDao
docente_bp = Blueprint('docente', __name__)


@docente_bp.route('/tablero_docente')
def tablero_docente():
    if 'username' not in session or session.get('rol').lower() != 'docente':
        flash("Acceso denegado. Debes iniciar sesión como docente.")
        return redirect(url_for('auth.iniciar_sesion'))

    nombre = session.get('username')
    id_usuario=session.get('usuario')
    mis_cursos=CursoDao.obtener_cursos_por_docente(id_usuario)
    return render_template('docente/tablero_docente.html', nombre=nombre, cursos=mis_cursos)

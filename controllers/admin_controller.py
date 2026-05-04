from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from dao.alumno_dao import AlumnoDao
from dao.docente_dao import DocenteDao

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/tablero_admin', methods=['GET'])
def tablero_administrador():

    nombre = session.get('username')

    if not nombre:
        flash("Por favor, inicia sesión primero")
        return redirect(url_for('auth.iniciar_sesion'))
    return f"Bienvenido {nombre}"

@admin_bp.route('/gestionar_docentes', methods=['GET'])
def gestionar_docentes():
    pass

@admin_bp.route('/gestionar_alumnos', methods=['GET'])
def gestionar_alumnos():
    pass
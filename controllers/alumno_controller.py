from flask import Blueprint, render_template, request, redirect, flash, session, url_for

alumno_bp = Blueprint('alumno', __name__)

@alumno_bp.route('/tablero_alumno', methods=['GET'])
def tablero_alumno():


    nombre = session.get('username')

    if not nombre:
        flash("Por favor, inicia sesión primero")
        return redirect(url_for('auth.iniciar_sesion'))
    return f"Bienvenido {nombre}"

from flask import Blueprint, render_template, request, redirect, flash, session, url_for

docente_bp = Blueprint('docente', __name__)


@docente_bp.route('/tablero_docente')
def tablero_docente():
    nombre = session.get('username')

    if not nombre:
        flash("Por favor, inicia sesión primero")
        return redirect(url_for('auth.iniciar_sesion'))
    return f"Bienvenido {nombre}"
from flask import Blueprint, render_template, request, redirect, flash, session, url_for

admin_bp = Blueprint('administrador', __name__)


@admin_bp.route('/tablero_administrador', methods=['GET'])
def tablero_admin():
    if 'username' not in session or session.get('rol').lower() not in ['admin', 'administrador']:
        flash("Acceso denegado. No tienes permisos de administrador.")
        return redirect(url_for('auth.iniciar_sesion'))

    nombre = session.get('username')
    return render_template('admin/tablero_admin.html', nombre=nombre)
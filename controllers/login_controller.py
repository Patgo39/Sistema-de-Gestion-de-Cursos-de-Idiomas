from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from dao.usuario_dao import UsuarioDao
login_bp = Blueprint('auth', __name__)

@login_bp.route('/login', methods=['GET', 'POST'])
def iniciar_sesion():
    '''
    Metodo para inicar sesion de usuario (controlador)
    Si es POST  pide los datos para iniciar sesion de usuario
    Si es GET muestra la pagina de iniciar sesion
    :return:
    '''
    if request.method == 'GET':
        return render_template('auth/LoginIH.html')

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        usuario_valido = UsuarioDao.verificar_login(username, password)

        if usuario_valido:

            session['usuario'] = usuario_valido.id_usuario
            session['username'] = usuario_valido.username
            session['rol'] = usuario_valido.rol
            rol_validar = usuario_valido.rol.lower()

            if rol_validar == 'alumno':
                return redirect(url_for('alumno.tablero_alumno'))
            elif rol_validar == 'docente':
                return redirect(url_for('docente.tablero_docente'))
            elif rol_validar == 'administrador':
                return redirect(url_for('admin.tablero_administrador'))
        else:
            flash("Usuario o contraseñas incorrectos. Intenta de nuevo")
            return redirect(url_for('auth.iniciar_sesion'))
@login_bp.route('/logout')
def cerrar_sesion():
    '''
    Metodo para cerrar sesion de usuario (controlador)
    :return: redirect para cerrar sesion de usuario (controlador)
    '''
    session.clear()
    flash("Has cerrado sesión exitosamente.", 'success')
    return redirect(url_for('auth.iniciar_sesion'))


@login_bp.route('/logout')
def cerrar_sesion():
    '''
    Metodo para cerrar sesion de usuario (controlador)
    :return: redirect para cerrar sesion de usuario (controlador)
    '''
    session.clear()
    flash("Has cerrado sesión exitosamente.", 'success')
    return redirect(url_for('auth.iniciar_sesion'))

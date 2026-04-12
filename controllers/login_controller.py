from flask import Blueprint, render_template, request, redirect, flash, session
from dao.usuario_dao import UsuarioDao
login_bp = Blueprint('login', __name__)
@login_bp.route('/login', methods=['GET', 'POST'])
def iniciar_sesion():
    if request.method == 'GET':
        return render_template('LoginIH.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        usuario_valido=UsuarioDao.verificar_login(username,password)
        if usuario_valido:
            session['usuario'] = usuario_valido.id_usuario
            session['username'] = usuario_valido.username
            session['rol']=usuario_valido.rol

            if usuario_valido.rol == 'alumno':
                return redirect('/tablero_alumno')
            elif usuario_valido.rol == 'docente':
                return redirect('/tablero_docente')
        else:
            flash("Usuario o contraseñas incorrectos. Intenta de nuevo")
            return redirect('/login')

@login_bp.route('/tablero_alumno')
def tablero_alumno():
    return f"Bienvenido {session['username']}"
@login_bp.route('/tablero_docente')
def tablero_docente():
    return f"Bienvenido {session['username']}"


from flask import Blueprint, render_template, request, redirect, flash
from dao.usuario_dao import UsuarioDao
registro_bp = Blueprint('registro', __name__)
@registro_bp.route('/registro', methods=['GET', 'POST'])
def registrar_usuario():
    if request.method == 'GET':
        return render_template('RegistroUsuarioIH.html')
    if request.method == 'POST':
        username=request.form.get('username')
        nombre=request.form.get('nombre')
        apellido_paterno=request.form.get('apellido_paterno')
        apellido_materno=request.form.get('apellido_materno')
        email=request.form.get('email')
        fecha_nacimiento=request.form.get('fecha_nacimiento')
        password=request.form.get('password')
        genero=request.form.get('genero')
        pais=request.form.get('pais')
        rol=request.form.get('rol')

        if rol=='docente':
            tiempo_experiencia=request.form.get('tiempo_experiencia')
            especialidad=request.form.get('especialidad')
            exito= UsuarioDao.registrar_docente(
                username=username,
                nombre=nombre,
                apellido_paterno=apellido_paterno,
                apellido_materno=apellido_materno,
                email=email,
                fecha_nacimiento=fecha_nacimiento,
                password=password,
                genero=genero,
                pais=pais,
                tiempo_experiencia=tiempo_experiencia,
                especialidad=especialidad
            )

            if exito:
                flash('Usuario registrado exitosamente')
            else:
                flash("Error al registrar docente")
                return redirect('/registro')

        elif rol=='alumno':
            grado_actual=request.form.get('grado_actual')
            exito=UsuarioDao.registrar_alumno(
                username=username,
                nombre=nombre,
                apellido_paterno=apellido_paterno,
                apellido_materno=apellido_materno,
                email=email,
                fecha_nacimiento=fecha_nacimiento,
                password=password,
                genero=genero,
                pais=pais,
                grado_actual=grado_actual
            )
            if exito:
                flash('Usuario registrado exitosamente')
            else:
                flash("Error al registrar alumno")
                return redirect('/registro')
        return redirect('/login')


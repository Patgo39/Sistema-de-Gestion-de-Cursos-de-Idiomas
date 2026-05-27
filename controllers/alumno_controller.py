from flask import Blueprint, render_template, request, redirect, flash, session, url_for

from dao.alumno_dao import AlumnoDao
from dao.curso_dao import CursoDao
from dao.inscribir_dao import InscribirDao
from dao.usuario_dao import UsuarioDao
from dao.recurso_dao import RecursoDao
from models.dominar import Dominar
from dao.docente_dao import DocenteDao

from dao.curso_dao import CursoDao
from flask import request

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

    usuario = UsuarioDao.buscar_por_username(session.get('username'))
    nombre = usuario.nombre if usuario else 'Alumno'
    id_usuario = session.get('usuario')
    cursos_inscritos = CursoDao.obtener_cursos_por_alumno(id_usuario)

    AlumnoDao.actualizar_ultimo_acceso(id_usuario)

    return render_template('alumno/tablero_alumno.html', nombre=nombre, cursos=cursos_inscritos)


@alumno_bp.route('/mis_cursos', methods=['GET'])
def mis_cursos():
    if 'username' not in session or session.get('rol', '').lower() != 'alumno':
        flash("Por favor, inicia sesión como alumno.")
        return redirect(url_for('auth.iniciar_sesion'))

    usuario = UsuarioDao.buscar_por_username(session.get('username'))
    cursos = CursoDao.obtener_cursos_por_alumno(usuario.id_usuario) if usuario else []
    nombre_alumno = usuario.nombre if usuario else 'Alumno'
    return render_template('alumno/mis_cursos_alumno.html', cursos=cursos, role='alumno', nombre=nombre_alumno)


@alumno_bp.route('/curso/<int:id_curso>', methods=['GET'])
def curso_detalle(id_curso):
    rol = session.get('rol', '').lower()
    if 'username' not in session:
        flash("Por favor, inicia sesión primero")
        return redirect(url_for('auth.iniciar_sesion'))
    if rol != 'alumno':
        flash("Acceso denegado. Esta sección es solo para alumnos.")
        return redirect(url_for('auth.iniciar_sesion'))

    curso = CursoDao.buscar_por_id(id_curso)
    recursos = RecursoDao.obtener_por_curso(id_curso)
    if not curso:
        flash("Curso no encontrado")
        return redirect(url_for('alumno.mis_cursos'))

    return render_template('curso_detalle.html', curso=curso, recursos=recursos, role='alumno')


@alumno_bp.route('/perfil', methods=['GET', 'POST'])
def perfil():
    if 'username' not in session:
        flash("Por favor, inicia sesión.")
        return redirect(url_for('auth.iniciar_sesion'))

    usuario = UsuarioDao.buscar_por_username(session.get('username'))
    if request.method == 'POST':
        datos = {
            'nombre': request.form.get('nombre'),
            'apellido_paterno': request.form.get('apellido_paterno'),
            'apellido_materno': request.form.get('apellido_materno'),
            'email': request.form.get('email'),
            'fecha_nacimiento': request.form.get('fecha_nacimiento') or None,
            'genero': request.form.get('genero'),
            'pais': request.form.get('pais')
        }
        llaves_alumno = ["nombre", "apellido_paterno", "apellido_materno",
                         "email", "fecha_nacimiento", "genero", "pais"]
        datos_verificados = {}
        for key, value in datos.items():
            if key in llaves_alumno:
                if value is not None and value != "":
                    datos_verificados[key] = value


        try:
            AlumnoDao.actualizar_alumno(usuario.id_usuario, datos_verificados)
            flash('Perfil actualizado correctamente', 'success')
        except Exception as e:
            msg = str(e)
            flash(f"Error: {msg}", category="error")
            return redirect(url_for('alumno.perfil'))

    return render_template('perfil.html', usuario=usuario, role='alumno')


#obtiene todos los cursos menos los que ya esta inscrito
@alumno_bp.route('/tablero_alumno/cursos_disponibles', methods=['GET'])
def tablero_cursos_disponibles_alumno():
    #verificamos la session del alumno
    nombre = session.get('username')
    if not nombre:
        flash("Por favor, inicia sesion primero")
        return redirect(url_for('auth.iniciar_sesion'))

    # obtenemos al usuario desde su username
    usuario = UsuarioDao.buscar_por_username(nombre)

    # cursos disponibles menos los que ya está inscrito
    todos_los_cursos = CursoDao.obtener_cursos_disponibles()
    cursos_inscritos = CursoDao.obtener_cursos_por_alumno(usuario.id_usuario)
    ids_inscritos = {c.id_curso for c in cursos_inscritos}
    cursos_disponibles = [c for c in todos_los_cursos if c['id_curso'] not in ids_inscritos]

    return render_template('alumno/cursos_disponibles.html', cursos_disponibles=cursos_disponibles)


@alumno_bp.route('/buscar_docentes', methods=['GET'])
def listar_docentes():
    if 'username' not in session or session.get('rol', '').lower() != 'alumno':
        flash('Por favor, inicia sesión como alumno.')
        return redirect(url_for('auth.iniciar_sesion'))

    docentes = DocenteDao.buscar_docentes()
    return render_template('alumno/listar_docentes.html', docentes=docentes)


@alumno_bp.route('/docente/<int:id_docente>/perfil', methods=['GET'])
def perfil_docente_publico(id_docente):
    if 'username' not in session or session.get('rol', '').lower() != 'alumno':
        flash('Por favor, inicia sesión como alumno.')
        return redirect(url_for('auth.iniciar_sesion'))

    docente = DocenteDao.buscar_por_id(id_docente)
    if not docente:
        flash('No se encontró el perfil del docente.')
        return redirect(url_for('alumno.listar_docentes'))

    return render_template('alumno/perfil_docente.html', docente=docente, role='alumno')

#realiza la inscripcion tras verificar requerimientos
@alumno_bp.route('/tablero_alumno/cursos_disponibles/<int:id_curso>/inscripcion', methods=['POST'])
def inscripcion_curso_disponibles(id_curso):
    # verificamos la session del alumno
    nombre = session.get('username')
    if not nombre:
        flash("Por favor, inicia sesion primero")
        return redirect(url_for('auth.iniciar_sesion'))

    #obtener datos de usuario y curso
    usuario = UsuarioDao.buscar_por_username(nombre)
    curso = CursoDao.buscar_por_id(id_curso)

    if not curso:
        flash("Curso no encontrado")
        return redirect(url_for('alumno.tablero_cursos_disponibles_alumno'))

    # verificar dominio de idioma antes
    if curso.nivel == 'Básico':
        puede_inscribirse = True
    elif curso.nivel == 'Intermedio':
        dominio = Dominar.query.filter_by(
            id_usuario=usuario.id_usuario,
            id_idioma=curso.id_idioma
        ).filter(Dominar.nivel_dominio == 'Básico').first()
        puede_inscribirse = dominio is not None
    elif curso.nivel == 'Avanzado':
        dominio = Dominar.query.filter_by(
            id_usuario=usuario.id_usuario,
            id_idioma=curso.id_idioma
        ).filter(Dominar.nivel_dominio == 'Intermedio').first()
        puede_inscribirse = dominio is not None
    else:
        puede_inscribirse = True

    if not puede_inscribirse:
        flash("No cumples con los requisitos para inscribirte a este curso")
        return redirect(url_for('alumno.tablero_cursos_disponibles_alumno'))

    #inscripcion despues de verificacion exitosa
    InscribirDao.crear_inscripcion(usuario.id_usuario, id_curso)
    flash("Inscripción exitosa")
    return redirect(url_for('alumno.tablero_cursos_disponibles_alumno'))

@alumno_bp.route('/mis_cursos', methods=['GET'])
def mis_cursos_alumno():
    if 'username' not in session or session.get('rol', '').lower() != 'alumno':
        flash("Por favor, inicia sesión como alumno.")
        return redirect(url_for('auth.iniciar_sesion'))

    usuario = UsuarioDao.buscar_por_username(session['username'])
    cursos = CursoDao.obtener_cursos_por_alumno(usuario.id_usuario) if usuario else []
    return render_template('curso_lista.html', cursos=cursos, role='alumno')
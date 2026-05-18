from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from dao.curso_dao import CursoDao
from dao.inscribir_dao import InscribirDao
from dao.usuario_dao import UsuarioDao
from models.dominar import Dominar

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
    cursos_inscritos = CursoDao.obtener_cursos_por_alumno(id_usuario)
    return render_template('alumno/tablero_alumno.html', nombre=nombre, cursos=cursos_inscritos)

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

#realiza la inscripcion tras verificar requerimientos
@alumno_bp.route('/tablero_alumno/cursos_disponibles/<int:id_curso>_inscripcion', methods=['POST'])
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
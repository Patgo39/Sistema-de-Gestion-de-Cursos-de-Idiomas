from flask import Blueprint, render_template, redirect, flash, session, url_for
from dao.inscribir_dao import InscribirDao
from dao.curso_dao import CursoDao

docente_bp = Blueprint('docente', __name__)


@docente_bp.route('/tablero_docente')
def tablero_docente():
    nombre = session.get('username')

    if not nombre:
        flash("Por favor, inicia sesión primero")
        return redirect(url_for('auth.iniciar_sesion'))
    return f"Bienvenido {nombre}"

#Obtiene informacion sobre un curso: nombre, id del curso, lista de alumnos
@docente_bp.route('/tablero_docente/curso_docente/<int:id_curso>', methods=['GET'])
def curso_docente(id_curso):
    #Verificamos la session del docente
    if not session.get('username'):
        flash("Por favor, inicia sesión primero")
        return redirect(url_for('auth.iniciar_sesion'))

    #informacion general y lista de alumnos inscritos al curso
    lista_inscripcion = InscribirDao.consultar_lista_inscripcion(id_curso)
    curso = CursoDao.buscar_por_id(id_curso)

    if not curso:
        flash("Curso no encontrado")
        return redirect(url_for('docente.tablero_docente'))

    return render_template('docente/curso_informacion.html', lista_inscripcion = lista_inscripcion, curso = curso)

#Obtiene los datos de un alumno inscrito al curso
@docente_bp.route('/tablero_docente/curso_docente/<int:id_curso>/alumno/<int:id_usuario>', methods=['GET'])
def datos_alumno(id_curso, id_usuario):
    # Verificamos la session del docente
    if not session.get('username'):
        flash("Por favor, inicia sesión primero")
        return redirect(url_for('auth.iniciar_sesion'))

    #datos del alumno seleccionado
    alumno = InscribirDao.consultar_alumno_inscripcion(id_usuario, id_curso)
    curso = CursoDao.buscar_por_id(id_curso)
    if not alumno:
        flash("Alumno no encontrado en este curso")
        return redirect(url_for('docente.curso_docente', id_curso = id_curso))
    return render_template('docente/alumno_datos.html', alumno = alumno, id_usuario = id_usuario, id_curso = id_curso, curso = curso)

#Docente elimina a alumno de un curso
@docente_bp.route('/tablero_docente/curso_docente/<int:id_curso>/alumno/<int:id_alumno>/eliminar', methods=['POST'])
def eliminar_alumno(id_curso, id_alumno):
    # Verificamos la session del docente
    if not session.get('username'):
        flash("Por favor, inicia sesión primero")
        return redirect(url_for('auth.iniciar_sesion'))

    #eliminar alumno
    alumno_eliminado = InscribirDao.eliminar_inscripcion(id_alumno, id_curso)
    if alumno_eliminado:
        flash("Alumno eliminado en este curso.")
    else:
        flash("No se puedo eliminar al alumno.")

    return redirect(url_for('docente.curso_docente', id_curso = id_curso))
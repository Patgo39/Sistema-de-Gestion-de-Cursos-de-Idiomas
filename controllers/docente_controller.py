
import os
import uuid
from typing import Optional
from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from supabase import create_client, Client

from dao.docente_dao import DocenteDao
from db import db
from dao.curso_dao import CursoDao
from dao.recurso_dao import RecursoDao
from dao.inscribir_dao import InscribirDao
from dao.usuario_dao import UsuarioDao
from models.curso import Curso
from models.idioma import Idioma

docente_bp = Blueprint('docente', __name__)

# Carga segura de credenciales de Supabase desde las variables de entorno del sistema (.env)
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
BUCKET_NAME = os.environ.get("SUPABASE_BUCKET", "materiales-cursos")

# Inicialización opcional del cliente de almacenamiento.
# Evita levantar excepciones si las variables no están definidas (útil en tests/local).
supabase_client: Optional[Client] = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception:
        supabase_client = None


@docente_bp.route('/tablero_docente')
def tablero_docente():
    '''
     Muestra el tablero docente con base en su username y id de usuario
    :return: redirect de docente tablero con base en su username y id de usuario
    '''
    if 'username' not in session or session.get('rol').lower() != 'docente':
        flash("Acceso denegado. Debes iniciar sesión como docente.")
        return redirect(url_for('auth.iniciar_sesion'))

    usuario = UsuarioDao.buscar_por_username(session.get('username'))
    nombre = usuario.nombre if usuario else 'Docente'
    id_usuario = session.get('usuario')
    mis_cursos = CursoDao.obtener_cursos_por_docente(id_usuario)
    DocenteDao.actualizar_ultimo_acceso(id_usuario)
    return render_template('docente/tablero_docente.html', nombre=nombre, cursos=mis_cursos, role='docente')


@docente_bp.route('/mis_cursos', methods=['GET'])
def mis_cursos_docente():
    if 'username' not in session or session.get('rol', '').lower() != 'docente':
        flash("Acceso denegado. Debes iniciar sesión como docente.")
        return redirect(url_for('auth.iniciar_sesion'))

    usuario = UsuarioDao.buscar_por_username(session.get('username'))
    id_usuario = usuario.id_usuario if usuario else None
    cursos = CursoDao.obtener_cursos_por_docente(id_usuario) if id_usuario else []
    return render_template('curso_lista.html', cursos=cursos, role='docente')


@docente_bp.route('/perfil', methods=['GET', 'POST'])
def perfil_docente():
    if 'username' not in session:
        flash('Por favor, inicia sesión.')
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
        success = UsuarioDao.actualizar_perfil_basico(usuario.id_usuario, datos)
        if success:
            flash('Perfil actualizado correctamente', 'success')
        else:
            flash('Error al actualizar el perfil', 'error')
        return redirect(url_for('docente.perfil_docente'))

    return render_template('perfil.html', usuario=usuario, role='docente')


@docente_bp.route('/crear_curso', methods=['GET'])
def crear_curso_vista():
    if 'username' not in session or session.get('rol').lower() != 'docente':
        flash("Acceso denegado. Debes iniciar sesión como docente.")
        return redirect(url_for('auth.iniciar_sesion'))

    # Consultamos todos los idiomas existentes para poblar el <datalist>
    todos_los_idiomas = Idioma.query.all()
    return render_template('docente/crear_curso.html', idiomas=todos_los_idiomas)


@docente_bp.route('/crear_curso_procesar', methods=['POST'])
def crear_curso_procesar():
    if 'username' not in session or session.get('rol').lower() != 'docente':
        return redirect(url_for('auth.iniciar_sesion'))

    nombre_curso = request.form.get('nombre_curso')
    nivel = request.form.get('nivel')
    descripcion = request.form.get('descripcion')
    nombre_idioma_input = request.form.get('nombre_idioma')
    id_docente = session.get('usuario')

    try:
        idioma_existente = Idioma.query.filter_by(nombre_idioma=nombre_idioma_input).first()
        if idioma_existente:
            id_idioma = idioma_existente.id_idioma
        else:
            nuevo_idioma = Idioma(nombre_idioma=nombre_idioma_input)
            db.session.add(nuevo_idioma)
            db.session.commit()
            id_idioma = nuevo_idioma.id_idioma

        CursoDao.crear_curso(nombre_curso, descripcion, nivel, id_docente, id_idioma)

        flash("Curso creado con éxito.", category="success")
        return redirect(url_for('docente.tablero_docente'))

    except Exception as e:
        flash(f"Error al crear el curso: {str(e)}", category="error")
        return redirect(url_for('docente.crear_curso_vista'))


@docente_bp.route('/gestionar_curso/<int:id_curso>', methods=['GET'])
def gestionar_curso_vista(id_curso):
    if 'username' not in session or session.get('rol').lower() != 'docente':
        flash("Acceso denegado. Debes iniciar sesión como docente.")
        return redirect(url_for('auth.iniciar_sesion'))
    curso = CursoDao.buscar_por_id(id_curso)
    if not curso:
        flash("El curso solicitado no existe.", category="error")
        return redirect(url_for('docente.tablero_docente'))

    todos_los_idiomas = Idioma.query.all()

    # Obtenemos los recursos vinculados a este curso usando tu recurso_dao
    materiales_del_curso = RecursoDao.obtener_por_curso(id_curso)

    return render_template('docente/gestionar_curso.html',
                           curso=curso,
                           idiomas=todos_los_idiomas,
                           recursos=materiales_del_curso)


@docente_bp.route('/curso/<int:id_curso>', methods=['GET'])
def acceder_curso_docente(id_curso):
    if 'username' not in session or session.get('rol', '').lower() != 'docente':
        flash("Acceso denegado. Debes iniciar sesión como docente.")
        return redirect(url_for('auth.iniciar_sesion'))

    return redirect(url_for('docente.gestionar_curso_vista', id_curso=id_curso))

#Obtiene informacion sobre un curso: nombre, id del curso, lista de alumnos
@docente_bp.route('/tablero_docente/curso_docente/<int:id_curso>', methods=['GET'])
def curso_docente(id_curso):
    #Verificamos la session del docente
    if not session.get('username'):
        flash("Por favor, inicia sesión primero")
        return redirect(url_for('auth.iniciar_sesion'))
    # informacion general, lista de alumnos y materiales del curso
    lista_inscripcion = InscribirDao.consultar_lista_inscripcion(id_curso)
    curso = CursoDao.buscar_por_id(id_curso)
    recursos = RecursoDao.obtener_por_curso(id_curso)

    if not curso:
        flash("Curso no encontrado")
        return redirect(url_for('docente.tablero_docente'))

    return render_template('curso_detalle.html', curso=curso, recursos=recursos, lista_inscripcion=lista_inscripcion, role='docente')

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



@docente_bp.route('/actualizar_curso_procesar/<int:id_curso>', methods=['POST'])
def actualizar_curso_procesar(id_curso):
    if 'username' not in session or session.get('rol').lower() != 'docente':
        return redirect(url_for('auth.iniciar_sesion'))

    curso = CursoDao.buscar_por_id(id_curso)
    if not curso:
        flash("El curso que intentas actualizar no existe.", category="error")
        return redirect(url_for('docente.tablero_docente'))

    nombre_idioma_input = request.form.get('nombre_idioma')

    try:
        idioma_existente = Idioma.query.filter_by(nombre_idioma=nombre_idioma_input).first()
        if idioma_existente:
            id_idioma = idioma_existente.id_idioma
        else:
            nuevo_idioma = Idioma(nombre_idioma=nombre_idioma_input)
            db.session.add(nuevo_idioma)
            db.session.commit()
            id_idioma = nuevo_idioma.id_idioma

        # Actualizamos los campos directo en el objeto del modelo obtenido por el DAO
        curso.nombre_curso = request.form.get('nombre_curso')
        curso.nivel = request.form.get('nivel')
        curso.descripcion = request.form.get('descripcion')
        curso.id_idioma = id_idioma

        db.session.commit()
        flash("Curso actualizado correctamente.", category="success")

    except Exception as e:
        db.session.rollback()
        flash(f"Error al actualizar el curso: {str(e)}", category="error")

    return redirect(url_for('docente.gestionar_curso_vista', id_curso=id_curso))


@docente_bp.route('/eliminar_curso_procesar/<int:id_curso>', methods=['POST'])
def eliminar_curso_procesar(id_curso):
    if 'username' not in session or session.get('rol').lower() != 'docente':
        return redirect(url_for('auth.iniciar_sesion'))

    resultado = CursoDao.eliminar_curso(id_curso)
    if resultado:
        flash("Curso eliminado correctamente del sistema.", category="success")
    else:
        flash("Error al intentar eliminar el curso.", category="error")

    return redirect(url_for('docente.tablero_docente'))


# Rutas para procesar carga y eliminación de materiales

@docente_bp.route('/gestionar_curso/<int:id_curso>/subir_recurso', methods=['POST'])
def subir_recurso_procesar(id_curso):
    if 'username' not in session or session.get('rol').lower() != 'docente':
        return redirect(url_for('auth.iniciar_sesion'))

    titulo = request.form.get('titulo_recurso')
    descripcion = request.form.get('descripcion_recurso')
    file = request.files.get('archivo_fisico')

    if not file or file.filename == '':
        flash("Por favor, selecciona un archivo válido para subir.", category="error")
        return redirect(url_for('docente.gestionar_curso_vista', id_curso=id_curso))

    try:
        # Generar un nombre único aleatorio para evitar colisiones en la nube
        extension = file.filename.split('.')[-1] if '.' in file.filename else 'dat'
        nombre_unico_archivo = f"{uuid.uuid4()}.{extension}"

        # Verificar que el cliente de Supabase esté disponible
        if not supabase_client:
            flash("El almacenamiento en la nube no está configurado.", category="error")
            return redirect(url_for('docente.gestionar_curso_vista', id_curso=id_curso))

        # Transmitir el archivo hacia Supabase
        file_bytes = file.read()
        supabase_client.storage.from_(BUCKET_NAME).upload(
            path=nombre_unico_archivo,
            file=file_bytes,
            file_options={"content-type": file.content_type}
        )

        # Construir la ruta URL de acceso directo público que entrega el Bucket
        url_publica_archivo = f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET_NAME}/{nombre_unico_archivo}"

        # Guardar información en la base de datos
        RecursoDao.guardar_recurso(titulo, url_publica_archivo, descripcion, id_curso)

        flash("Material cargado y almacenado correctamente.", category="success")

    except Exception as e:
        flash(f"Error al interactuar con el almacenamiento: {str(e)}", category="error")

    return redirect(url_for('docente.gestionar_curso_vista', id_curso=id_curso))


@docente_bp.route('/gestionar_curso/<int:id_curso>/eliminar_recurso/<int:id_recurso>', methods=['POST'])
def eliminar_recurso_procesar(id_curso, id_recurso):
    if 'username' not in session or session.get('rol').lower() != 'docente':
        return redirect(url_for('auth.iniciar_sesion'))

    recurso = RecursoDao.buscar_por_id(id_recurso)
    if not recurso:
        flash("El recurso que intentas eliminar no existe.", category="error")
        return redirect(url_for('docente.gestionar_curso_vista', id_curso=id_curso))

    try:
        # Recuperar el nombre exacto del objeto en la nube
        nombre_archivo_en_nube = recurso.archivo_url.split('/')[-1]

        # Verificar que el cliente de Supabase esté disponible
        if not supabase_client:
            flash("El almacenamiento en la nube no está configurado.", category="error")
            return redirect(url_for('docente.gestionar_curso_vista', id_curso=id_curso))

        # Purgar el archivo binario del Storage de Supabase
        supabase_client.storage.from_(BUCKET_NAME).remove([nombre_archivo_en_nube])

        # Eliminar el registro en la base de datos
        RecursoDao.eliminar_recurso(id_recurso)

        flash("El material ha sido eliminado correctamente.", category="success")

    except Exception as e:
        flash(f"Error al eliminar el archivo: {str(e)}", category="error")

    return redirect(url_for('docente.gestionar_curso_vista', id_curso=id_curso))

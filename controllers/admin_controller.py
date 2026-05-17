from getopt import error

from flask import Blueprint, render_template, request, redirect, flash, session, url_for, jsonify
from dao.alumno_dao import AlumnoDao
from dao.docente_dao import DocenteDao
from models import Alumno
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/tablero_admin', methods=['GET'])
def tablero_administrador():

    nombre = session.get('username')

    if not nombre:
        flash("Por favor, inicia sesión primero", category="error")
        return redirect(url_for('auth.iniciar_sesion'))
    return render_template('admin/tablero_admin.html')

@admin_bp.route('/gestionar_docentes', methods=['GET'])
def visualizar_docentes():
    lista_docentes = DocenteDao.buscar_docentes()

    docentes_json = [
        {
            "id_usuario": d.id_usuario,
            "username": d.perfil_usuario.username,
            "nombre": d.perfil_usuario.nombre,
            "apellido_paterno": d.perfil_usuario.apellido_paterno,
            "apellido_materno": d.perfil_usuario.apellido_materno,
            "email": d.perfil_usuario.email,
            "genero": d.perfil_usuario.genero,
            "pais": d.perfil_usuario.pais,
            "fecha_nacimiento": d.perfil_usuario.fecha_nacimiento.strftime(
                "%Y-%m-%d") if d.perfil_usuario.fecha_nacimiento else None,
            "ultima_fecha_acceso": d.perfil_usuario.ultima_fecha_acceso.strftime(
                "%Y-%m-%d") if d.perfil_usuario.ultima_fecha_acceso else None,
            "tiempo_experiencia": d.tiempo_experiencia,
            "especialidad": d.especialidad
        } for d in lista_docentes
    ]

    return render_template('admin/gestionar_docentes.html', docentes=docentes_json)

    return lista_docentes
@admin_bp.route('/gestionar_docentes/<id_usuario>', methods=['GET', 'POST'])
def gestionar_docentes(id_usuario):
    if request.method == 'GET':
        d = DocenteDao.buscar_por_id(id_usuario)

        docente = {
                "id_usuario": d.id_usuario,
                "username": d.perfil_usuario.username,
                "nombre": d.perfil_usuario.nombre,
                "apellido_paterno": d.perfil_usuario.apellido_paterno,
                "apellido_materno": d.perfil_usuario.apellido_materno,
                "email": d.perfil_usuario.email,
                "genero": d.perfil_usuario.genero,
                "pais": d.perfil_usuario.pais,
                "fecha_nacimiento": d.perfil_usuario.fecha_nacimiento.strftime(
                    "%Y-%m-%d") if d.perfil_usuario.fecha_nacimiento else None,
                "ultima_fecha_acceso": d.perfil_usuario.ultima_fecha_acceso.strftime(
                    "%Y-%m-%d") if d.perfil_usuario.ultima_fecha_acceso else None,
                "tiempo_experiencia": d.tiempo_experiencia,
                "especialidad": d.especialidad
            }
        return render_template('admin/editar_docente.html', docente=docente)

    elif request.method == 'POST':
        llaves = [
            "username", "nombre", "apellido_paterno", "apellido_materno",
            "email", "password", "genero", "pais", "fecha_nacimiento",
            "tiempo_experiencia", "especialidad"
        ]

        datos_entrada = request.get_json() if request.is_json else request.form

        if not datos_entrada:
            return redirect(url_for('admin.gestionar_docentes', id_usuario=id_usuario))

        docente_dict = {
            k : datos_entrada.get(k)
            for k in llaves
            if datos_entrada.get(k)
        }


        try:
            if "fecha_nacimiento" in docente_dict:
                datetime.strptime(docente_dict["fecha_nacimiento"], "%Y-%m-%d")
        except ValueError:
            flash("Error: El formato de fecha debe ser YYYY-MM-DD", category="error")
            return redirect(url_for('admin.gestionar_docentes', id_usuario=id_usuario))

        try:
            DocenteDao.actualizar_docente(id_usuario, docente_dict)
            flash("Datos actualizados correctamente", category="success")
            return redirect(url_for('admin.gestionar_docentes', id_usuario=id_usuario))
        except Exception as e:
            msg = str(e)
            flash(f"Error: {msg}", category="error")
            return redirect(url_for('admin.gestionar_docentes', id_usuario=id_usuario))


@admin_bp.route('/consultar_docentes', methods=['POST'])
def consultar_docentes():
    llaves = [
        "id_usuario", "username", "nombre", "apellido_paterno", "apellido_materno",
        "email", "genero", "pais", "fecha_nacimiento_min", "fecha_nacimiento_max",
        "ultima_fecha_acceso_min", "ultima_fecha_acceso_max",
        "tiempo_experiencia_min", "tiempo_experiencia_max" ,"especialidad"
    ]

    datos_entrada = request.get_json() if request.is_json else request.form
    if not datos_entrada:
        flash("Error: Formato de datos incorrecto", category="error")
        return redirect(url_for('admin.visualizar_docentes'))

    docente_dict = {
        k: datos_entrada.get(k)
        for k in llaves
        if datos_entrada.get(k)
    }

    llaves_fecha = [
        "fecha_nacimiento_min", "fecha_nacimiento_max",
        "ultima_fecha_acceso_min", "ultima_fecha_acceso_max"
    ]

    try:
        for llave in llaves_fecha:
            if llave in docente_dict:
                datetime.strptime(docente_dict[llave], "%Y-%m-%d")

    except ValueError:
        flash("Error: El formato de fecha debe ser YYYY-MM-DD", category="error")
        return redirect(url_for('admin.visualizar_docentes'))

    try:

        lista_docentes = DocenteDao.buscar_por_atributos(docente_dict)

        docentes_json = [
            {
                "id_usuario": d.id_usuario,
                "username": d.perfil_usuario.username,
                "nombre": d.perfil_usuario.nombre,
                "apellido_paterno": d.perfil_usuario.apellido_paterno,
                "apellido_materno": d.perfil_usuario.apellido_materno,
                "email": d.perfil_usuario.email,
                "genero": d.perfil_usuario.genero,
                "pais": d.perfil_usuario.pais,
                "fecha_nacimiento": d.perfil_usuario.fecha_nacimiento.strftime(
                    "%Y-%m-%d") if d.perfil_usuario.fecha_nacimiento else None,
                "ultima_fecha_acceso": d.perfil_usuario.ultima_fecha_acceso.strftime(
                    "%Y-%m-%d") if d.perfil_usuario.ultima_fecha_acceso else None,
                "tiempo_experiencia": d.tiempo_experiencia,
                "especialidad": d.especialidad
            } for d in lista_docentes
        ]
        return jsonify(docentes_json)
    except Exception as e:
        msg = str(e)
        flash(f"Error: {msg}", category="error")
        return redirect(url_for('admin.visualizar_docentes'))

@admin_bp.route('/eliminar_docente/<id_usuario>', methods=['GET'])
def eliminar_docente(id_usuario):

    try:
        DocenteDao.eliminar_docente(id_usuario)
        flash("Docente eliminado correctamente", category="success")
        return redirect(url_for('admin.visualizar_docentes'))
    except Exception as e:
        flash(f"Error: {e}", category="error")
        return redirect(url_for('admin.gestionar_docentes', id_usuario=id_usuario))

@admin_bp.route('/gestionar_alumnos', methods=['GET'])
def visualizar_alumnos():
    lista_alumnos = AlumnoDao.buscar_alumnos()

    alumnos_json = [
        {
            "id_usuario": a.id_usuario,
            "username": a.perfil_usuario.username,
            "nombre": a.perfil_usuario.nombre,
            "apellido_paterno": a.perfil_usuario.apellido_paterno,
            "apellido_materno": a.perfil_usuario.apellido_materno,
            "email": a.perfil_usuario.email,
            "genero": a.perfil_usuario.genero,
            "pais": a.perfil_usuario.pais,
            "fecha_nacimiento": a.perfil_usuario.fecha_nacimiento.strftime(
                "%Y-%m-%d") if a.perfil_usuario.fecha_nacimiento else None,
            "ultima_fecha_acceso": a.perfil_usuario.ultima_fecha_acceso.strftime(
                "%Y-%m-%d") if a.perfil_usuario.ultima_fecha_acceso else None,
            "grado_actual": a.grado_actual
        } for a in lista_alumnos
    ]

    return render_template('admin/gestionar_alumnos.html', alumnos=alumnos_json)

@admin_bp.route('/gestionar_alumnos/<id_usuario>', methods=['GET', 'POST'])
def gestionar_alumnos(id_usuario):
    if request.method == 'GET':
        a = AlumnoDao.buscar_por_id(id_usuario)

        alumno = {
                "id_usuario": a.id_usuario,
                "username": a.perfil_usuario.username,
                "nombre": a.perfil_usuario.nombre,
                "apellido_paterno": a.perfil_usuario.apellido_paterno,
                "apellido_materno": a.perfil_usuario.apellido_materno,
                "email": a.perfil_usuario.email,
                "genero": a.perfil_usuario.genero,
                "pais": a.perfil_usuario.pais,
                "fecha_nacimiento": a.perfil_usuario.fecha_nacimiento.strftime(
                    "%Y-%m-%d") if a.perfil_usuario.fecha_nacimiento else None,
                "ultima_fecha_acceso": a.perfil_usuario.ultima_fecha_acceso.strftime(
                    "%Y-%m-%d") if a.perfil_usuario.ultima_fecha_acceso else None,
                "grado_actual": a.grado_actual
        }
        return render_template('admin/editar_alumno.html', alumno=alumno)

    elif request.method == 'POST':
        llaves = [
            "username", "nombre", "apellido_paterno", "apellido_materno",
            "email", "password", "genero", "pais", "fecha_nacimiento",
            "grado_actual"
        ]

        datos_entrada = request.get_json() if request.is_json else request.form
        if not datos_entrada:
            return redirect(url_for('admin.gestionar_alumnos', id_usuario=id_usuario))

        alumno_dict = {
            k: datos_entrada.get(k)
            for k in llaves
            if datos_entrada.get(k)
        }


        try:
            if "fecha_nacimiento" in alumno_dict:
                datetime.strptime(alumno_dict["fecha_nacimiento"], "%Y-%m-%d")
        except ValueError:
            flash("Error: El formato de fecha debe ser YYYY-MM-DD", category="error")
            return redirect(url_for('admin.gestionar_alumnos', id_usuario=id_usuario))

        try:
            AlumnoDao.actualizar_alumno(id_usuario, alumno_dict)
            flash("Datos actualizados correctamente", category="success")
            return redirect(url_for('admin.gestionar_alumnos', id_usuario=id_usuario))
        except Exception as e:
            msg = str(e)
            flash(f"Error: {msg}", category="error")
            return redirect(url_for('admin.gestionar_alumnos', id_usuario=id_usuario))



@admin_bp.route('/consultar_alumnos', methods=['POST'])
def consultar_alumnos():
    llaves = [
        "id_usuario", "username", "nombre", "apellido_paterno", "apellido_materno",
        "email", "genero", "pais", "fecha_nacimiento_min", "fecha_nacimiento_max",
        "ultima_fecha_acceso_min", "ultima_fecha_acceso_max",
        "grado_actual"
    ]

    datos_entrada = request.get_json() if request.is_json else request.form
    if not datos_entrada:
        flash("Error: Formato de datos incorrecto", category="error")
        return redirect(url_for('admin.visualizar_alumnos'))

    alumno_dict = {
        k: datos_entrada.get(k)
        for k in llaves
        if datos_entrada.get(k)
    }

    llaves_fecha = [
        "fecha_nacimiento_min", "fecha_nacimiento_max",
        "ultima_fecha_acceso_min", "ultima_fecha_acceso_max"
    ]

    try:
        for llave in llaves_fecha:
            if llave in alumno_dict:
                datetime.strptime(alumno_dict[llave], "%Y-%m-%d")

    except ValueError:
        flash("Error: El formato de fecha debe ser YYYY-MM-DD", category="error")
        return redirect(url_for('admin.visualizar_alumnos'))

    try:
        lista_alumnos = AlumnoDao.buscar_por_atributos(alumno_dict)

        alumnos_json = [
            {
                "id_usuario": a.id_usuario,
                "username": a.perfil_usuario.username,
                "nombre": a.perfil_usuario.nombre,
                "apellido_paterno": a.perfil_usuario.apellido_paterno,
                "apellido_materno": a.perfil_usuario.apellido_materno,
                "email": a.perfil_usuario.email,
                "genero": a.perfil_usuario.genero,
                "pais": a.perfil_usuario.pais,
                "fecha_nacimiento": a.perfil_usuario.fecha_nacimiento.strftime(
                    "%Y-%m-%d") if a.perfil_usuario.fecha_nacimiento else None,
                "ultima_fecha_acceso": a.perfil_usuario.ultima_fecha_acceso.strftime(
                    "%Y-%m-%d") if a.perfil_usuario.ultima_fecha_acceso else None,
                "grado_actual": a.grado_actual
            } for a in lista_alumnos
        ]

        return jsonify(alumnos_json)
    except Exception as e:
        msg = str(e)
        flash(f"Error: {msg}", category="error")
        return redirect(url_for('admin.visualizar_alumnos'))


@admin_bp.route('/eliminar_alumno/<id_usuario>', methods=['GET'])
def eliminar_alumno(id_usuario):

    try:
        AlumnoDao.eliminar_alumno(id_usuario)
        flash("Alumno eliminado correctamente", category="success")
        return redirect(url_for('admin.visualizar_alumnos'))
    except Exception as e:
        flash(f"Error: {e}", category="error")
        return redirect(url_for('admin.gestionar_alumnos', id_usuario=id_usuario))
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
        flash("Por favor, inicia sesión primero")
        return redirect(url_for('auth.iniciar_sesion'))
    return f"Bienvenido {nombre}"

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

    return jsonify(docentes_json)

    return lista_docentes
@admin_bp.route('/gestionar_docentes/<id_usuario>', methods=['GET', 'POST'])
def gestionar_docente(id_usuario):
    if request.method == 'GET':
        d = DocenteDao.buscar_por_id(id_usuario)

        docente = [
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
            }
        ]
        return jsonify(docente)

    elif request.method == 'POST':
        llaves = [
            "username", "nombre", "apellido_paterno", "apellido_materno",
            "email", "password", "genero", "pais", "fecha_nacimiento", "ultima_fecha_acceso",
            "tiempo_experiencia", "especialidad"
        ]

        docente_dict = {
            k : request.form.get(k)
            for k in llaves
            if request.form.get(k)
        }

        if "fecha_nacimiento" in docente_dict:
            try:
                datetime.strptime(docente_dict["fecha_nacimiento"], "%Y-%m-%d")
                if "ultima_fecha_acceso" in docente_dict:
                    datetime.strptime(docente_dict["ultima_fecha_acceso"], "%Y-%m-%d")
                DocenteDao.actualizar_docente(id_usuario, docente_dict)
                flash("Datos actualizados correctamente")
                return redirect(url_for(f'admin_bp.gestionar_docente/{id_usuario}'))
            except ValueError:
                flash("Error: El formato de fecha debe ser YYYY-MM-DD")
                return redirect(url_for('admin_bg.gestionar_docente'))

@admin_bp.route('/consultar_docentes', methods=['POST'])
def consultar_docentes():
    llaves = [
        "id_usuario", "username", "nombre", "apellido_paterno", "apellido_materno",
        "email", "password", "genero", "pais", "fecha_nacimiento", "ultima_fecha_acceso",
        "tiempo_experiencia", "especialidad"
    ]

    docente_dict = {
        k: request.form.get(k)
        for k in llaves
        if request.form.get(k)
    }

    if "fecha_nacimiento" in docente_dict:
        try:
            datetime.strptime(docente_dict["fecha_nacimiento"], "%Y-%m-%d")
            if "ultima_fecha_acceso" in docente_dict:
                datetime.strptime(docente_dict["ultima_fecha_acceso"], "%Y-%m-%d")
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
            flash("Datos actualizados correctamente")
            return jsonify(docentes_json)
        except ValueError:
            flash("Error: El formato de fecha debe ser YYYY-MM-DD")
            return redirect(url_for('admin_bg.conultar_docentes'))



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

    return jsonify(alumnos_json)

@admin_bp.route('/gestionar_alumnos/<id_usuario>', methods=['GET', 'POST'])
def gestionar_alumno(id_usuario):
    if request.method == 'GET':
        a = AlumnoDao.buscar_por_id(id_usuario)

        alumno = [
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
            }
        ]
        return jsonify(alumno)

    elif request.method == 'POST':
        llaves = [
            "username", "nombre", "apellido_paterno", "apellido_materno",
            "email", "password", "genero", "pais", "fecha_nacimiento", "ultima_fecha_acceso",
            "grado_actual"
        ]

        alumno_dict = {
            k: request.form.get(k)
            for k in llaves
            if request.form.get(k)
        }

        if "fecha_nacimiento" in alumno_dict:
            try:
                datetime.strptime(alumno_dict["fecha_nacimiento"], "%Y-%m-%d")
                if "ultima_fecha_acceso" in alumno_dict:
                    datetime.strptime(alumno_dict["ultima_fecha_acceso"], "%Y-%m-%d")
                AlumnoDao.actualizar_alumno(id_usuario, alumno_dict)
                flash("Datos actualizados correctamente")
            except ValueError:
                flash("Error: El formato de fecha debe ser YYYY-MM-DD")
                return redirect(url_for('admin_bg.gestionar_alumno'))



@admin_bp.route('/consultar_alumnos', methods=['POST'])
def consultar_alumnos():
    llaves = [
        "id_usuario", "username", "nombre", "apellido_paterno", "apellido_materno",
        "email", "password", "genero", "pais", "fecha_nacimiento", "ultima_fecha_acceso",
        "grado_actual"
    ]

    alumno_dict = {
        k: request.form.get(k)
        for k in llaves
        if request.form.get(k)
    }

    if "fecha_nacimiento" in alumno_dict:
        try:
            datetime.strptime(alumno_dict["fecha_nacimiento"], "%Y-%m-%d")
            if "ultima_fecha_acceso" in alumno_dict:
                datetime.strptime(alumno_dict["ultima_fecha_acceso"], "%Y-%m-%d")
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

            flash("Datos actualizados correctamente")
            return jsonify(alumnos_json)

        except ValueError:
            flash("Error: El formato de fecha debe ser YYYY-MM-DD")
            return redirect(url_for('admin_bg.conultar_alumnos'))

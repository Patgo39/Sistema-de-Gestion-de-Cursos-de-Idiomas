from flask import Blueprint, render_template, request, redirect, flash, session, url_for
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
    return lista_docentes
@admin_bp.route('/gestionar_docentes/<id_usuario>', methods=['GET', 'POST'])
def gestionar_docente(id_usuario):
    if request.method == 'GET':
        docente = DocenteDao.buscar_por_id(id_usuario)
        return docente
    elif request.method == 'POST':
        llaves = [
            "username", "nombre", "apellido_paterno", "apellido_materno",
            "email", "password", "genero", "pais", "fecha_nacimiento",
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
                DocenteDao.actualizar_docente(id_usuario, docente_dict)
                flash("Datos actualizados correctamente")
            except ValueError:
                flash("Error: El formato de fecha debe ser YYYY-MM-DD")
                return redirect(url_for('admin_bg.gestionar_docente'))


@admin_bp.route('/gestionar_alumnos', methods=['GET'])
def visualizar_alumnos():
    lista_alumnos = AlumnoDao.buscar_alumnos()
    return lista_alumnos

@admin_bp.route('/gestionar_alumnos/<id_usuario>', methods=['GET', 'POST'])
def gestionar_alumno(id_usuario):
    if request.method == 'GET':
        alumno = AlumnoDao.buscar_por_id(id_usuario)
        return alumno
    elif request.method == 'POST':
        llaves = [
            "username", "nombre", "apellido_paterno", "apellido_materno",
            "email", "password", "genero", "pais", "fecha_nacimiento",
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
                AlumnoDao.actualizar_alumno(id_usuario, alumno_dict)
                flash("Datos actualizados correctamente")
            except ValueError:
                flash("Error: El formato de fecha debe ser YYYY-MM-DD")
                return redirect(url_for('admin_bg.gestionar_alumno'))



from flask import Blueprint, request, jsonify
from dao.curso_dao import CursoDao


curso_bp = Blueprint('curso_bp', __name__)


@curso_bp.route('/cursos', methods=['POST'])
def crear_curso():
    data = request.get_json()

    nombre = data.get('nombre_curso')
    descripcion = data.get('descripcion')
    nivel = data.get('nivel')
    id_usuario = data.get('id_usuario')
    id_idioma = data.get('id_idioma')

    if not all([nombre, id_usuario, id_idioma]):
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    nuevo_curso = CursoDao.crear_curso(nombre, descripcion, nivel, id_usuario, id_idioma)

    if nuevo_curso:
        return jsonify({
            "message": "Curso creado con éxito",
            "id_curso": nuevo_curso.id_curso
        }), 201

    return jsonify({"error": "No se pudo crear el curso"}), 500


@curso_bp.route('/cursos/docente/<int:id_docente>', methods=['GET'])
def listar_cursos(id_docente):
    cursos = CursoDao.obtener_cursos_por_docente(id_docente)

    resultado = []
    for c in cursos:
        resultado.append({
            "id_curso": c.id_curso,
            "nombre": c.nombre_curso,
            "nivel": c.nivel,
            "descripcion": c.descripcion
        })

    return jsonify(resultado), 200



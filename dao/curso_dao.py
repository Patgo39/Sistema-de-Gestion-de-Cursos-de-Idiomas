from db import db
from models.curso import Curso

class CursoDao:

    @classmethod
    def crear_curso(cls, nombre_curso, descripcion, nivel, id_usuario, id_idioma):
        try:
            nuevo_curso = Curso(
                nombre_curso=nombre_curso,
                descripcion=descripcion,
                nivel=nivel,
                id_usuario=id_usuario,
                id_idioma=id_idioma
            )

            db.session.add(nuevo_curso)
            db.session.commit()
            return nuevo_curso

        except Exception as e:
            db.session.rollback()
            print(f"Error al crear el curso: {e}")
            return None

    @classmethod
    def obtener_cursos_por_docente(cls, id_usuario):
        return Curso.query.filter_by(id_usuario=id_usuario).all()
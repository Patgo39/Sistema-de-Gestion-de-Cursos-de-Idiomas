from db import db
from models.curso import Curso
from models.inscribir import Inscribir
from models.alumno import Alumno

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
    @classmethod
    def obtener_cursos_por_alumno(cls, id_usuario):
        try:
            cursos_inscritos = db.session.query(Curso).join(
                Inscribir, Curso.id_curso == Inscribir.id_curso
            ).filter(
                Inscribir.id_usuario == id_usuario
            ).all()

            return cursos_inscritos

        except Exception as e:
            print(f"Error al obtener los cursos del alumno: {e}")
            return []

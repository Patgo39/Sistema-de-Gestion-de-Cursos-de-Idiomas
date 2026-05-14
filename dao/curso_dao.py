from db import db
from models.curso import Curso
from models.inscribir import Inscribir
from models.alumno import Alumno

class CursoDao:

    @classmethod
    def crear_curso(cls, nombre_curso, descripcion, nivel, id_usuario, id_idioma):
        '''
        Crear un curso en la base de datos
        :param nombre_curso:  nombre del curso
        :param descripcion:  descripcion del curso
        :param nivel:  nivel del curso
        :param id_usuario:  id_usuario del usuario
        :param id_idioma:  id_idioma del usuario
        :return:  Curso en la base de datos
        '''
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
    def obtener_todos(cls):
        '''
        Obtener todos los cursos
        :return: cursos en la base de datos
        '''
        return Curso.query.all()

    @classmethod
    def buscar_por_id(cls, id_curso):
        '''
        Buscar un curso en la base de datos por id_curso
        :param id_curso:  id_curso
        :return:  curso en la base de datos
        '''
        try:
            curso = Curso.query.filter_by(id_curso=id_curso).first()
            return curso
        except Exception as e:
            print(f"Error al buscar el curso: {e}")
            return None

    @classmethod
    def actualizar_curso(cls, id_curso, datos_actualizados):
        '''
        Actualizar un curso en la base de datos
        :param id_curso:  id_curso
        :param datos_actualizados:  Diccionario con los datos actualizados del curso
        :return:  None
        '''
        try:
            curso = cls.buscar_por_id(id_curso)
            if curso:
                for clave, valor in datos_actualizados.items():
                    if hasattr(curso, clave):
                        setattr(curso, clave, valor)

                db.session.commit()
                return curso
            return None
        except Exception as e:
            db.session.rollback()
            print(f"Error al actualizar el curso: {e}")
            return None

    @classmethod
    def eliminar_curso(cls, id_curso):
        '''
        Eliminar un curso en la base de datos
        :param id_curso:  id_curso
        :return:  Bool si se elimino el curso en la base de datos
        '''
        try:
            curso = cls.buscar_por_id(id_curso)
            if curso:
                db.session.delete(curso)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            print(f"Error al eliminar el curso: {e}")
            return False

    @classmethod
    def obtener_cursos_por_docente(cls, id_usuario):
        '''
        Obtener todos los cursos en la base de datos por id_usuario (alumno)
        :param id_usuario:  id_usuario
        :return:  cursos en la base de datos
        '''
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
    @classmethod
    def buscar_por_id(cls, id_curso):
        ''' Buscar un curso en la base de datos
        :param id_curso:  id_curso
        :return:  curso en la base de datos
        '''
        try:
            curso=Curso.query.filter_by(id_curso=id_curso).first()
            return curso
        except Exception as e:
            print(f"Error al buscar el curso: {e}")
            return None


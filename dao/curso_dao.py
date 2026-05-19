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
    def obtener_todos_los_cursos(cls):
        '''
        Obtener todos los cursos
        :return:  Lista de cursos en la base de datos
        '''
        cursos_db = Curso.query.all()
        lista_cursos = []

        for curso in cursos_db:
            inscritos_mapped = []
            for inscrito in curso.lista_inscritos.all():
                inscritos_mapped.append({
                    'id_usuario': inscrito.id_usuario,
                    'fecha_inscripcion': inscrito.fecha_inscripcion.strftime(
                        '%Y-%m-%d %H:%M:%S') if inscrito.fecha_inscripcion else None,
                    'nombre_alumno': inscrito.alumno.nombre if inscrito.alumno else None
                })


            recursos_mapped = []
            for recurso in curso.lista_recursos.all():
                recursos_mapped.append({
                    'id_recurso': recurso.id_recurso,
                    'titulo_recurso': recurso.titulo_recurso,
                    'descripcion': recurso.descripcion,
                    'fecha_subida': recurso.fecha_subida.strftime('%Y-%m-%d') if recurso.fecha_subida else None,
                    'archivo_url': recurso.archivo_url
                })


            lista_cursos.append({
                'id_curso': curso.id_curso,
                'nombre_curso': curso.nombre_curso,
                'descripcion': curso.descripcion,
                'nivel': curso.nivel,
                'docente': curso.docente.perfil_usuario.nombre if curso.docente and curso.docente.perfil_usuario else None,
                'idioma': curso.idioma.nombre_idioma if curso.idioma else None,
                'inscritos': inscritos_mapped,
                'recursos': recursos_mapped
            })

        return lista_cursos

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
        ''' Buscar un curso en la base de datos por id_curso
        :param id_curso:  id_curso
        :return:  curso en la base de datos
        '''
        try:
            curso=Curso.query.filter_by(id_curso=id_curso).first()
            return curso
        except Exception as e:
            print(f"Error al buscar el curso: {e}")
            return None


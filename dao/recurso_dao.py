from db import db
from models.recurso import Recurso


class RecursoDao:
    @staticmethod
    def guardar_recurso(titulo, filename, descripcion, id_curso):
        '''
        Guardar un recurso en la base de datos
        :param titulo: titulo del recurso
        :param filename:  nombre del archivo
        :param descripcion:  descripcion del recurso
        :param id_curso:  id_curso del recurso
        :return: recurso en la base de datos
        '''
        nuevo_recurso = Recurso(
            titulo_recurso=titulo,
            archivo_url=filename,
            descripcion=descripcion,
            id_curso=id_curso
        )
        db.session.add(nuevo_recurso)
        db.session.commit()
        return nuevo_recurso
    @staticmethod
    def obtener_todos():
        '''
        Obtener todos los recursos
        :return:  todos los recursos
        '''
        return Recurso.query.all()

    @staticmethod
    def buscar_por_id(id_recurso):
        '''
        Buscar un recurso en la base de datos
        :param id_recurso:  id_recurso
        :return:  recurso en la base de datos
        '''
        return Recurso.query.get(id_recurso)

    @staticmethod
    def obtener_por_curso(id_curso):
        '''
        Obtener un recurso en la base de datos por id_curso
        :param id_curso:  id_curso
        :return:  recurso en la base de datos
        '''
        return Recurso.query.filter_by(id_curso=id_curso).all()

    @staticmethod
    def actualizar_recurso(id_recurso, datos):
        '''
        Actualizar un recurso en la base de datos
        :param id_recurso:  id_recurso
        :param datos: Diccionario de los datos del recurso
        :return: None
        '''
        try:
            recurso = Recurso.query.get(id_recurso)
            if recurso:
                for clave, valor in datos.items():
                    if hasattr(recurso, clave):
                        setattr(recurso, clave, valor)
                db.session.commit()
                return recurso
            return None
        except Exception as e:
            db.session.rollback()
            print(f"Error al actualizar recurso: {e}")
            return None

    @staticmethod
    def eliminar_recurso(id_recurso):
        '''
        Eliminar un recurso en la base de datos
        :param id_recurso:  id_recurso
        :return:  recurso en la base de datos
        '''
        try:
            recurso = Recurso.query.get(id_recurso)
            if recurso:
                db.session.delete(recurso)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            print(f"Error al eliminar recurso: {e}")
            return False



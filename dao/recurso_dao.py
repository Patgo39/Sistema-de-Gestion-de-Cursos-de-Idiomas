from db import db
from models.recurso import Recurso


class RecursoDao:
    @staticmethod
    def guardar_recurso(titulo, filename, descripcion, id_curso):
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
        return Recurso.query.all()


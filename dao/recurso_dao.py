from db import db
from models.recurso import Recurso


class RecursoDao:
    @staticmethod
    def guardar_recurso(nombre,filename,descripcion, id_profe):
        nuevo_recurso = Recurso(
            nombre_recurso = nombre,
            archivo_url = filename,
            descripcion = descripcion,
            id_docente = id_profe
        )
        db.session.add(nuevo_recurso)
        db.session.commit()
        return nuevo_recurso
    @staticmethod
    def obtener_todos():
        return Recurso.query.all()


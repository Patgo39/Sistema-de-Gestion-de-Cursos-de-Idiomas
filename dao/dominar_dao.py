from db import db
from models.dominar import Dominar

class DominarDao:

    @staticmethod
    def obtener_ids_por_alumno(id_alumno: int) -> set[int]:
        """Retorna un conjunto de IDs de idiomas que ya maneja el alumno."""
        relaciones = Dominar.query.filter_by(id_usuario=id_alumno).all()
        return {r.id_idioma for r in relaciones}

    @staticmethod
    def eliminar_relaciones_por_ids(id_alumno: int, ids_idiomas: list[int]):
        """Elimina la vinculación de idiomas específicos por id para un alumno."""
        if ids_idiomas:
            Dominar.query.filter(
                Dominar.id_usuario == id_alumno,
                Dominar.id_idioma.in_(ids_idiomas)
            ).delete(synchronize_session=False)

    @staticmethod
    def agregar_relaciones(id_alumno: int, idiomas_con_nivel: dict[int, str]):
        """Crea nuevas filas en la tabla Dominar usando un diccionario {id: nivel}."""
        for id_idm, nivel in idiomas_con_nivel.items():
            nueva_relacion = Dominar(
                id_usuario=id_alumno,
                id_idioma=id_idm,
                nivel_dominio=nivel
            )
            db.session.add(nueva_relacion)
from db import db
from models.manejar import Manejar

class ManejarDao:

    @staticmethod
    def obtener_ids_por_docente(id_docente: int) -> set[int]:
        """Retorna un conjunto de IDs de idiomas que ya maneja el docente."""
        relaciones = Manejar.query.filter_by(id_usuario=id_docente).all()
        return {r.id_idioma for r in relaciones}

    @staticmethod
    def eliminar_relaciones_por_ids(id_docente: int, ids_idiomas: list[int]):
        """Elimina la vinculación de idiomas específicos por id para un docente."""
        if ids_idiomas:
            Manejar.query.filter(
                Manejar.id_usuario == id_docente,
                Manejar.id_idioma.in_(ids_idiomas)
            ).delete(synchronize_session=False)

    @staticmethod
    def agregar_relaciones(id_docente: int, idiomas_con_nivel: dict[int, str]):
        """Crea nuevas filas en la tabla Manejar usando un diccionario {id: nivel}."""
        for id_idm, nivel in idiomas_con_nivel.items():
            nueva_relacion = Manejar(
                id_usuario=id_docente,
                id_idioma=id_idm,
                nivel_dominio=nivel
            )
            db.session.add(nueva_relacion)
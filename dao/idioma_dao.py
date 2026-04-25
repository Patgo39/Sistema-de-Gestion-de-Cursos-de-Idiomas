from db import db
from models.idioma import Idioma

class IdiomaDao:

    @staticmethod
    def buscar_por_id(id_idioma: int) -> Idioma:
        idioma = Idioma.query.get(id_idioma)
        if not idioma:
            raise Exception(f'No existe el idioma con id {id_idioma}')
        return idioma

    @staticmethod
    def buscar_por_nombre(nombre_idioma: str) -> Idioma:
        """

        :param nombre_idioma:
        :return: EL objeto idioma con nombre del idioma o None si no
            se encuentra ningún idioma con el nombre.
        """
        nombre_idioma = nombre_idioma.upper()
        idioma = Idioma.query.filter_by(nombre_idioma=nombre_idioma).first()
        return idioma

    @staticmethod
    def agregar_idioma(nombre_idioma:str) -> Idioma:

        nombre_idioma = nombre_idioma.upper()

        idioma  = Idioma.filter_by(nombre_idioma=nombre_idioma).first()

        if idioma is None:
            idioma = Idioma(nombre_idioma=nombre_idioma)

            try:
                db.session.add(idioma)
                db.session.commit()
                db.session.refresh(idioma)
            except Exception as e:
                db.rollback()
                idioma = Idioma.query.filter_by(nombre_idioma=nombre_idioma).first()

        return idioma


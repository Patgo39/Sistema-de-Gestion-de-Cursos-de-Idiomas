from db import db
from datetime import datetime
from models.editar import Editar


class EditarDao:

    @staticmethod
    def crear_registro_edicion(id_administrador: int, id_usuario: int) -> Editar:
        try:
            nuevo_registro = Editar(
                id_administrador=id_administrador,
                id_usuario=id_usuario,
                fecha_edicion=datetime.now().date()
            )
            db.session.add(nuevo_registro)
            db.session.commit()
            return nuevo_registro
        except Exception as e:
            db.session.rollback()
            print(f"Error al crear el registro de edición: {e}")
            return None

    @staticmethod
    def buscar_por_llave_compuesta(id_administrador: int, id_usuario: int) -> Editar:
        # Cambio: Para llaves compuestas, pasamos una tupla a session.get
        return db.session.get(Editar, (id_administrador, id_usuario))

    @staticmethod
    def buscar_ediciones_por_administrador(id_administrador: int) -> list[Editar]:
        # filter_by sigue siendo válido, pero podrías usar la sintaxis moderna 2.0 si quisieras.
        # Por consistencia con lo anterior, mantenemos el query.filter_by que es aceptable.
        return Editar.query.filter_by(id_administrador=id_administrador).all()

    @staticmethod
    def actualizar_fecha_edicion(id_administrador: int, id_usuario: int) -> bool:
        try:
            # Cambio: Uso de db.session.get con tupla
            registro = db.session.get(Editar, (id_administrador, id_usuario))
            if not registro:
                raise Exception("El registro de edición no existe.")

            registro.fecha_edicion = datetime.now().date()
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error al actualizar la fecha de edición: {e}")
            raise e

    @staticmethod
    def eliminar_registro(id_administrador: int, id_usuario: int) -> bool:
        try:
            # Cambio: Uso de db.session.get con tupla
            registro = db.session.get(Editar, (id_administrador, id_usuario))
            if not registro:
                raise Exception("El registro de edición no existe.")

            db.session.delete(registro)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error al eliminar el registro de edición: {e}")
            raise e
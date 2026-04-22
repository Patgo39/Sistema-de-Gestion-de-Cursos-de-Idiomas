from db import db
from models.docente import Docente

class DocenteDao:

    @staticmethod
    def buscar_por_id(id_docente: int) -> Docente:
        pass

    @staticmethod
    def buscar_docentes() -> list[Docente]:
        pass

    @staticmethod
    def eliminar_docente(id_docente: int) -> None:
        pass

    @staticmethod
    def actualizar_docente(id_docente: int, datos: dict[str, str]) -> None:
        """
        Se actualizan los datos el docente.
        NO se puede modificar el rol ni la última fecha de acceso.
        :param id_docente: El id del docente a actualizar.
        :param datos: Los datos a actualizar. Es un diccionario con las llaves:
            username
            nombre
            apellido_paterno
            apellido_materno
            email
            password
            genero
            pais
            fecha_nacimiento
            tiempo_experiencia
            especialidad
        """
        pass


    @staticmethod
    def actualizar_ultimo_acceso() -> None:
        pass
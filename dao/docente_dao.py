from uno import Bool
from datetime import datetime
from datetime import date
from db import db
from models.docente import Docente
from models.manejar import Manejar
from models.idioma import Idioma
from dao.idioma_dao import IdiomaDao
from dao.manejar_dao import ManejarDao


class DocenteDao:

    @staticmethod
    def buscar_por_id(id_docente: int) -> Docente:
        docente = Docente.query.filter_by(id_usuario=id_docente).first()
        return docente

    @staticmethod
    def buscar_docentes() -> list[Docente]:
        docentes = Docente.query.all()
        return docentes

    @staticmethod
    def eliminar_docente(id_docente: int) -> Bool:
        docente = DocenteDao.buscar_por_id(id_docente)

        if not docente:
            raise Exception(f"No se encontró el docente con id : {id_docente}")
        try:
            usuario_eliminar = docente.perfil_usuario
            db.session.delete(usuario_eliminar)
            db.session.commit()
            return True
        except:
            db.session.rollback()
            raise Exception(f"Error al eliminar el docente con id : {id_docente}")

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
        docente = DocenteDao.buscar_por_id(id_docente)

        if not docente:
            raise Exception(f"No se encontró el docente con id : {id_docente}")

        try:
            if 'tiempo_experiencia' in datos:
                docente.tiempo_experiencia = datos['tiempo_experiencia']
            if 'especialidad' in datos:
                docente.especialidad = datos['especialidad']
            usuario = docente.perfil_usuario

            campos_usuario = [
                'username', 'nombre', 'apellido_paterno', 'apellido_materno',
                'email', 'password', 'genero', 'pais', 'fecha_nacimiento'
            ]

            for campo in campos_usuario:
                if campo in datos and datos[campo] is not None:
                    valor = datos[campo]

                    if campo == 'fecha_nacimiento' and isinstance(valor, str):
                        valor = datetime.strptime(valor, '%Y-%m-%d').date()

                    setattr(usuario, campo, valor) # Asignación dinámica de valores a usuario

            db.session.commit()

        except Exception as e:
            db.session.rollback()
            raise e


    @staticmethod
    def actualizar_ultimo_acceso(id_docente) -> None:
        docente = DocenteDao.buscar_por_id(id_docente)
        if not docente:
            raise Exception(f"No se encontró el docente con id : {id_docente}")

        usuario = docente.perfil_usuario

        usuario.ultima_fecha_acceso = date.today()
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def actualizar_lista_idiomas(id_docente: int, idiomas_input: dict[str, str]):
        """
        Recibe un diccionario de idioma, nivel y se compara con la lista actual de idiomas
        borrando o agregando idiomas.
        :param idiomas_input: Diccionario {'Ingles': 'Avanzado', 'Ruso': 'Básico'}
        """
        docente = DocenteDao.buscar_por_id(id_docente)
        if not docente:
            raise Exception(f"No se encontró el docente con id : {id_docente}")

        datos_finales = {}
        # Se hace un diccionario con id_idioma y nivel
        for nombre, nivel in idiomas_input.items():
            idm_obj = IdiomaDao.agregar_idioma(nombre)
            datos_finales[idm_obj.id_idioma] = nivel

        # Los ids nuevos son los recibidos en idiomas_input
        # Es posible que idiomas en idiomas_input ya estén asociados a docente
        ids_nuevos = set(datos_finales.keys())
        ids_actuales = ManejarDao.obtener_ids_por_docente(id_docente)

        # Si hay borrados y agregados, se actualiza la lista
        a_borrar = ids_actuales - ids_nuevos
        a_agregar = ids_nuevos - ids_actuales

        try:
            # Se eliminan los idiomas sobrantes en la BD
            ManejarDao.eliminar_relaciones_por_ids(id_docente, list(a_borrar))
            # Se agregan los idiomas faltantes en la BD
            diccionario_agregar = {id_idm: datos_finales[id_idm] for id_idm in a_agregar}
            ManejarDao.agregar_relaciones(id_docente, diccionario_agregar)

            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
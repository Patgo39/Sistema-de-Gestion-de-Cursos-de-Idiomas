
from datetime import datetime
from datetime import date
from db import db
from models import Docente
from models.alumno import Alumno
from models.usuario import Usuario
from dao.idioma_dao import IdiomaDao
from dao.dominar_dao import DominarDao


class AlumnoDao:

    @staticmethod
    def buscar_por_id(id_alumno: int) -> Alumno:
        alumno = Alumno.query.filter_by(id_usuario=id_alumno).first()
        return alumno

    @staticmethod
    def buscar_alumnos() -> list[Alumno]:
        alumnos = Alumno.query.all()
        return alumnos

    @staticmethod
    def eliminar_alumno(id_alumno: int) -> bool:
        alumno = AlumnoDao.buscar_por_id(id_alumno)

        if not alumno:
            raise Exception(f"No se encontró el alumno con id : {id_alumno}")
        try:
            usuario_eliminar = alumno.perfil_usuario
            db.session.delete(usuario_eliminar)
            db.session.commit()
            return True
        except:
            db.session.rollback()
            raise Exception(f"Error al eliminar el alumno con id : {id_alumno}")

    @staticmethod
    def actualizar_alumno(id_alumno: int, datos: dict[str, str]) -> None:
        """
        Se actualizan los datos del alumno.
        NO se puede modificar el rol ni la última fecha de acceso.
        :param id_alumno: El id del alumno a actualizar.
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
            grado_actual
        """
        alumno = AlumnoDao.buscar_por_id(id_alumno)

        if not alumno:
            raise Exception(f"No se encontró el alumno con id : {id_alumno}")

        if 'username' in datos and datos['username']:

            if datos['username'] is None or not str(datos['username']).strip():
                raise Exception("El username no puede ser vacio.")

            nuevo_username = datos['username']
            usuario_existente = Usuario.query.filter(
                Usuario.username == nuevo_username,
                Usuario.id_usuario != alumno.id_usuario
            ).first()

            if usuario_existente:
                raise Exception(f"El nombre de usuario '{nuevo_username}' ya está en uso por otra cuenta.")

        if 'email' in datos and datos['email']:
            if datos['email'] is not None and str(datos['email']).strip():
                nuevo_email = datos['email']
                usuario_email_existente = Usuario.query.filter(
                    Usuario.email == nuevo_email,
                    Usuario.id_usuario != alumno.id_usuario
                ).first()

                if usuario_email_existente:
                    raise Exception(f"El email {nuevo_email} ya esta en uso por otra cuenta.")

        try:
            if 'grado_actual' in datos:
                alumno.grado_actual = datos['grado_actual']
            usuario = alumno.perfil_usuario

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
    def actualizar_ultimo_acceso(id_alumno) -> None:
        alumno = AlumnoDao.buscar_por_id(id_alumno)
        if not alumno:
            raise Exception(f"No se encontró el alumno con id : {id_alumno}")

        usuario = alumno.perfil_usuario

        usuario.ultima_fecha_acceso = date.today()
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def actualizar_lista_idiomas(id_alumno: int, idiomas_input: dict[str, str]) -> None:
        """
        Recibe un diccionario de idioma, nivel y se compara con la lista actual de idiomas
        borrando o agregando idiomas.
        :param idiomas_input: Diccionario {'Ingles': 'Avanzado', 'Ruso': 'Básico'}
        """
        alumno = AlumnoDao.buscar_por_id(id_alumno)
        if not alumno:
            raise Exception(f"No se encontró el alumno con id : {id_alumno}")

        datos_finales = {}
        # Se hace un diccionario con id_idioma y nivel
        for nombre, nivel in idiomas_input.items():
            idm_obj = IdiomaDao.agregar_idioma(nombre)
            datos_finales[idm_obj.id_idioma] = nivel

        # Los ids nuevos son los recibidos en idiomas_input
        # Es posible que idiomas en idiomas_input ya estén asociados a alumno
        ids_nuevos = set(datos_finales.keys())
        ids_actuales = DominarDao.obtener_ids_por_alumno(id_alumno)

        # Si hay borrados y agregados, se actualiza la lista
        a_borrar = ids_actuales - ids_nuevos
        a_agregar = ids_nuevos - ids_actuales

        try:
            # Se eliminan los idiomas sobrantes en la BD
            DominarDao.eliminar_relaciones_por_ids(id_alumno, list(a_borrar))
            # Se agregan los idiomas faltantes en la BD
            diccionario_agregar = {id_idm: datos_finales[id_idm] for id_idm in a_agregar}
            DominarDao.agregar_relaciones(id_alumno, diccionario_agregar)

            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def buscar_por_atributos(filtros:dict[str, str]) -> list[Alumno]:
        """
        Se puede consultar por:
        id_usuario
        username
        nombre
        apellido_paterno
        apellido_materno
        email
        genero
        pais
        fecha_nacimiento_min
        fecha_nacimiento_max
        ultima_fecha_acceso_min
        ultima_fecha_acceso_max
        grado_actual
        """
        query = Alumno.query.join(Usuario, Alumno.id_usuario == Usuario.id_usuario)

        campos_alumno = ['grado_actual']

        campos_exactos_usuario = ['id_usuario', 'genero']

        campos_usuario = [
            'username', 'nombre', 'apellido_paterno',
            'apellido_materno', 'email', 'pais'
        ]

        for clave, valor in filtros.items():
            if not valor:
                continue


            if clave == 'fecha_nacimiento_min':
                query = query.filter(Usuario.fecha_nacimiento >= valor)
            if clave == 'fecha_nacimiento_max':
                query = query.filter(Usuario.fecha_nacimiento <= valor)

            if clave == 'ultima_fecha_acceso_min':
                query = query.filter(Usuario.ultima_fecha_acceso >= valor)
            if clave == 'ultima_fecha_acceso_max':
                query = query.filter(Usuario.ultima_fecha_acceso <= valor)

            if clave in campos_alumno:
                query = query.filter(getattr(Alumno, clave).ilike(f'%{valor}%'))

            elif clave in campos_usuario:
                query = query.filter(getattr(Usuario, clave).ilike(f'%{valor}%'))

            elif clave in campos_exactos_usuario:
                query = query.filter(getattr(Usuario, clave) == valor)

        return query.all()


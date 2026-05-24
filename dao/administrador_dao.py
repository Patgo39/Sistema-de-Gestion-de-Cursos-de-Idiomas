from db import db
from models.usuario import Usuario
from models.administrador import Administrador
from datetime import datetime
from datetime import date

class AdministradorDao:

    @staticmethod
    def crear_administrador(username, nombre, apellido_paterno, apellido_materno, email, fecha_nacimiento, password, genero, pais, nivel_privilegio):
        try:
            nuevo_usuario = Usuario(
                username=username,
                nombre=nombre,
                apellido_paterno=apellido_paterno,
                apellido_materno=apellido_materno,
                email=email,
                fecha_nacimiento=fecha_nacimiento,
                password=password,
                genero=genero,
                pais=pais,
                rol='Administrador'
            )
            db.session.add(nuevo_usuario)
            db.session.flush()

            nuevo_admin = Administrador(
                id_usuario=nuevo_usuario.id_usuario,
                nivel_privilegio=nivel_privilegio
            )
            db.session.add(nuevo_admin)
            db.session.commit()
            return nuevo_admin
        except Exception as e:
            db.session.rollback()
            print(f"Error, no se pudo crear el nuevo administrador: {e}")
            return None

    @staticmethod
    def obtener_por_id(id_usuario):
        # Cambio: de Administrador.query.get(id) a db.session.get(Administrador, id)
        return db.session.get(Administrador, id_usuario)

    @staticmethod
    def obtener_todos():
        # Nota: query.all() sigue funcionando, pero en 2.0 se prefiere db.session.execute(select(Administrador)).scalars().all()
        # Por ahora, para no complicar el código, query.all() es aceptable y no genera tanto ruido.
        return Administrador.query.all()

    @staticmethod
    def actualizar_administrador(id_usuario: int, datos: dict) -> bool:
        try:
            # Cambio: Uso de db.session.get
            admin = db.session.get(Administrador, id_usuario)
            if not admin:
                return False

            usuario = db.session.get(Usuario, id_usuario)

            campos_usuario = [
                'username', 'nombre', 'apellido_paterno', 'apellido_materno',
                'email', 'password', 'genero', 'pais', 'fecha_nacimiento'
            ]

            campos_admin = ['nivel_privilegio']

            if 'username' in datos and datos['username']:

                if datos['username'] is None or not str(datos['username']).strip():
                    raise Exception("El username no puede ser vacio.")

                nuevo_username = datos['username']
                usuario_existente = Usuario.query.filter(
                    Usuario.username == nuevo_username,
                    Usuario.id_usuario != admin.id_usuario
                ).first()

                if usuario_existente:
                    raise Exception(f"El nombre de usuario '{nuevo_username}' ya está en uso por otra cuenta.")

            for campo in campos_usuario:
                if campo in datos:
                    setattr(usuario, campo, datos[campo])

            for campo in campos_admin:
                if campo in datos:
                    setattr(admin, campo, datos[campo])

            db.session.commit()
            return True

        except Exception as e:
            db.session.rollback()
            print(f"Error al actualizar el administrador: {e}")
            raise e

    @staticmethod
    def eliminar_administrador(id_usuario):
        try:
            # Cambio: Uso de db.session.get
            admin = db.session.get(Administrador, id_usuario)
            if admin:
                usuario = db.session.get(Usuario, id_usuario)
                db.session.delete(usuario)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            print(f"Error al eliminar administrador: {e}")
            return False

    @staticmethod
    def actualizar_ultimo_acceso(id_usuario) -> None:
        admin = AdministradorDao.obtener_por_id(id_usuario)
        if not admin:
            raise Exception(f"No se encontró el administrador con id : {id_usuario}")

        usuario = admin.perfil_usuario

        usuario.ultima_fecha_acceso = date.today()
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

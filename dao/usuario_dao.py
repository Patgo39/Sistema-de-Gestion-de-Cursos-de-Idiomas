from db import db
from models.usuario import Usuario
from models.alumno import Alumno
from models.docente import Docente
from models.administrador import Administrador
class UsuarioDao:
    @staticmethod
    def registrar_alumno(username, nombre, apellido_paterno, apellido_materno, email, fecha_nacimiento, password, genero, pais, grado_actual):
        '''
        Registra un alumno en la base de datos
        :param username: usuario del alumno
        :param nombre: nombre del alumno
        :param apellido_paterno:  apellido paterno del alumno
        :param apellido_materno: apellido materno del alumno
        :param email: correo del alumno
        :param fecha_nacimiento: fecha de nacimiento del alumno
        :param password: Contraseña del alumno (8 caracteres) del usuario)
        :param genero: genero del alumno
        :param pais: pais del alumno
        :param grado_actual:  Grado actual del alumno
        :return: Bool si registro el nuevo alumno
        '''
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
                rol='Alumno'
            )
            db.session.add(nuevo_usuario)
            db.session.flush()
            nuevo_alumno = Alumno(id_usuario=nuevo_usuario.id_usuario, grado_actual=grado_actual)
            db.session.add(nuevo_alumno)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error al registar nuevo usuario: {e}")
            return False
    @staticmethod
    def registrar_docente(username, nombre, apellido_paterno, apellido_materno, email, fecha_nacimiento, password,genero, pais,tiempo_experiencia,especialidad):
        '''
        Registra un docente en la base de datos
        :param username: usuario del docente
        :param nombre:  nombre del docente
        :param apellido_paterno:  apellido paterno
        :param apellido_materno:  apellido materno
        :param email:  correo del docente
        :param fecha_nacimiento: fecha de nacimiento del docente
        :param password: Contraseña (8 caracteres) del usuario)
        :param genero: genero del docente
        :param pais: pais del docente
        :param tiempo_experiencia: Años de experiencia del docente(Int )
        :param especialidad: Idioma del especialidad
        :return: Bool si registrado el nuevo docente
        '''
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
                rol='Docente'
            )
            db.session.add(nuevo_usuario)
            db.session.flush()
            nuevo_docente = Docente(
                id_usuario=nuevo_usuario.id_usuario,
                tiempo_experiencia=tiempo_experiencia,
                especialidad=especialidad
            )
            db.session.add(nuevo_docente)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error al registar nuevo docente: {e}")
            return False
    @staticmethod
    def registrar_administrador(username, nombre, apellido_paterno, apellido_materno, email, fecha_nacimiento, password,
                                genero, pais, nivel_privilegio):
        '''
        Registra un administrador en la base de datos
        :param username: username del administrador
        :param nombre:  nombre del administrador
        :param apellido_paterno:  apellido paterno
        :param apellido_materno:  apellido materno
        :param email: correo del administrador
        :param fecha_nacimiento: fecha de nacimiento del administrador
        :param password: Contraseña (8 caracteres) del administrador)
        :param genero: genero del administrador
        :param pais: pais del administrador
        :param nivel_privilegio:  nivel de privilegio(Int )
        :return: Bool si se registro el nuevo administrador
        '''
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
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error al registrar nuevo administrador: {e}")
            return False

    @staticmethod
    def buscar_por_id(id_usuario):
        '''
        Busca un id de usuario en la base de datos
        :param id_usuario: id del usuario
        :return: usuario en la base de datos
        '''
        return Usuario.query.get(id_usuario)

    @staticmethod
    def obtener_todos():
        '''
        Obtener todos los registros de usuarios
        :return:  todos los registros de usuarios
        '''
        return Usuario.query.all()

    @staticmethod
    def obtener_usuarios_por_rol(rol):
        '''
        Obtener todos los registros de usuarios por rol
        :param rol:  rol del usuario
        :return:  todos los registros de usuarios por rol
        '''
        return Usuario.query.filter_by(rol=rol).all()

    @staticmethod
    def actualizar_perfil_basico(id_usuario, datos):
        '''
        Actualiza un usuario en la base de datos
        :param id_usuario:  id_usuario del usuario
        :param datos: Diccionario con los datos del usuario
        :return:  Bool si se actualiza el usuario en la base de datos
        '''
        try:
            usuario = Usuario.query.get(id_usuario)
            if usuario:
                for clave, valor in datos.items():
                    if hasattr(usuario, clave):
                        setattr(usuario, clave, valor)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            print(f"Error al actualizar usuario: {e}")
            return False

    @staticmethod
    def eliminar_usuario(id_usuario):
        '''
        Elimina el usuario con el id_usuario
        :param id_usuario: id_usuario del usuario
        :return:  Bool si se elimino el usuario en la base de datos
        '''
        try:
            usuario = Usuario.query.get(id_usuario)
            if usuario:
                db.session.delete(usuario)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            print(f"Error al eliminar: {e}")
            return False
    @staticmethod
    def verificar_login(username, password):
        '''
        Verifica si el usuario existe en la base de datos
        :param username:  Usuario del usuario
        :param password:  contraseni del usuario
        :return:  Bool si existe el usuario en la base de datos
        '''
        try:
            usuario=Usuario.query.filter_by(username=username).first()
            if usuario and usuario.password == password:
                return usuario
            else:
                return None
        except Exception as e:
            print(f"Error al verificar login: {e}")
            return False

    @staticmethod
    def existe_username(username):
        '''
        Verifica si un nombre de usuario ya existe en la base de datos
        :param username: El nombre de usuario a verificar
        :return: Bool (True si ya existe, False si está libre)
        '''
        try:
            usuario = Usuario.query.filter_by(username=username).first()
            return usuario is not None
        except Exception as e:
            print(f"Error al verificar duplicado de username: {e}")
            return False

    @staticmethod
    def existe_email(email):
        '''
        Verifica si un correo electrónico ya existe en la base de datos
        :param email: El correo electrónico a verificar
        :return: Bool (True si ya existe, False si está libre)
        '''
        try:
            usuario = Usuario.query.filter_by(email=email).first()
            return usuario is not None
        except Exception as e:
            print(f"Error al verificar duplicado de email: {e}")
            return False









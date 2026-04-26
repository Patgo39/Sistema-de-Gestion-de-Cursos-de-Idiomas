from db import db
from models.usuario import Usuario
from models.alumno import Alumno
from models.docente import Docente
from models.administrador import Administrador
class UsuarioDao:
    @staticmethod
    def registrar_alumno(username, nombre, apellido_paterno, apellido_materno, email, fecha_nacimiento, password, genero, pais, grado_actual):
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
                rol='docente'
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
                rol='administrador'
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
    def verificar_login(username, password):
        try:
            usuario=Usuario.query.filter_by(username=username).first()
            if usuario and usuario.password == password:
                return usuario
            else:
                return None
        except Exception as e:
            print(f"Error al verificar login: {e}")
            return False







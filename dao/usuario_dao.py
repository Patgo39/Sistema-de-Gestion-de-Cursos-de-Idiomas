from db import db
from models.usuario import Usuario
from models.alumno import Alumno
from models.docente import Docente

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
                rol='alumno'
            )
            db.session.add(nuevo_usuario)
            db.session.flush()
            nuevo_alumno = Alumno(id_usuario=nuevo_usuario.id_usuario, grado_actual=grado_actual)
            db.session.add(nuevo_alumno)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Erro  al registar nuevo usuario: {e}")
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
                pais=pais
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
            print(f"Erro  al registar nuevo docente: {e}")
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
            print(f"Erro  al verificar login: {e}")
            return False







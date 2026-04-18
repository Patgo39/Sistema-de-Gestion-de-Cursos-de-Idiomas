import pytest
from datetime import date
from dao.usuario_dao import UsuarioDao
from models.usuario import Usuario
from models.alumno import Alumno
from models.docente import Docente

def test_registrar_alumno_flujo_completo(app, db):
    with app.app_context():
        res = UsuarioDao.registrar_alumno(
            username="estudiante1",
            nombre="Carlos",
            apellido_paterno="Santana",
            apellido_materno="López",
            email="carlos@correo.com",
            fecha_nacimiento=date(2000, 1, 1),
            password="hash_password_seguro",
            genero="Masculino",
            pais="México",
            grado_actual="3er Semestre"
        )

        assert res is True

        usuario = Usuario.query.filter_by(username="estudiante1").first()
        assert usuario is not None
        assert usuario.rol == 'alumno'

        alumno = Alumno.query.filter_by(id_usuario=usuario.id_usuario).first()
        assert alumno is not None
        assert alumno.grado_actual == "3er Semestre"


def test_registrar_docente_exitoso(app, db):
    with app.app_context():
        # Datos para el docente
        params = {
            "username": "profesor_x",
            "nombre": "Charles",
            "apellido_paterno": "Xavier",
            "apellido_materno": "Mansion",
            "email": "charles@mansion.com",
            "fecha_nacimiento": date(1970, 5, 20),
            "password": "telepatia123",
            "genero": "Masculino",
            "pais": "USA",
            "tiempo_experiencia": 20,
            "especialidad": "Ingles"
        }

        exito = UsuarioDao.registrar_docente(**params)

        assert exito is True

        u = Usuario.query.filter_by(username="profesor_x").first()
        assert u is not None

        d = Docente.query.filter_by(id_usuario=u.id_usuario).first()
        assert d is not None
        assert d.especialidad == "Ingles"
        assert d.tiempo_experiencia == 20


def test_verificar_login_exitoso(app, db):
    with app.app_context():

        user = Usuario(username="login_test", password="secret_password", email="login@test.com")
        db.session.add(user)
        db.session.commit()


        resultado = UsuarioDao.verificar_login("login_test", "secret_password")
        assert resultado is not None
        assert resultado.username == "login_test"


def test_verificar_login_fallido(app, db):
    with app.app_context():

        user = Usuario(username="user_fail", password="correct_password", email="fail@test.com")
        db.session.add(user)
        db.session.commit()

        res_pass_wrong = UsuarioDao.verificar_login("user_fail", "wrong_password")
        assert res_pass_wrong is None


        res_no_user = UsuarioDao.verificar_login("inexistente", "123")
        assert res_no_user is None


def test_registrar_alumno_rollback_si_falla(app, db):
    with app.app_context():
        resultado = UsuarioDao.registrar_alumno(
            username=None,
            nombre="Error",
            apellido_paterno="Test",
            apellido_materno="Test",
            email="error@test.com",
            fecha_nacimiento=None,
            password="123",
            genero="X",
            pais="Test",
            grado_actual="Ninguno"
        )

        assert resultado is False
        assert Usuario.query.count() == 0

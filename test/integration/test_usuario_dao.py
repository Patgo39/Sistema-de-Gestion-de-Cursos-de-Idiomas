import pytest
from datetime import date
from dao.usuario_dao import UsuarioDao
from models.usuario import Usuario
from models.alumno import Alumno
from models.docente import Docente
from models.administrador import Administrador

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
        assert usuario.rol == 'Alumno'

        alumno = Alumno.query.filter_by(id_usuario=usuario.id_usuario).first()
        assert alumno is not None
        assert alumno.grado_actual == "3er Semestre"


def test_registrar_docente_exitoso(app, db):
    with app.app_context():
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

def test_registrar_administrador(app, db):
    with app.app_context():
        resultado = UsuarioDao.registrar_administrador(
            username="admin_01",
            nombre="Carlos",
            apellido_paterno="Ruiz",
            apellido_materno="Mora",
            email="admin@test.com",
            fecha_nacimiento=date(1980, 1, 15),
            password="adminpass",
            genero="Masculino",
            pais="Argentina",
            nivel_privilegio=1
        )

        assert resultado is True

        usuario_db = Usuario.query.filter_by(username="admin_01").first()
        assert usuario_db is not None
        assert usuario_db.rol == 'administrador'

        admin_db = Administrador.query.filter_by(id_usuario=usuario_db.id_usuario).first()
        assert admin_db is not None
        assert admin_db.nivel_privilegio == 1


def test_verificar_login_exitoso(app, db):
    with app.app_context():
        user = Usuario(username="login_test", password="secret_password", email="login@test.com", rol="alumno")
        db.session.add(user)
        db.session.commit()


        resultado = UsuarioDao.verificar_login("login_test", "secret_password")
        assert resultado is not None
        assert resultado.username == "login_test"


def test_verificar_login_fallido(app, db):
    with app.app_context():
        user = Usuario(username="user_fail", password="correct_password", email="fail@test.com", rol="Alumno")
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


def test_buscar_por_id(app, db):
    with app.app_context():
        usuario_nuevo = Usuario(
            username="busqueda_id", nombre="Ana", apellido_paterno="Gomez",
            email="ana.id@test.com", password="123", rol="Alumno"
        )
        db.session.add(usuario_nuevo)
        db.session.commit()

        usuario_encontrado = UsuarioDao.buscar_por_id(usuario_nuevo.id_usuario)

        assert usuario_encontrado is not None
        assert usuario_encontrado.id_usuario == usuario_nuevo.id_usuario
        assert usuario_encontrado.username == "busqueda_id"


def test_buscar_por_username(app, db):
    with app.app_context():
        usuario_nuevo = Usuario(
            username="busqueda_user", nombre="Beto", apellido_paterno="Perez",
            email="beto.user@test.com", password="123", rol="Docente"
        )
        db.session.add(usuario_nuevo)
        db.session.commit()

        usuario_encontrado = UsuarioDao.buscar_por_username("busqueda_user")
        usuario_no_existe = UsuarioDao.buscar_por_username("no_existo_123")

        assert usuario_encontrado is not None
        assert usuario_encontrado.username == "busqueda_user"
        assert usuario_no_existe is None


def test_obtener_todos(app, db):
    with app.app_context():
        u1 = Usuario(username="todos_1", email="t1@test.com", password="123", rol="Alumno")
        u2 = Usuario(username="todos_2", email="t2@test.com", password="123", rol="Docente")
        db.session.add_all([u1, u2])
        db.session.commit()

        usuarios = UsuarioDao.obtener_todos()

        assert len(usuarios) >= 2
        usernames = [u.username for u in usuarios]
        assert "todos_1" in usernames
        assert "todos_2" in usernames


def test_obtener_usuarios_por_rol(app, db):
    with app.app_context():
        u1 = Usuario(username="rol_alum", email="alum@test.com", password="123", rol="Alumno")
        u2 = Usuario(username="rol_doc", email="doc@test.com", password="123", rol="Docente")
        db.session.add_all([u1, u2])
        db.session.commit()

        alumnos = UsuarioDao.obtener_usuarios_por_rol("Alumno")
        docentes = UsuarioDao.obtener_usuarios_por_rol("Docente")

        assert len(alumnos) >= 1
        assert alumnos[-1].rol == "Alumno"

        assert len(docentes) >= 1
        assert docentes[-1].rol == "Docente"


def test_actualizar_perfil_basico(app, db):
    with app.app_context():
        usuario_actualizar = Usuario(
            username="user_act", nombre="Original", pais="Mexico",
            email="act@test.com", password="123", rol="Alumno"
        )
        db.session.add(usuario_actualizar)
        db.session.commit()

        datos_nuevos = {
            "nombre": "Actualizado",
            "pais": "España"
        }
        resultado = UsuarioDao.actualizar_perfil_basico(usuario_actualizar.id_usuario, datos_nuevos)

        assert resultado is True

        usuario_db = Usuario.query.get(usuario_actualizar.id_usuario)
        assert usuario_db.nombre == "Actualizado"
        assert usuario_db.pais == "España"


def test_eliminar_usuario(app, db):
    with app.app_context():
        usuario_eliminar = Usuario(
            username="user_eliminar", email="eliminar@test.com", password="123", rol="Alumno"
        )
        db.session.add(usuario_eliminar)
        db.session.commit()
        id_borrar = usuario_eliminar.id_usuario

        resultado = UsuarioDao.eliminar_usuario(id_borrar)

        assert resultado is True
        assert Usuario.query.get(id_borrar) is None


def test_existe_username(app, db):
    with app.app_context():
        usuario = Usuario(username="username_unico", email="unico@test.com", password="123", rol="Alumno")
        db.session.add(usuario)
        db.session.commit()

        assert UsuarioDao.existe_username("username_unico") is True
        assert UsuarioDao.existe_username("username_no_existe") is False


def test_existe_email(app, db):
    with app.app_context():
        usuario = Usuario(username="test_email", email="email_unico@test.com", password="123", rol="Alumno")
        db.session.add(usuario)
        db.session.commit()

        assert UsuarioDao.existe_email("email_unico@test.com") is True
        assert UsuarioDao.existe_email("email_falso@test.com") is False

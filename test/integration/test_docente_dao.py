import pytest
from app import app, db
from models.usuario import Usuario
from models.docente import Docente
from models.manejar import Manejar
from models.idioma import Idioma
from dao.docente_dao import DocenteDao
from datetime import date

class TestDocenteDao:

    # Crea y elimina la BD provisional para los tests.
    @pytest.fixture(autouse=True)
    def config_test_db(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True

        with app.app_context():
            db.create_all()
            yield
            db.session.remove()
            db.drop_all()

    @pytest.fixture
    def docente_test(self):
        with app.app_context():
            usuario = Usuario(
                username="testuser",
                nombre="Juan",
                apellido_paterno="Perez",
                apellido_materno="Alcantara",
                email="juan@test.com",
                password="hash",
                genero="M",
                pais="México",
                fecha_nacimiento=date(2000, 12, 9),
                ultima_fecha_acceso=date.today(),
                rol="Docente"
            )
            db.session.add(usuario)
            db.session.commit()

            docente = Docente(
                id_usuario=usuario.id_usuario,
                tiempo_experiencia=8,
                especialidad="Lenguas extranjeras")
            db.session.add(docente)
            db.session.commit()
            return docente


    def test_buscar_por_id(self, docente_test):
        with app.app_context():
            id_erroneo = docente_test.id_usuario + 1
            docente = DocenteDao.buscar_por_id(id_erroneo)
            assert docente is None

            docente = DocenteDao.buscar_por_id(docente_test.id_usuario)
            assert docente is not None
            assert docente.perfil_usuario.nombre == "Juan"
            assert docente.perfil_usuario.username == "testuser"
            assert docente.perfil_usuario.password == "hash"
            assert docente.especialidad == "Lenguas extranjeras"


    def test_actualizar_docente(self, docente_test):
        with app.app_context():
            nuevos_datos = {
                "nombre": "Pedro",
                "username" : "test_pedrito",
                "fecha_nacimiento": "1995-01-01",
                "especialidad" : "Traducción",
                "rol" : "Alumno"
            }

            id_usuario = docente_test.id_usuario
            id_erroneo = id_usuario + 1

            try:
                DocenteDao.actualizar_docente(id_erroneo, nuevos_datos)
            except Exception as e:
                assert True

            try:
                DocenteDao.actualizar_docente(docente_test.id_usuario, nuevos_datos)
                docente_upd = DocenteDao.buscar_por_id(id_usuario)

                assert docente_upd is not None
                assert docente_upd.perfil_usuario.nombre == "Pedro"
                assert docente_upd.perfil_usuario.username == "test_pedrito"
                assert docente_upd.perfil_usuario.fecha_nacimiento == "1995-01-01"
                assert docente_upd.perfil_usuario.rol != "Alumno"
                assert docente_upd.especialidad == "Traducción"

            except Exception as e:
                assert False



import pytest
from models.docente import Docente
from models.manejar import Manejar
from models.idioma import Idioma
from dao.idioma_dao import IdiomaDao
from models.usuario import Usuario
from dao.docente_dao import DocenteDao
from datetime import date

class TestDocenteDao:

    @pytest.fixture
    def docente_test(self, app, db):
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
            db.session.refresh(docente)
            db.session.expunge(docente)
            return docente


    def test_buscar_por_id(self, app, docente_test):
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


    def test_actualizar_docente(self, app, docente_test):
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
                assert docente_upd.perfil_usuario.fecha_nacimiento == date(1995, 1, 1)
                assert docente_upd.perfil_usuario.rol == "Docente"
                assert docente_upd.especialidad == "Traducción"

            except Exception as e:
                assert False


    def test_actualizar_idiomas(self, app, docente_test):
        with app.app_context():

            IdiomaDao.agregar_idioma("Inglés")
            IdiomaDao.agregar_idioma("Francés")
            IdiomaDao.agregar_idioma("Ruso")

            id_docente = docente_test.id_usuario


            # Agregar idiomas
            idiomas = {
                "Inglés" : "Avanzado",
                "Francés" : "Básico"
            }

            DocenteDao.actualizar_lista_idiomas(id_docente, idiomas)
            docente_upd = DocenteDao.buscar_por_id(id_docente)
            idiomas_docente = docente_upd.idiomas_manejados.all()

            assert idiomas_docente is not None
            assert len(idiomas_docente) == 2
            assert idiomas_docente[0].idioma.nombre_idioma == "INGLÉS"
            assert idiomas_docente[0].nivel_dominio == "Avanzado"
            assert idiomas_docente[1].idioma.nombre_idioma == "FRANCÉS"
            assert idiomas_docente[1].nivel_dominio == "Básico"

            #Actualizar idiomas
            idiomas.update({"Ruso" : "Básico"})

            DocenteDao.actualizar_lista_idiomas(id_docente, idiomas)
            docente_upd = DocenteDao.buscar_por_id(id_docente)
            idiomas_docente = docente_upd.idiomas_manejados.all()

            assert idiomas_docente is not None
            assert len(idiomas_docente) == 3
            assert idiomas_docente[0].idioma.nombre_idioma == "INGLÉS"
            assert idiomas_docente[0].nivel_dominio == "Avanzado"
            assert idiomas_docente[1].idioma.nombre_idioma == "FRANCÉS"
            assert idiomas_docente[1].nivel_dominio == "Básico"
            assert idiomas_docente[2].idioma.nombre_idioma == "RUSO"
            assert idiomas_docente[2].nivel_dominio == "Básico"

            #Eliminar idiomas
            idiomas = {
                "Inglés": "Avanzado",
                "Ruso": "Básico"
            }

            DocenteDao.actualizar_lista_idiomas(id_docente, idiomas)
            docente_upd = DocenteDao.buscar_por_id(id_docente)
            idiomas_docente = docente_upd.idiomas_manejados.all()

            assert idiomas_docente is not None
            assert len(idiomas_docente) == 2
            assert idiomas_docente[0].idioma.nombre_idioma == "INGLÉS"
            assert idiomas_docente[0].nivel_dominio == "Avanzado"
            assert idiomas_docente[1].idioma.nombre_idioma == "RUSO"
            assert idiomas_docente[1].nivel_dominio == "Básico"

    def test_actualizar_ultimo_acceso(self, app, docente_test):
        with app.app_context():
            DocenteDao.actualizar_ultimo_acceso(docente_test.id_usuario)
            docente_upd = DocenteDao.buscar_por_id(docente_test.id_usuario)
            assert docente_upd.perfil_usuario.ultima_fecha_acceso.date() == date.today()

    def test_buscar_por_atributos(self, app, docente_test):
        with app.app_context():
            filtros_nombre = {"nombre": "Juan"}
            resultados = DocenteDao.buscar_por_atributos(filtros_nombre)
            assert len(resultados) >= 1
            assert resultados[0].perfil_usuario.nombre == "Juan"

            filtros_esp = {"especialidad": "Lenguas extranjeras"}
            resultados = DocenteDao.buscar_por_atributos(filtros_esp)
            assert len(resultados) >= 1
            assert resultados[0].especialidad == "Lenguas extranjeras"

            filtros_comb = {
                "pais": "México",
                "tiempo_experiencia": 8
            }
            resultados = DocenteDao.buscar_por_atributos(filtros_comb)
            assert len(resultados) >= 1
            assert resultados[0].perfil_usuario.pais == "México"
            assert resultados[0].tiempo_experiencia == 8

            filtros_vacios = {"nombre": "NombreInexistente"}
            resultados = DocenteDao.buscar_por_atributos(filtros_vacios)
            assert len(resultados) == 0

            filtros_id = {"id_usuario": docente_test.id_usuario}
            resultados = DocenteDao.buscar_por_atributos(filtros_id)
            assert len(resultados) == 1
            assert resultados[0].id_usuario == docente_test.id_usuario

    def test_eliminar_docente(self, app, docente_test):
        with app.app_context():
            id_docente = docente_test.id_usuario

            valor = DocenteDao.eliminar_docente(id_docente)

            docente_upd = DocenteDao.buscar_por_id(id_docente)

            assert docente_upd is None

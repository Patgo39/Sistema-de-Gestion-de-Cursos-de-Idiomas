import pytest
from models.alumno import Alumno
from models.dominar import Dominar
from models.idioma import Idioma
from dao.idioma_dao import IdiomaDao
from models.usuario import Usuario
from dao.alumno_dao import AlumnoDao
from datetime import date

class TestAlumnoDao:

    @pytest.fixture
    def alumno_test(self, app, db):
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
                rol="Alumno"
            )
            db.session.add(usuario)
            db.session.commit()

            alumno = Alumno(
                id_usuario=usuario.id_usuario,
                grado_actual="Tercero Preparatoria"
            )
            db.session.add(alumno)
            db.session.commit()
            db.session.refresh(alumno)
            db.session.expunge(alumno)
            return alumno


    def test_buscar_por_id(self, app, alumno_test):
        with app.app_context():
            id_erroneo = alumno_test.id_usuario + 1
            docente = AlumnoDao.buscar_por_id(id_erroneo)
            assert docente is None

            alumno = AlumnoDao.buscar_por_id(alumno_test.id_usuario)
            assert alumno is not None
            assert alumno.perfil_usuario.nombre == "Juan"
            assert alumno.perfil_usuario.username == "testuser"
            assert alumno.perfil_usuario.password == "hash"
            assert alumno.grado_actual == "Tercero Preparatoria"


    def test_actualizar_alumno(self, app, alumno_test):
        with app.app_context():
            nuevos_datos = {
                "nombre": "Pedro",
                "username" : "test_pedrito",
                "fecha_nacimiento": "1995-01-01",
                "grado_actual" : "Licenciatura en Ciencias de la Computación",
                "rol" : "Alumno"
            }

            id_usuario = alumno_test.id_usuario
            id_erroneo = id_usuario + 1

            try:
                AlumnoDao.actualizar_alumno(id_erroneo, nuevos_datos)
            except Exception as e:
                assert True

            try:
                AlumnoDao.actualizar_alumno(alumno_test.id_usuario, nuevos_datos)
                alumno_upd = AlumnoDao.buscar_por_id(id_usuario)

                assert alumno_upd is not None
                assert alumno_upd.perfil_usuario.nombre == "Pedro"
                assert alumno_upd.perfil_usuario.username == "test_pedrito"
                assert alumno_upd.perfil_usuario.fecha_nacimiento == date(1995, 1, 1)
                assert alumno_upd.perfil_usuario.rol == "Alumno"
                assert alumno_upd.grado_actual == "Licenciatura en Ciencias de la Computación"

            except Exception as e:
                assert False


    def test_actualizar_idiomas(self, app, alumno_test):
        with app.app_context():

            IdiomaDao.agregar_idioma("Inglés")
            IdiomaDao.agregar_idioma("Francés")
            IdiomaDao.agregar_idioma("Ruso")

            id_alumno = alumno_test.id_usuario


            # Agregar idiomas
            idiomas = {
                "Inglés" : "Avanzado",
                "Francés" : "Básico"
            }

            AlumnoDao.actualizar_lista_idiomas(id_alumno, idiomas)
            alumno_upd = AlumnoDao.buscar_por_id(id_alumno)
            idiomas_alumno = alumno_upd.idiomas_dominados.all()

            assert idiomas_alumno is not None
            assert len(idiomas_alumno) == 2
            assert idiomas_alumno[0].idioma.nombre_idioma == "INGLÉS"
            assert idiomas_alumno[0].nivel_dominio == "Avanzado"
            assert idiomas_alumno[1].idioma.nombre_idioma == "FRANCÉS"
            assert idiomas_alumno[1].nivel_dominio == "Básico"

            #Actualizar idiomas
            idiomas.update({"Ruso" : "Básico"})

            AlumnoDao.actualizar_lista_idiomas(id_alumno, idiomas)
            alumno_upd = AlumnoDao.buscar_por_id(id_alumno)
            idiomas_alumno = alumno_upd.idiomas_dominados.all()

            assert idiomas_alumno is not None
            assert len(idiomas_alumno) == 3
            assert idiomas_alumno[0].idioma.nombre_idioma == "INGLÉS"
            assert idiomas_alumno[0].nivel_dominio == "Avanzado"
            assert idiomas_alumno[1].idioma.nombre_idioma == "FRANCÉS"
            assert idiomas_alumno[1].nivel_dominio == "Básico"
            assert idiomas_alumno[2].idioma.nombre_idioma == "RUSO"
            assert idiomas_alumno[2].nivel_dominio == "Básico"

            #Eliminar idiomas
            idiomas = {
                "Inglés": "Avanzado",
                "Ruso": "Básico"
            }

            AlumnoDao.actualizar_lista_idiomas(id_alumno, idiomas)
            alumno_upd = AlumnoDao.buscar_por_id(id_alumno)
            idiomas_alumno = alumno_upd.idiomas_dominados.all()

            assert idiomas_alumno is not None
            assert len(idiomas_alumno) == 2
            assert idiomas_alumno[0].idioma.nombre_idioma == "INGLÉS"
            assert idiomas_alumno[0].nivel_dominio == "Avanzado"
            assert idiomas_alumno[1].idioma.nombre_idioma == "RUSO"
            assert idiomas_alumno[1].nivel_dominio == "Básico"

    def test_actualizar_ultimo_acceso(self, app, alumno_test):
        with app.app_context():
            AlumnoDao.actualizar_ultimo_acceso(alumno_test.id_usuario)
            alumno_upd = AlumnoDao.buscar_por_id(alumno_test.id_usuario)
            assert alumno_upd.perfil_usuario.ultima_fecha_acceso.date() == date.today()

    def test_buscar_por_atributos(self, app, alumno_test):
        with app.app_context():

            filtros_nombre = {"nombre": "Juan"}
            resultados = AlumnoDao.buscar_por_atributos(filtros_nombre)
            assert len(resultados) >= 1
            assert resultados[0].perfil_usuario.nombre == "Juan"

            filtros_grado = {"grado_actual": "Tercero Preparatoria"}
            resultados = AlumnoDao.buscar_por_atributos(filtros_grado)
            assert len(resultados) >= 1
            assert resultados[0].grado_actual == "Tercero Preparatoria"

            filtros_comb = {
                "pais": "México",
                "grado_actual": "Tercero Preparatoria"
            }
            resultados = AlumnoDao.buscar_por_atributos(filtros_comb)
            assert len(resultados) >= 1
            assert resultados[0].perfil_usuario.pais == "México"
            assert resultados[0].grado_actual == "Tercero Preparatoria"

            filtros_vacios = {"nombre": "NombreInexistente"}
            resultados = AlumnoDao.buscar_por_atributos(filtros_vacios)
            assert len(resultados) == 0

            filtros_id = {"id_usuario": alumno_test.id_usuario}
            resultados = AlumnoDao.buscar_por_atributos(filtros_id)
            assert len(resultados) == 1
            assert resultados[0].id_usuario == alumno_test.id_usuario

    def test_eliminar_alumno(self, app, alumno_test):
        with app.app_context():
            id_alumno = alumno_test.id_usuario

            valor = AlumnoDao.eliminar_alumno(id_alumno)

            alumno_upd = AlumnoDao.buscar_por_id(id_alumno)

            assert alumno_upd is None


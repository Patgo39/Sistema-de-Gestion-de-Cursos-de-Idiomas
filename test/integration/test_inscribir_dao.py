import pytest
from dao.inscribir_dao import InscribirDao
from models import Usuario, Alumno, Curso, Docente, Idioma, Inscribir


class TestInscribirDao:
    @pytest.fixture
    def inscribir_test(self, app, db):
        with app.app_context():
            #creamos el primer alumno
            usuario1 = Usuario(
                username="testuser1",
                nombre="Juan",
                apellido_paterno="Perez",
                apellido_materno="Alcantara",
                email="juan@test.com",
                password="password",
                genero="M",
                rol="Alumno"
            )
            db.session.add(usuario1)
            db.session.commit()

            alumno1 = Alumno(
                id_usuario = usuario1.id_usuario,
                grado_actual = "Tercero Preparatoria"
            )
            db.session.add(alumno1)
            db.session.commit()

            # creamos el segundo alumno
            usuario2 = Usuario(
                username="testuser2",
                nombre="Juana",
                apellido_paterno="Perez",
                apellido_materno="Alcantara",
                email="juana@test.com",
                password="password",
                genero="F",
                rol="Alumno"
            )
            db.session.add(usuario2)
            db.session.commit()

            alumno2 = Alumno(
                id_usuario=usuario2.id_usuario,
                grado_actual="Tercero Preparatoria"
            )
            db.session.add(alumno2)
            db.session.commit()

            #creamos el docente
            usuario = Usuario(
                username="testuserdocente",
                nombre="Ana",
                apellido_paterno="Lopez",
                apellido_materno="Canal",
                email="ana@test.com",
                password="password",
                genero="F",
                rol="Docente"
            )
            db.session.add(usuario)
            db.session.commit()

            docente = Docente(
                id_usuario = usuario.id_usuario
            )
            db.session.add(docente)
            db.session.commit()

            #creamos el idioma
            idioma = Idioma(
                nombre_idioma = "Francés"
            )
            db.session.add(idioma)
            db.session.commit()

            #creamos el curso
            curso = Curso(
                id_idioma=idioma.id_idioma,
                id_usuario=docente.id_usuario,
                nombre_curso="Francés II"
            )
            db.session.add(curso)
            db.session.commit()

            #Sincronizamos la sesión
            db.session.refresh(alumno1)
            db.session.refresh(alumno2)
            db.session.refresh(docente)
            db.session.refresh(curso)

            db.session.expunge(alumno1)
            db.session.expunge(alumno2)
            db.session.expunge(docente)
            db.session.expunge(curso)
            return {"alumno1": alumno1, "alumno2": alumno2, "docente": docente, "curso": curso}

    def test_crear_inscripcion(self, app, inscribir_test):
        alumno = inscribir_test["alumno1"]
        curso = inscribir_test["curso"]

        with app.app_context():
            # caso inscribir alumno a un curso
            InscribirDao.crear_inscripcion(alumno.id_usuario, curso.id_curso)

            inscripcion = Inscribir.query.filter_by(
                id_alumno=alumno.id_usuario,
                id_curso=curso.id_curso
            ).first()
            assert inscripcion is not None
            assert inscripcion.id_alumno == alumno.id_usuario
            assert inscripcion.id_curso == curso.id_curso

            # caso consultar que un alumno no tenga doble inscripcion al mismo curso
            InscribirDao.crear_inscripcion(alumno.id_usuario, curso.id_curso)

            inscripciones = Inscribir.query.filter_by(
                id_alumno=alumno.id_usuario,
                id_curso=curso.id_curso
            ).all()
            assert len(inscripciones) == 1

    def test_consultar_alumno_inscripcion(self, app, inscribir_test):
        alumno = inscribir_test["alumno1"]
        curso = inscribir_test["curso"]

        with app.app_context():
            # caso consultar datos de un alumno no inscrito
            resultado = InscribirDao.consultar_alumno_inscripcion(alumno.id_usuario, curso.id_curso)
            assert resultado is None

            InscribirDao.crear_inscripcion(alumno.id_usuario, curso.id_curso)

            # caso consultar datos de un alumno inscrito
            info_alumno = InscribirDao.consultar_alumno_inscripcion(alumno.id_usuario, curso.id_curso)
            assert info_alumno is not None
            assert info_alumno["nombre_completo"] == "Perez Alcantara Juan"
            assert info_alumno["email"] == "juan@test.com"
            assert info_alumno["genero"] == "M"
            assert info_alumno["grado_actual"] == "Tercero Preparatoria"

    def test_consultar_lista_inscripcion(self, app, inscribir_test):
        alumno1 = inscribir_test["alumno1"]
        alumno2 = inscribir_test["alumno2"]
        curso = inscribir_test["curso"]

        with app.app_context():
            # caso consultar lista de curso sin inscripciones
            lista = InscribirDao.consultar_lista_inscripcion(curso.id_curso)
            assert len(lista) == 0

            InscribirDao.crear_inscripcion(alumno1.id_usuario, curso.id_curso)
            InscribirDao.crear_inscripcion(alumno2.id_usuario, curso.id_curso)

            # caso consultar lista de inscripciones
            lista = InscribirDao.consultar_lista_inscripcion(curso.id_curso)
            assert len(lista) == 2
            nombres = [a["nombre_completo"] for a in lista]
            assert "Perez Alcantara Juan" in nombres
            assert "Perez Alcantara Juana" in nombres

            ids = [a["id_usuario"] for a in lista]
            assert alumno1.id_usuario in ids
            assert alumno2.id_usuario in ids

    def test_eliminar_inscripcion(self, app,inscribir_test):
        alumno = inscribir_test["alumno1"]
        curso = inscribir_test["curso"]

        with app.app_context():
            #caso eliminar alumno que no esta inscrito
            resultado = InscribirDao.eliminar_inscripcion(alumno.id_usuario, curso.id_curso)
            assert resultado is False

            InscribirDao.crear_inscripcion(alumno.id_usuario, curso.id_curso)

            #caso eliminar alumno inscrito
            eliminado = InscribirDao.eliminar_inscripcion(alumno.id_usuario, curso.id_curso)
            assert eliminado is True

            #revisar en bd que no siga inscrito
            inscripcion = Inscribir.query.filter_by(
                id_alumno=alumno.id_usuario,
                id_curso=curso.id_curso
            ).first()
            assert inscripcion is None

            #revisar en bd que solo se eliminó la inscripcion no el alumno
            alumno = Alumno.query.filter_by(id_usuario=alumno.id_usuario).first()
            assert alumno is not None

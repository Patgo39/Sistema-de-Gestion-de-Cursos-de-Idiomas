import pytest
from models import Usuario, Alumno, Curso, Docente, Idioma, Inscribir


class TestDocenteController:
    @pytest.fixture
    def docente_test(self, app, db):
        with app.app_context():
            # creamos el alumno
            usuario_alumno = Usuario(
                username="testuser1",
                nombre="Juan",
                apellido_paterno="Perez",
                apellido_materno="Alcantara",
                email="juan@test.com",
                password="password",
                genero="M",
                rol="Alumno"
            )
            db.session.add(usuario_alumno)
            db.session.commit()

            alumno = Alumno(
                id_usuario=usuario_alumno.id_usuario,
                grado_actual="Tercero Preparatoria"
            )
            db.session.add(alumno)
            db.session.commit()

            # creamos el docente
            usuario_docente = Usuario(
                username="testdocente",
                nombre="Ana",
                apellido_paterno="Lopez",
                apellido_materno="Canal",
                email="ana@test.com",
                password="password",
                genero="F",
                rol="Docente"
            )
            db.session.add(usuario_docente)
            db.session.commit()

            docente = Docente(
                id_usuario=usuario_docente.id_usuario
            )
            db.session.add(docente)
            db.session.commit()

            # creamos el idioma y curso
            idioma = Idioma(nombre_idioma="Francés")
            db.session.add(idioma)
            db.session.commit()

            curso = Curso(
                id_idioma=idioma.id_idioma,
                id_usuario=docente.id_usuario,
                nombre_curso="Francés II"
            )
            db.session.add(curso)
            db.session.commit()

            # inscribimos al alumno
            inscripcion = Inscribir(
                id_alumno=alumno.id_usuario,
                id_curso=curso.id_curso
            )
            db.session.add(inscripcion)
            db.session.commit()

            # Sincronizamos y liberamos objetos de la sesión
            db.session.refresh(alumno)
            db.session.refresh(docente)
            db.session.refresh(curso)

            db.session.expunge(alumno)
            db.session.expunge(docente)
            db.session.expunge(curso)

            return {"alumno": alumno, "docente": docente, "curso": curso}

    def test_curso_docente(self, client, app, db,docente_test):
        curso = docente_test["curso"]

        with client.session_transaction() as sess:
            sess['username'] = 'testdocente'

        response = client.get(f'/docente/tablero_docente/curso_docente/{curso.id_curso}')
        assert response.status_code == 200
        assert 'Francés II'.encode('utf-8') in response.data
        assert 'Juan'.encode('utf-8') in response.data

        with app.app_context():
            curso_bd = Curso.query.filter_by(id_curso=curso.id_curso).first()
            assert curso_bd is not None
            assert curso_bd.nombre_curso == 'Francés II'

    def test_curso_docente_vacio(self, client, docente_test):
        curso = docente_test["curso"]

        with client.session_transaction() as sess:
            sess['username'] = 'testdocente'

        response = client.get(f'/docente/tablero_docente/curso_docente/{curso.id_curso + 999}')
        assert response.status_code == 302

    def test_datos_alumno(self, client, app, db, docente_test):
        alumno = docente_test["alumno"]
        curso = docente_test["curso"]

        with client.session_transaction() as sess:
            sess['username'] = 'testdocente'

        response = client.get(f'/docente/tablero_docente/curso_docente/{curso.id_curso}/alumno/{alumno.id_usuario}')
        assert response.status_code == 200
        assert 'Perez'.encode('utf-8') in response.data
        assert 'juan@test.com'.encode('utf-8') in response.data
        assert 'Tercero Preparatoria'.encode('utf-8') in response.data

        with app.app_context():
            inscripcion = Inscribir.query.filter_by(
                id_alumno=alumno.id_usuario,
                id_curso=curso.id_curso
            ).first()
            assert inscripcion is not None

    def test_datos_alumno_no_existe(self, client, docente_test):
        curso = docente_test["curso"]

        with client.session_transaction() as sess:
            sess['username'] = 'testdocente'

        response = client.get(f'/docente/tablero_docente/curso_docente/{curso.id_curso}/alumno/9999')
        assert response.status_code == 302
        assert f'/docente/tablero_docente/curso_docente/{curso.id_curso}' in response.headers['Location']

    def test_eliminar_alumno(self, client, app, db, docente_test):
        alumno = docente_test["alumno"]
        curso = docente_test["curso"]

        with client.session_transaction() as sess:
            sess['username'] = 'testdocente'

        response = client.post(
            f'/docente/tablero_docente/curso_docente/{curso.id_curso}/alumno/{alumno.id_usuario}/eliminar')
        assert response.status_code == 302
        assert f'/docente/tablero_docente/curso_docente/{curso.id_curso}' in response.headers['Location']

        with app.app_context():
            inscripcion = Inscribir.query.filter_by(
                id_alumno=alumno.id_usuario,
                id_curso=curso.id_curso
            ).first()
            assert inscripcion is None

    def test_eliminar_alumno_no_existe(self, client, docente_test):
        curso = docente_test["curso"]

        with client.session_transaction() as sess:
            sess['username'] = 'testdocente'

        response = client.post(f'/docente/tablero_docente/curso_docente/{curso.id_curso}/alumno/9999/eliminar')
        assert response.status_code == 302
        assert f'/docente/tablero_docente/curso_docente/{curso.id_curso}' in response.headers['Location']
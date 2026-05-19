import pytest
from dao.inscribir_dao import InscribirDao
from models import Usuario, Alumno, Curso, Docente, Idioma, Dominar, Inscribir


class TestAlumnoController:
    @pytest.fixture
    def alumno_test(self, app, db):
        with app.app_context():
            # creamos el alumno1
            usuario_alumno = Usuario(
                username="testalumno",
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

            # creamos el alumno2
            usuario_alumno2 = Usuario(
                username="testalumno2",
                nombre="Pedro",
                apellido_paterno="Garcia",
                apellido_materno="Lopez",
                email="pedro@test.com",
                password="password",
                genero="M",
                rol="Alumno"
            )
            db.session.add(usuario_alumno2)
            db.session.commit()

            alumno2 = Alumno(
                id_usuario=usuario_alumno2.id_usuario,
                grado_actual="Primero Preparatoria"
            )
            db.session.add(alumno2)
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

            docente = Docente(id_usuario=usuario_docente.id_usuario)
            db.session.add(docente)
            db.session.commit()

            # creamos el idioma
            idioma = Idioma(nombre_idioma="Francés")
            db.session.add(idioma)
            db.session.commit()

            # creamos curso basico, intermedio y avanzado
            curso_basico = Curso(
                id_idioma=idioma.id_idioma,
                id_usuario=docente.id_usuario,
                nombre_curso="Francés I",
                nivel="Básico"
            )
            curso_intermedio = Curso(
                id_idioma=idioma.id_idioma,
                id_usuario=docente.id_usuario,
                nombre_curso="Francés II",
                nivel="Intermedio"
            )
            curso_avanzado = Curso(
                id_idioma=idioma.id_idioma,
                id_usuario=docente.id_usuario,
                nombre_curso="Francés III",
                nivel="Avanzado"
            )

            db.session.add(curso_basico)
            db.session.add(curso_intermedio)
            db.session.add(curso_avanzado)
            db.session.commit()


            # creamos dominio basico del alumno1
            dominio = Dominar(
                id_idioma=idioma.id_idioma,
                id_usuario=alumno.id_usuario,
                nivel_dominio="Básico"
            )
            db.session.add(dominio)
            db.session.commit()

            # sincronizamos y liberamos
            db.session.refresh(alumno)
            db.session.refresh(alumno2)
            db.session.refresh(curso_basico)
            db.session.refresh(curso_intermedio)
            db.session.refresh(curso_avanzado)

            db.session.expunge(alumno)
            db.session.expunge(alumno2)
            db.session.expunge(curso_basico)
            db.session.expunge(curso_intermedio)
            db.session.expunge(curso_avanzado)

            return {
                "alumno": alumno,
                "alumno2": alumno2,
                "curso_basico": curso_basico,
                "curso_intermedio": curso_intermedio,
                "curso_avanzado": curso_avanzado
            }

    def test_inscripcion_curso_basico(self, client, app, db, alumno_test):
        alumno = alumno_test["alumno"]
        curso = alumno_test["curso_basico"]

        #simula que hay una sesión activa para evitar redireccionamiento
        with client.session_transaction() as sess:
            sess['username'] = 'testalumno'
            sess['rol'] = 'Alumno'

        response = client.post(f'/alumno/tablero_alumno/cursos_disponibles/{curso.id_curso}/inscripcion')
        assert response.status_code == 302

        #verifica que se guardó en la base
        with app.app_context():
            inscripcion = Inscribir.query.filter_by(
                id_alumno=alumno.id_usuario,
                id_curso=curso.id_curso
            ).first()
            assert inscripcion is not None

    def test_inscripcion_curso_intermedio_con_dominio(self, client, app, db, alumno_test):
        alumno = alumno_test["alumno"]
        curso = alumno_test["curso_intermedio"]

        with client.session_transaction() as sess:
            sess['username'] = 'testalumno'
            sess['rol'] = 'Alumno'

        response = client.post(f'/alumno/tablero_alumno/cursos_disponibles/{curso.id_curso}/inscripcion')
        assert response.status_code == 302

        with app.app_context():
            inscripcion = Inscribir.query.filter_by(
                id_alumno=alumno.id_usuario,
                id_curso=curso.id_curso
            ).first()
            assert inscripcion is not None

    def test_inscripcion_sin_dominio_intermedio_y_avanzado(self, client, app, db, alumno_test):
        curso_intermedio = alumno_test["curso_intermedio"]
        curso_avanzado = alumno_test["curso_avanzado"]

        with client.session_transaction() as sess:
            sess['username'] = 'testalumno2'
            sess['rol'] = 'Alumno'

        #intermedio
        response = client.post(f'/alumno/tablero_alumno/cursos_disponibles/{curso_intermedio.id_curso}/inscripcion')
        assert response.status_code == 302

        with app.app_context():
            inscripcion = Inscribir.query.filter_by(
                id_alumno=alumno_test["alumno2"].id_usuario,
                id_curso=curso_intermedio.id_curso
            ).first()
            assert inscripcion is None

        #avanzado
        response = client.post(f'/alumno/tablero_alumno/cursos_disponibles/{curso_avanzado.id_curso}/inscripcion')
        assert response.status_code == 302

        with app.app_context():
            inscripcion = Inscribir.query.filter_by(
                id_alumno=alumno_test["alumno2"].id_usuario,
                id_curso=curso_avanzado.id_curso
            ).first()
            assert inscripcion is None

    def test_cursos_disponibles_sin_estar_inscrito(self, client, app, db, alumno_test):
        alumno = alumno_test["alumno"]
        curso_basico = alumno_test["curso_basico"]

        with client.session_transaction() as sess:
            sess['username'] = 'testalumno'
            sess['rol'] = 'Alumno'
            sess['usuario'] = alumno.id_usuario

        with app.app_context():
            InscribirDao.crear_inscripcion(alumno.id_usuario, curso_basico.id_curso)

        response = client.get('/alumno/tablero_alumno/cursos_disponibles')
        assert response.status_code == 200
        assert 'Francés I</span>'.encode('utf-8') not in response.data
        assert 'Francés II'.encode('utf-8') in response.data

    def test_inscripcion_curso_no_existe(self, client, alumno_test):
        with client.session_transaction() as sess:
            sess['username'] = 'testalumno'
            sess['rol'] = 'Alumno'

        response = client.post('/alumno/tablero_alumno/cursos_disponibles/9999/inscripcion')
        assert response.status_code == 302
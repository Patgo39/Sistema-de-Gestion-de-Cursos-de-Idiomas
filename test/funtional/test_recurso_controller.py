import pytest
import io
from flask import session
from datetime import date
from models.usuario import Usuario
from models.docente import Docente
from models.idioma import Idioma
from dao.curso_dao import CursoDao


def test_subir_recurso_sin_sesion(client):
    response = client.get('/recursos/subir_recurso/1')
    assert response.status_code == 302
    assert '/auth/login' in response.headers['Location']


def test_subir_recurso_exitoso(client, app, db):
    with app.app_context():
        user = Usuario(username="profe_recurso", email="p@recurso.com", password="123", rol="docente")
        db.session.add(user)
        db.session.commit()
        id_usuario_test = user.id_usuario
        docente = Docente(id_usuario=user.id_usuario, especialidad="Inglés", tiempo_experiencia=5)
        idioma = Idioma(nombre_idioma="Inglés")
        db.session.add_all([docente, idioma])
        db.session.commit()

        curso = CursoDao.crear_curso("Inglés Técnico", "Desc", "B2", docente.id_usuario, idioma.id_idioma)
        id_curso_test = curso.id_curso

    with client.session_transaction() as sess:
        sess['usuario'] = id_usuario_test
        sess['rol'] = 'docente'

    archivo_dummy = (io.BytesIO(b"contenido de prueba"), "examen_ingles.pdf")
    datos_formulario = {
        "nombre_recurso": "Examen de Inglés",
        "descripcion": "PDF con el examen",
        "archivo": archivo_dummy
    }


    response = client.post(
        f'/recursos/subir_recurso/{id_curso_test}',
        data=datos_formulario,
        content_type='multipart/form-data'
    )

    assert response.status_code == 302
    assert '/docente/tablero' in response.headers['Location']


def test_subir_recurso_sin_archivo(client, app, db):
    with app.app_context():
        user = Usuario(username="profe_error", email="e@error.com", password="123", rol="docente")
        db.session.add(user)
        db.session.commit()
        id_usuario_error = user.id_usuario
        docente = Docente(id_usuario=user.id_usuario, especialidad="Inglés")
        idioma = Idioma(nombre_idioma="Inglés")
        db.session.add_all([docente, idioma])
        db.session.commit()
        curso = CursoDao.crear_curso("Curso Error", "D", "A1", docente.id_usuario, idioma.id_idioma)
        id_c = curso.id_curso

    with client.session_transaction() as sess:
        sess['usuario'] = id_usuario_error

    datos_formulario = {
        "nombre_recurso": "Recurso vacío",
        "descripcion": "Sin archivo",
        "archivo": (io.BytesIO(b""), "")
    }

    response = client.post(
        f'/recursos/subir_recurso/{id_c}',
        data=datos_formulario,
        content_type='multipart/form-data',
        follow_redirects=True
    )

    assert b'Archivo no encontrado o inv' in response.data


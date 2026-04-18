import pytest
import io
from flask import session
from dao.usuario_dao import UsuarioDao

def  test_subir_recurso_sin_sesion(client):
    response=client.get('/auth/subir_recurso')
    assert response.status_code == 302
    assert 'login' in response.headers['Location']

def test_subir_recurso_exitoso(client, app, db):
    with client.session_transaction() as sess:
        sess['usuario']=1
        sess['rol']='docente'
    archivo_dummy= (io.BytesIO(b"contenido de prueba del pdf"), "examen_ingles.pdf")
    datos_formulario={
        "nombre_recurso": "Examen de Inglés",
        "descripcion": "PDF con el examen del primer parcial",
        "archivo": archivo_dummy
    }
    response = client.post(
        '/auth/subir_recurso',
        data=datos_formulario,
        content_type='multipart/form-data'
    )
    assert response.status_code == 302
    assert 'tablero_docente' in response.headers['Location']

def test_subir_recurso_sin_archivo(client):
    with client.session_transaction() as sess:
        sess['usuario']=1

    datos_formulario = {
        "nombre_recurso": "Recurso vacío",
        "descripcion": "Sin archivo",
        "archivo": (io.BytesIO(b""), "")
    }

    response = client.post(
        '/auth/subir_recurso',
        data=datos_formulario,
        content_type='multipart/form-data',
        follow_redirects=True
    )
    assert b'Archivo no encontrado o inv' in response.data



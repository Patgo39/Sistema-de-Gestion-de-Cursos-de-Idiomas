import pytest
from models.usuario import Usuario
from models.alumno import Alumno
from models.docente import Docente


def test_cargar_pagina_registro(client):
    response = client.get("/auth/registro")
    assert response.status_code == 200



def test_registro_docente_exitoso(client, app, db):
    datos_formulario={
        "username": "nuevo_docente",
        "nombre": "Ana",
        "apellido_paterno": "Gómez",
        "apellido_materno": "Díaz",
        "email": "ana@test.com",
        "fecha_nacimiento": "1990-05-15",
        "password": "password_seguro",
        "genero": "Femenino",
        "pais": "Colombia",
        "rol": "docente",
        "tiempo_experiencia": "4",
        "especialidad": "Inglés"
    }
    response = client.post("/auth/registro", data=datos_formulario)
    assert response.status_code == 302

    assert 'login' in response.headers['Location']
    with app.app_context():
        usuario_creado = Usuario.query.filter_by(username="nuevo_docente").first()
        assert usuario_creado is not None
        assert usuario_creado.nombre == "Ana"
        profe_creado = Docente.query.filter_by(id_usuario=usuario_creado.id_usuario).first()
        assert profe_creado is not None
        assert profe_creado.especialidad == "Inglés"



def test_registro_alumno_exitoso(client, app, db):
    datos_formulario={
        "username": "nuevo_alumno",
        "nombre": "Carlos",
        "apellido_paterno": "Ruiz",
        "apellido_materno": "Paz",
        "email": "carlos@test.com",
        "fecha_nacimiento": "2005-08-20",
        "password": "password_seguro",
        "genero": "Masculino",
        "pais": "Perú",
        "rol": "alumno",
        "grado_actual": "2do Semestre"
    }
    response = client.post("/auth/registro", data=datos_formulario)
    assert response.status_code == 302
    assert 'login' in response.headers['Location']
    with app.app_context():
        usuario_creado = Usuario.query.filter_by(username="nuevo_alumno").first()
        assert usuario_creado is not None
        assert usuario_creado.email == "carlos@test.com"
        alumno_creado = Alumno.query.filter_by(id_usuario=usuario_creado.id_usuario).first()
        assert alumno_creado is not None
        assert alumno_creado.grado_actual == "2do Semestre"



import pytest
from datetime import date
from dao.usuario_dao import UsuarioDao


def test_cargar_pagina_login(client):
    response = client.get("/auth/login")
    assert response.status_code == 200

def test_alumno_exitoso(client, app, db):
    with app.app_context():
        UsuarioDao.registrar_alumno(
            username="alumno_login",
            nombre="Juan",
            apellido_paterno="Perez",
            apellido_materno="Sosa",
            email="juan@test.com",
            fecha_nacimiento=date(2005, 1, 1),
            password="password123",
            genero="Masculino",
            pais="México",
            grado_actual="1er Semestre"
        )

    response = client.post('/auth/login', data={
        "username": "alumno_login",
        "password": "password123"
    })

    assert response.status_code == 302
    assert '/auth/tablero_alumno' in response.headers['Location']

    with client.session_transaction() as session:
        assert session['username'] == 'alumno_login'
        assert session['rol'] == 'alumno'
        assert session.get('usuario') is not None


def test_login_fallido(client):
    response = client.post('/auth/login', data={
        "username": "usuario_fantasma",
        "password": "clave_incorrecta"
    })

    assert response.status_code == 302
    assert '/auth/login' in response.headers['Location']


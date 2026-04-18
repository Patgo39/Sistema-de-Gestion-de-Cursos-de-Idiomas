import os
import pytest
from sqlalchemy import create_engine
os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
from app import app as flask_app
from db import db as _db
from models.usuario import Usuario
from models.alumno import Alumno
from models.docente import Docente


@pytest.fixture
def app():
    flask_app.config.update({
        "TESTING": True,
        "SECRET_KEY": "llave_secreta_de_prueba",
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "WTF_CSRF_ENABLED": False
    })

    with flask_app.app_context():
        engine = create_engine('sqlite:///:memory:')
        _db.session.remove()
        _db.engines[None] = engine
        _db.create_all()
        yield flask_app
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def db(app):
    return _db

@pytest.fixture
def client(app):
    return app.test_client()


import pytest
from app import app, db
from models.usuario import Usuario
from models.docente import Docente
from dao.docente_dao import DocenteDao

class TestDocenteDao:

    # Crea y elimina la BD provisional para los tests.
    @pytest.fixture(autouse=True)
    def config_test_db(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
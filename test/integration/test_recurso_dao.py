import pytest
from dao.recurso_dao import RecursoDao
from dao.usuario_dao import UsuarioDao
from models.recurso import Recurso
from models.docente import Docente
from datetime import date

def test_guardar_recurso_exitoso(app, db):
    with app.app_context():
        UsuarioDao.registrar_docente(
            username="profe_test",
            nombre="Juan",
            apellido_paterno="Pérez",
            apellido_materno="Sosa",
            email="juan@perez.com",
            fecha_nacimiento=date(1985, 5, 10),
            password="123",
            genero="Masculino",
            pais="México",
            tiempo_experiencia=5,
            especialidad="Francés"
        )

        profe = Docente.query.first()
        assert profe is not None

        recurso = RecursoDao.guardar_recurso(
            nombre="Guía de Verbos",
            filename="verbos_frances.pdf",
            descripcion="Lista de verbos irregulares",
            id_profe=profe.id_usuario
        )

        assert recurso.id_recurso is not None
        assert recurso.nombre_recurso == "Guía de Verbos"


        en_db = Recurso.query.filter_by(nombre_recurso="Guía de Verbos").first()
        assert en_db is not None
        assert en_db.archivo_url == "verbos_frances.pdf"


def test_obtener_todos_los_recursos(app, db):
    with app.app_context():
        UsuarioDao.registrar_docente(
            username="profe_2",
            nombre="Maria",
            apellido_paterno="G",
            apellido_materno="L",
            email="maria@test.com",
            fecha_nacimiento=date(1990, 1, 1),
            password="123",
            genero="Femenino",
            pais="España",
            tiempo_experiencia=2,
            especialidad="Italiano"
        )
        profe = Docente.query.first()


        RecursoDao.guardar_recurso("Recurso 1", "file1.png", "Desc 1", profe.id_usuario)
        RecursoDao.guardar_recurso("Recurso 2", "file2.png", "Desc 2", profe.id_usuario)

        lista = RecursoDao.obtener_todos()
        assert len(lista) == 2
        assert lista[0].nombre_recurso == "Recurso 1"
        assert lista[1].nombre_recurso == "Recurso 2"
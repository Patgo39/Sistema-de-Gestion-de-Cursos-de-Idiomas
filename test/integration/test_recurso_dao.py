import pytest
from dao.recurso_dao import RecursoDao
from dao.usuario_dao import UsuarioDao
from dao.curso_dao import CursoDao
from models.recurso import Recurso
from models.docente import Docente
from models.usuario import Usuario
from models.idioma import Idioma
from models.curso import Curso
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


        usuario_profe = Usuario.query.filter_by(username="profe_test").first()
        profe = Docente.query.filter_by(id_usuario=usuario_profe.id_usuario).first()
        assert profe is not None


        idioma_test = Idioma(nombre_idioma="Francés")
        db.session.add(idioma_test)
        db.session.commit()


        curso = CursoDao.crear_curso(
            nombre_curso="Francés Nivel 1",
            descripcion="Básico",
            nivel="A1",
            id_usuario=profe.id_usuario,
            id_idioma=idioma_test.id_idioma
        )

        recurso = RecursoDao.guardar_recurso(
            titulo="Guía de Verbos",
            filename="verbos_frances.pdf",
            descripcion="Lista de verbos irregulares",
            id_curso=curso.id_curso
        )

        assert recurso.id_recurso is not None
        assert recurso.titulo_recurso == "Guía de Verbos"

        en_db = Recurso.query.filter_by(titulo_recurso="Guía de Verbos").first()
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

        usuario_profe = Usuario.query.filter_by(username="profe_2").first()
        profe = Docente.query.filter_by(id_usuario=usuario_profe.id_usuario).first()


        idioma_test = Idioma(nombre_idioma="Italiano")
        db.session.add(idioma_test)
        db.session.commit()


        curso = CursoDao.crear_curso(
            nombre_curso="Italiano Nivel 1",
            descripcion="Básico",
            nivel="A1",
            id_usuario=profe.id_usuario,
            id_idioma=idioma_test.id_idioma
        )

        RecursoDao.guardar_recurso("Recurso 1", "file1.png", "Desc 1", curso.id_curso)
        RecursoDao.guardar_recurso("Recurso 2", "file2.png", "Desc 2", curso.id_curso)

        lista = RecursoDao.obtener_todos()
        assert len(lista) == 2
        assert lista[0].titulo_recurso == "Recurso 1"
        assert lista[1].titulo_recurso == "Recurso 2"
import pytest
from datetime import date
from dao.curso_dao import CursoDao
from dao.usuario_dao import UsuarioDao
from models.curso import Curso
from models.docente import Docente
from models.idioma import Idioma
from models.usuario import Usuario  # <-- NUEVO IMPORT


def test_crear_curso_exitoso(app, db):
    with app.app_context():
        UsuarioDao.registrar_docente(
            username="profe_curso",
            nombre="Carlos",
            apellido_paterno="Ruiz",
            apellido_materno="Mora",
            email="carlos@cursos.com",
            fecha_nacimiento=date(1985, 8, 20),
            password="123",
            genero="Masculino",
            pais="Perú",
            tiempo_experiencia=4,
            especialidad="Alemán"
        )
        usuario_profe = Usuario.query.filter_by(username="profe_curso").first()
        profe = Docente.query.filter_by(id_usuario=usuario_profe.id_usuario).first()

        idioma_test = Idioma(nombre_idioma="Alemán")
        db.session.add(idioma_test)
        db.session.commit()

        curso_creado = CursoDao.crear_curso(
            nombre_curso="Alemán Básico",
            descripcion="Introducción al idioma alemán",
            nivel="A1",
            id_usuario=profe.id_usuario,
            id_idioma=idioma_test.id_idioma
        )

        assert curso_creado is not None
        assert curso_creado.id_curso is not None
        assert curso_creado.nombre_curso == "Alemán Básico"

        curso_en_db = Curso.query.filter_by(nombre_curso="Alemán Básico").first()
        assert curso_en_db is not None
        assert curso_en_db.nivel == "A1"
        assert curso_en_db.id_usuario == profe.id_usuario


def test_obtener_cursos_por_docente(app, db):
    with app.app_context():
        UsuarioDao.registrar_docente(
            username="profe_multi",
            nombre="Laura",
            apellido_paterno="García",
            apellido_materno="Vega",
            email="laura@multi.com",
            fecha_nacimiento=date(1992, 2, 10),
            password="123",
            genero="Femenino",
            pais="España",
            tiempo_experiencia=2,
            especialidad="Italiano"
        )
        usuario_profe = Usuario.query.filter_by(username="profe_multi").first()
        profe = Docente.query.filter_by(id_usuario=usuario_profe.id_usuario).first()

        idioma_ita = Idioma(nombre_idioma="Italiano")
        db.session.add(idioma_ita)
        db.session.commit()

        CursoDao.crear_curso(
            nombre_curso="Italiano 1",
            descripcion="Básico",
            nivel="A1",
            id_usuario=profe.id_usuario,
            id_idioma=idioma_ita.id_idioma
        )
        CursoDao.crear_curso(
            nombre_curso="Italiano 2",
            descripcion="Intermedio",
            nivel="A2",
            id_usuario=profe.id_usuario,
            id_idioma=idioma_ita.id_idioma
        )

        cursos_laura = CursoDao.obtener_cursos_por_docente(profe.id_usuario)

        assert len(cursos_laura) == 2
        assert cursos_laura[0].nombre_curso == "Italiano 1"
        assert cursos_laura[1].nombre_curso == "Italiano 2"
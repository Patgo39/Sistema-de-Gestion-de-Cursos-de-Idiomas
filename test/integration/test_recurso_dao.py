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


def test_buscar_por_id(app, db):
    with app.app_context():
        UsuarioDao.registrar_docente(
            username="profe_buscar_rec", nombre="Ana", apellido_paterno="López", apellido_materno="Mora",
            email="ana@buscar_rec.com", fecha_nacimiento=date(1988, 3, 14), password="123",
            genero="Femenino", pais="Colombia", tiempo_experiencia=4, especialidad="Inglés"
        )
        usuario_profe = Usuario.query.filter_by(username="profe_buscar_rec").first()
        profe = Docente.query.filter_by(id_usuario=usuario_profe.id_usuario).first()

        idioma_test = Idioma(nombre_idioma="Inglés Británico")
        db.session.add(idioma_test)
        db.session.commit()

        curso = CursoDao.crear_curso(
            nombre_curso="Inglés B1", descripcion="Intermedio", nivel="B1",
            id_usuario=profe.id_usuario, id_idioma=idioma_test.id_idioma
        )

        recurso_creado = RecursoDao.guardar_recurso(
            titulo="Audio Lección 1", filename="audio1.mp3",
            descripcion="Práctica de listening", id_curso=curso.id_curso
        )

        recurso_encontrado = RecursoDao.buscar_por_id(recurso_creado.id_recurso)

        assert recurso_encontrado is not None
        assert recurso_encontrado.id_recurso == recurso_creado.id_recurso
        assert recurso_encontrado.titulo_recurso == "Audio Lección 1"


def test_obtener_por_curso(app, db):
    with app.app_context():
        UsuarioDao.registrar_docente(
            username="profe_curso_rec", nombre="Carlos", apellido_paterno="Ruiz", apellido_materno="Gil",
            email="carlos@curso_rec.com", fecha_nacimiento=date(1980, 8, 20), password="123",
            genero="Masculino", pais="Perú", tiempo_experiencia=8, especialidad="Alemán"
        )
        usuario_profe = Usuario.query.filter_by(username="profe_curso_rec").first()
        profe = Docente.query.filter_by(id_usuario=usuario_profe.id_usuario).first()

        idioma_test = Idioma(nombre_idioma="Alemán")
        db.session.add(idioma_test)
        db.session.commit()

        curso_aleman = CursoDao.crear_curso(
            nombre_curso="Alemán A1", descripcion="Básico", nivel="A1",
            id_usuario=profe.id_usuario, id_idioma=idioma_test.id_idioma
        )

        RecursoDao.guardar_recurso("Vocabulario", "vocab.pdf", "Palabras básicas", curso_aleman.id_curso)
        RecursoDao.guardar_recurso("Gramática", "gramatica.pdf", "Reglas iniciales", curso_aleman.id_curso)
        recursos_del_curso = RecursoDao.obtener_por_curso(curso_aleman.id_curso)

        assert len(recursos_del_curso) == 2
        titulos = [r.titulo_recurso for r in recursos_del_curso]
        assert "Vocabulario" in titulos
        assert "Gramática" in titulos


def test_actualizar_recurso(app, db):
    with app.app_context():
        UsuarioDao.registrar_docente(
            username="profe_act_rec", nombre="Luis", apellido_paterno="Paz", apellido_materno="Sol",
            email="luis@act_rec.com", fecha_nacimiento=date(1992, 11, 5), password="123",
            genero="Masculino", pais="Chile", tiempo_experiencia=3, especialidad="Portugués"
        )
        usuario_profe = Usuario.query.filter_by(username="profe_act_rec").first()
        profe = Docente.query.filter_by(id_usuario=usuario_profe.id_usuario).first()

        idioma_test = Idioma(nombre_idioma="Portugués")
        db.session.add(idioma_test)
        db.session.commit()

        curso = CursoDao.crear_curso(
            nombre_curso="Portugués Básico", descripcion="Iniciación", nivel="A1",
            id_usuario=profe.id_usuario, id_idioma=idioma_test.id_idioma
        )

        recurso_original = RecursoDao.guardar_recurso(
            titulo="Guía Vieja", filename="guia_v1.pdf",
            descripcion="Versión 1", id_curso=curso.id_curso
        )

        datos_nuevos = {
            "titulo_recurso": "Guía Actualizada",
            "descripcion": "Versión 2 definitiva"
        }
        recurso_actualizado = RecursoDao.actualizar_recurso(recurso_original.id_recurso, datos_nuevos)

        assert recurso_actualizado is not None
        assert recurso_actualizado.titulo_recurso == "Guía Actualizada"
        assert recurso_actualizado.descripcion == "Versión 2 definitiva"

        recurso_db = Recurso.query.get(recurso_original.id_recurso)
        assert recurso_db.titulo_recurso == "Guía Actualizada"


def test_eliminar_recurso(app, db):
    with app.app_context():
        UsuarioDao.registrar_docente(
            username="profe_eli_rec", nombre="Sofía", apellido_paterno="Luz", apellido_materno="Mar",
            email="sofia@eli_rec.com", fecha_nacimiento=date(1995, 2, 28), password="123",
            genero="Femenino", pais="Argentina", tiempo_experiencia=2, especialidad="Chino"
        )
        usuario_profe = Usuario.query.filter_by(username="profe_eli_rec").first()
        profe = Docente.query.filter_by(id_usuario=usuario_profe.id_usuario).first()

        idioma_test = Idioma(nombre_idioma="Chino")
        db.session.add(idioma_test)
        db.session.commit()

        curso = CursoDao.crear_curso(
            nombre_curso="Chino Mandarín", descripcion="Básico", nivel="A1",
            id_usuario=profe.id_usuario, id_idioma=idioma_test.id_idioma
        )

        recurso_a_eliminar = RecursoDao.guardar_recurso(
            titulo="Documento Temporal", filename="temp.pdf",
            descripcion="Para borrar", id_curso=curso.id_curso
        )
        id_recurso_borrar = recurso_a_eliminar.id_recurso

        resultado = RecursoDao.eliminar_recurso(id_recurso_borrar)

        assert resultado is True
        recurso_borrado = RecursoDao.buscar_por_id(id_recurso_borrar)
        assert recurso_borrado is None
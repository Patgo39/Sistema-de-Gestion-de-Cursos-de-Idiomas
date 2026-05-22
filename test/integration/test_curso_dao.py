import pytest
from datetime import date
from dao.curso_dao import CursoDao
from dao.usuario_dao import UsuarioDao
from models.curso import Curso
from models.docente import Docente
from models.idioma import Idioma
from models.usuario import Usuario
from models.inscribir import Inscribir

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


def test_obtener_cursos_por_alumno(app, db):
    with app.app_context():
        UsuarioDao.registrar_docente(
            username="profe_frances",
            nombre="Julien",
            apellido_paterno="Dupont",
            apellido_materno="Lefevre",
            email="julien@cursos.com",
            fecha_nacimiento=date(1980, 5, 15),
            password="123",
            genero="Masculino",
            pais="Francia",
            tiempo_experiencia=8,
            especialidad="Francés"
        )
        usuario_profe = Usuario.query.filter_by(username="profe_frances").first()

        idioma_fra = Idioma(nombre_idioma="Francés")
        db.session.add(idioma_fra)
        db.session.commit()

        curso1 = CursoDao.crear_curso(
            nombre_curso="Francés A1", descripcion="Básico", nivel="A1",
            id_usuario=usuario_profe.id_usuario, id_idioma=idioma_fra.id_idioma
        )
        curso2 = CursoDao.crear_curso(
            nombre_curso="Francés A2", descripcion="Intermedio", nivel="A2",
            id_usuario=usuario_profe.id_usuario, id_idioma=idioma_fra.id_idioma
        )
        curso_no_inscrito = CursoDao.crear_curso(
            nombre_curso="Francés B1", descripcion="Avanzado", nivel="B1",
            id_usuario=usuario_profe.id_usuario, id_idioma=idioma_fra.id_idioma
        )
        UsuarioDao.registrar_alumno(
            username="alumno_test",
            nombre="Ana",
            apellido_paterno="López",
            apellido_materno="Gómez",
            email="ana@test.com",
            fecha_nacimiento=date(2002, 10, 5),
            password="123",
            genero="Femenino",
            pais="México",
            grado_actual="Universidad"
        )
        usuario_alumno = Usuario.query.filter_by(username="alumno_test").first()

        inscripcion1 = Inscribir(id_usuario=usuario_alumno.id_usuario, id_curso=curso1.id_curso)
        inscripcion2 = Inscribir(id_usuario=usuario_alumno.id_usuario, id_curso=curso2.id_curso)
        db.session.add_all([inscripcion1, inscripcion2])
        db.session.commit()
        cursos_alumno = CursoDao.obtener_cursos_por_alumno(usuario_alumno.id_usuario)
        assert len(cursos_alumno) == 2, "El alumno debería estar inscrito exactamente en 2 cursos"
        nombres_cursos_inscritos = [curso.nombre_curso for curso in cursos_alumno]

        assert "Francés A1" in nombres_cursos_inscritos
        assert "Francés A2" in nombres_cursos_inscritos
        assert "Francés B1" not in nombres_cursos_inscritos, "El alumno no debería ver cursos en los que no se inscribió"


def test_buscar_por_id(app, db):
    with app.app_context():
        UsuarioDao.registrar_docente(
            username="profe_buscar", nombre="Luis", apellido_paterno="Soto", apellido_materno="Rey",
            email="luis@buscar.com", fecha_nacimiento=date(1990, 1, 1), password="123",
            genero="Masculino", pais="Chile", tiempo_experiencia=5, especialidad="Inglés"
        )
        profe = Usuario.query.filter_by(username="profe_buscar").first()

        idioma_ing = Idioma(nombre_idioma="Inglés")
        db.session.add(idioma_ing)
        db.session.commit()

        curso_nuevo = CursoDao.crear_curso(
            nombre_curso="Inglés Básico", descripcion="Para principiantes", nivel="A1",
            id_usuario=profe.id_usuario, id_idioma=idioma_ing.id_idioma
        )

        curso_encontrado = CursoDao.buscar_por_id(curso_nuevo.id_curso)

        assert curso_encontrado is not None
        assert curso_encontrado.id_curso == curso_nuevo.id_curso
        assert curso_encontrado.nombre_curso == "Inglés Básico"


def test_actualizar_curso(app, db):
    with app.app_context():
        UsuarioDao.registrar_docente(
            username="profe_actualizar", nombre="María", apellido_paterno="Paz", apellido_materno="Gil",
            email="maria@actualizar.com", fecha_nacimiento=date(1988, 3, 3), password="123",
            genero="Femenino", pais="Colombia", tiempo_experiencia=3, especialidad="Portugués"
        )
        profe = Usuario.query.filter_by(username="profe_actualizar").first()

        idioma_por = Idioma(nombre_idioma="Portugués")
        db.session.add(idioma_por)
        db.session.commit()

        curso_original = CursoDao.crear_curso(
            nombre_curso="Portugués 1", descripcion="Básico", nivel="A1",
            id_usuario=profe.id_usuario, id_idioma=idioma_por.id_idioma
        )

        datos_nuevos = {
            "nombre_curso": "Portugués Avanzado",
            "nivel": "C1"
        }
        curso_actualizado = CursoDao.actualizar_curso(curso_original.id_curso, datos_nuevos)

        assert curso_actualizado is not None
        assert curso_actualizado.nombre_curso == "Portugués Avanzado"
        assert curso_actualizado.nivel == "C1"

        curso_db = Curso.query.filter_by(id_curso=curso_original.id_curso).first()
        assert curso_db.nombre_curso == "Portugués Avanzado"


def test_eliminar_curso(app, db):
    with app.app_context():
        UsuarioDao.registrar_docente(
            username="profe_eliminar", nombre="Pedro", apellido_paterno="Luz", apellido_materno="Sol",
            email="pedro@eliminar.com", fecha_nacimiento=date(1982, 4, 4), password="123",
            genero="Masculino", pais="Argentina", tiempo_experiencia=10, especialidad="Japonés"
        )
        profe = Usuario.query.filter_by(username="profe_eliminar").first()

        idioma_jap = Idioma(nombre_idioma="Japonés")
        db.session.add(idioma_jap)
        db.session.commit()

        curso_a_eliminar = CursoDao.crear_curso(
            nombre_curso="Japonés N5", descripcion="Básico", nivel="N5",
            id_usuario=profe.id_usuario, id_idioma=idioma_jap.id_idioma
        )
        id_curso_borrar = curso_a_eliminar.id_curso

        resultado = CursoDao.eliminar_curso(id_curso_borrar)
        assert resultado is True
        curso_borrado = CursoDao.buscar_por_id(id_curso_borrar)
        assert curso_borrado is None


def test_obtener_todos(app, db):
    with app.app_context():
        UsuarioDao.registrar_docente(
            username="profe_todos", nombre="Ana", apellido_paterno="Rios", apellido_materno="Mar",
            email="ana@todos.com", fecha_nacimiento=date(1995, 5, 5), password="123",
            genero="Femenino", pais="México", tiempo_experiencia=2, especialidad="Chino"
        )
        profe = Usuario.query.filter_by(username="profe_todos").first()

        idioma_chi = Idioma(nombre_idioma="Chino")
        db.session.add(idioma_chi)
        db.session.commit()

        CursoDao.crear_curso(
            nombre_curso="Chino HSK1", descripcion="Básico", nivel="HSK1",
            id_usuario=profe.id_usuario, id_idioma=idioma_chi.id_idioma
        )
        CursoDao.crear_curso(
            nombre_curso="Chino HSK2", descripcion="Intermedio", nivel="HSK2",
            id_usuario=profe.id_usuario, id_idioma=idioma_chi.id_idioma
        )

        cursos = CursoDao.obtener_todos()
        assert len(cursos) >= 2
        assert isinstance(cursos[0], Curso)


def test_obtener_todos_los_cursos_mapped(app, db):
    with app.app_context():
        UsuarioDao.registrar_docente(
            username="profe_mapped", nombre="Sofía", apellido_paterno="Sol", apellido_materno="Luna",
            email="sofia@mapped.com", fecha_nacimiento=date(1991, 6, 6), password="123",
            genero="Femenino", pais="España", tiempo_experiencia=4, especialidad="Ruso"
        )
        profe = Usuario.query.filter_by(username="profe_mapped").first()

        idioma_rus = Idioma(nombre_idioma="Ruso")
        db.session.add(idioma_rus)
        db.session.commit()

        CursoDao.crear_curso(
            nombre_curso="Ruso Básico", descripcion="Alfabeto cirílico", nivel="A1",
            id_usuario=profe.id_usuario, id_idioma=idioma_rus.id_idioma
        )

        cursos_mapped = CursoDao.obtener_todos_los_cursos()

        assert isinstance(cursos_mapped, list)
        assert len(cursos_mapped) >= 1

        curso_dict = cursos_mapped[-1]
        assert 'id_curso' in curso_dict
        assert 'nombre_curso' in curso_dict
        assert 'inscritos' in curso_dict
        assert 'recursos' in curso_dict
        assert isinstance(curso_dict['inscritos'], list)
        assert isinstance(curso_dict['recursos'], list)
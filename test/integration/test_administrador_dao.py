import pytest
from datetime import date
from dao.administrador_dao import AdministradorDao
from models.administrador import Administrador
from models.usuario import Usuario


class TestAdministradorDao:

    @pytest.fixture
    def admin_test(self, app, db):
        """Fixture para crear un administrador base para las pruebas."""
        with app.app_context():
            admin = AdministradorDao.crear_administrador(
                username="admin_test",
                nombre="Admin",
                apellido_paterno="Sistemas",
                apellido_materno="Central",
                email="admin@test.com",
                fecha_nacimiento=date(1990, 1, 1),
                password="hashed_password",
                genero="Otro",
                pais="México",
                nivel_privilegio=1
            )
            # SOLUCIÓN AL DetachedInstanceError:
            # Forzamos la carga del atributo id_usuario mientras el contexto está abierto.
            # Al acceder a él, se guarda en el diccionario local del objeto.
            _ = admin.id_usuario

            # Expulsamos el objeto de la sesión para que no intente refrescarse
            # cuando lo usemos en otros tests.
            db.session.expunge(admin)
            return admin

    def test_crear_administrador(self, app, db):
        with app.app_context():
            nuevo_admin = AdministradorDao.crear_administrador(
                username="root",
                nombre="Super",
                apellido_paterno="User",
                apellido_materno="Root",
                email="root@test.com",
                fecha_nacimiento=date(1985, 5, 20),
                password="root_password",
                genero="Masculino",
                pais="España",
                nivel_privilegio=2
            )

            assert nuevo_admin is not None
            assert nuevo_admin.nivel_privilegio == 2

            # Uso de db.session.get (Recomendado en SQLAlchemy 2.0+)
            usuario = db.session.get(Usuario, nuevo_admin.id_usuario)
            assert usuario.username == "root"
            assert usuario.rol == "Administrador"

    def test_obtener_por_id(self, app, admin_test):
        with app.app_context():
            # admin_test ya trae su id_usuario cargado en memoria
            admin = AdministradorDao.obtener_por_id(admin_test.id_usuario)
            assert admin is not None
            assert admin.nivel_privilegio == 1

            admin_inexistente = AdministradorDao.obtener_por_id(9999)
            assert admin_inexistente is None

    def test_obtener_todos(self, app, admin_test):
        with app.app_context():
            # Crear un segundo admin para verificar la lista
            AdministradorDao.crear_administrador(
                "admin2", "Nom", "Ap", "Am", "a2@t.com",
                date(1990, 1, 1), "pass", "F", "México", 1
            )

            lista = AdministradorDao.obtener_todos()
            assert len(lista) >= 2

    def test_actualizar_administrador(self, app, db, admin_test):
        with app.app_context():
            id_admin = admin_test.id_usuario
            nuevos_datos = {
                "nombre": "Nombre Editado",
                "nivel_privilegio": 3,
                "pais": "Colombia"
            }

            exito = AdministradorDao.actualizar_administrador(id_admin, nuevos_datos)
            assert exito is True

            admin_upd = AdministradorDao.obtener_por_id(id_admin)
            usuario_upd = db.session.get(Usuario, id_admin)

            assert admin_upd.nivel_privilegio == 3
            assert usuario_upd.nombre == "Nombre Editado"
            assert usuario_upd.pais == "Colombia"

    def test_eliminar_administrador(self, app, db, admin_test):
        with app.app_context():
            id_admin = admin_test.id_usuario

            exito = AdministradorDao.eliminar_administrador(id_admin)
            assert exito is True

            # Verificamos usando db.session.get para evitar warnings
            assert db.session.get(Administrador, id_admin) is None
            assert db.session.get(Usuario, id_admin) is None


if __name__ == "__main__":
    pytest.main([__file__])
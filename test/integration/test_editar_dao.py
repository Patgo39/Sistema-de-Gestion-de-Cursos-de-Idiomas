import pytest
from datetime import date
from dao.editar_dao import EditarDao
from dao.administrador_dao import AdministradorDao
from models.editar import Editar
from models.usuario import Usuario


class TestEditarDao:

    @pytest.fixture
    def setup_datos(self, app, db):
        # Para crear un administrador y un usuario base para las pruebas.
        with app.app_context():
            # Creamos un Administrador
            admin = AdministradorDao.crear_administrador(
                username="admin_editor",
                nombre="Admin",
                apellido_paterno="Editor",
                apellido_materno="Test",
                email="admin_editor@test.com",
                fecha_nacimiento=date(1980, 5, 15),
                password="password123",
                genero="M",
                pais="México",
                nivel_privilegio=1
            )

            # Crear un Usuario común
            usuario_editado = AdministradorDao.crear_administrador(
                username="usuario_editado",
                nombre="Juan",
                apellido_paterno="Pérez",
                apellido_materno="García",
                email="juan@test.com",
                fecha_nacimiento=date(1995, 10, 20),
                password="password456",
                genero="M",
                pais="España",
                nivel_privilegio=1
            )

            id_admin = admin.id_usuario
            id_user = usuario_editado.id_usuario

            db.session.expunge(admin)
            db.session.expunge(usuario_editado)

            return {"id_admin": id_admin, "id_user": id_user}

    def test_crear_registro_edicion(self, app, setup_datos):
        with app.app_context():
            id_admin = setup_datos["id_admin"]
            id_user = setup_datos["id_user"]

            registro = EditarDao.crear_registro_edicion(id_admin, id_user)

            assert registro is not None
            assert registro.id_administrador == id_admin
            assert registro.id_usuario == id_user
            assert registro.fecha_edicion == date.today()

    def test_buscar_por_llave_compuesta(self, app, setup_datos):
        with app.app_context():
            id_admin = setup_datos["id_admin"]
            id_user = setup_datos["id_user"]

            EditarDao.crear_registro_edicion(id_admin, id_user)

            registro = EditarDao.buscar_por_llave_compuesta(id_admin, id_user)

            assert registro is not None
            assert registro.id_administrador == id_admin
            assert registro.id_usuario == id_user

    def test_buscar_ediciones_por_administrador(self, app, setup_datos):
        with app.app_context():
            id_admin = setup_datos["id_admin"]
            id_user = setup_datos["id_user"]

            EditarDao.crear_registro_edicion(id_admin, id_user)

            ediciones = EditarDao.buscar_ediciones_por_administrador(id_admin)
            assert len(ediciones) >= 1
            assert ediciones[0].id_administrador == id_admin

    def test_actualizar_fecha_edicion(self, app, setup_datos):
        with app.app_context():
            id_admin = setup_datos["id_admin"]
            id_user = setup_datos["id_user"]

            EditarDao.crear_registro_edicion(id_admin, id_user)

            exito = EditarDao.actualizar_fecha_edicion(id_admin, id_user)
            assert exito is True

    def test_eliminar_registro(self, app, db, setup_datos):
        with app.app_context():
            id_admin = setup_datos["id_admin"]
            id_user = setup_datos["id_user"]

            EditarDao.crear_registro_edicion(id_admin, id_user)

            exito = EditarDao.eliminar_registro(id_admin, id_user)
            assert exito is True

            registro_eliminado = db.session.get(Editar, (id_admin, id_user))
            assert registro_eliminado is None


if __name__ == "__main__":
    pytest.main([__file__])
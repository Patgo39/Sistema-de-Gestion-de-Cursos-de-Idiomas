from db import db
from models import Usuario, Alumno
from models.inscribir import Inscribir

class InscribirDao:
    #Crea una nueva inscripcion: necesita el id del usuario y del curso
    @staticmethod
    def crear_inscripcion(id_usuario, id_curso):
        try:
            nueva_inscripcion = Inscribir(id_alumno=id_usuario, id_curso=id_curso)

            db.session.add(nueva_inscripcion)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error al inscribir: {e}")

    #Consulta los datos de inscripcion de un alumno(devuelve dic: nombre completo, email, género, grado actual): necesita el id del alumno y del curso
    @staticmethod
    def consultar_alumno_inscripcion(id_usuario, id_curso):
        try:
            datos_alumno = (db.session.query(Usuario.apellido_paterno,
                                                Usuario.apellido_materno,
                                                Usuario.nombre,
                                                Usuario.email,
                                                Usuario.genero,
                                                Alumno.grado_actual)
                            .join(Alumno, Alumno.id_usuario == Usuario.id_usuario)
                            .join(Inscribir, Inscribir.id_alumno == Alumno.id_usuario)
                            .filter(Inscribir.id_curso == id_curso, Inscribir.id_alumno == id_usuario)
                            .first())
            if datos_alumno:
                return {
                    "nombre_completo": f"{datos_alumno[0]} {datos_alumno[1]} {datos_alumno[2]}",
                    "email": datos_alumno[3],
                    "genero": datos_alumno[4],
                    "grado_actual": datos_alumno[5]
                }
            else:
                return None
        except Exception as e:
            db.session.rollback()
            print(f"Error al buscar inscripcion: {e}")

    #Consulta la lista de alumnos inscritos a un curso(devuelve los nombres completos): necesita el id del curso
    @staticmethod
    def consultar_lista_inscripcion(id_curso):
        try:
            lista_alumnos_inscritos = (db.session.query(Usuario.id_usuario, Usuario.apellido_paterno, Usuario.apellido_materno, Usuario.nombre)
                                       .join(Alumno, Alumno.id_usuario == Usuario.id_usuario)
                                       .join(Inscribir, Inscribir.id_alumno == Alumno.id_usuario)
                                       .filter(Inscribir.id_curso == id_curso)
                                       .all())
            return [{"id_usuario": alumno.id_usuario, "nombre_completo": f"{alumno.apellido_paterno} {alumno.apellido_materno} {alumno.nombre}"
                     } for alumno in lista_alumnos_inscritos]
        except Exception as e:
            db.session.rollback()
            print(f"Error al consultar lista: {e}")
            return []

    #Eliminar inscripcion de un alumno en un curso(devuelve true/false): necesita el id del usuario y del curso
    @staticmethod
    def eliminar_inscripcion(id_usuario, id_curso):
        try:
            inscripcion = Inscribir.query.filter_by(id_alumno = id_usuario, id_curso = id_curso).first()
            if inscripcion:
                db.session.delete(inscripcion)
                db.session.commit()
                return True
            else:
                return False

        except Exception as e:
            db.session.rollback()
            print(f"Error al eliminar alumno: {e}")
            return False

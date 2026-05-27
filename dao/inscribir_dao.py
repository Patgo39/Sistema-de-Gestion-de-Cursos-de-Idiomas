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
            inscripcion = (Inscribir.query
                           .filter_by(id_curso=id_curso, id_alumno=id_usuario)
                           .first())

            if inscripcion and inscripcion.alumno:
                alumno_obj = inscripcion.alumno
                usuario_obj = alumno_obj.perfil_usuario


                return {
                    "nombre_completo": f"{usuario_obj.apellido_paterno or ''} {usuario_obj.apellido_materno or ''} {usuario_obj.nombre or ''}".strip(),
                    "email": usuario_obj.email,
                    "genero": usuario_obj.genero,
                    "fecha_nacimiento" : usuario_obj.fecha_nacimiento,
                    "grado_actual": alumno_obj.grado_actual,
                    "pais": usuario_obj.pais,
                    "ultima_fecha_acceso": usuario_obj.ultima_fecha_acceso

                }
            return None

        except Exception as e:
            db.session.rollback()
            print(f"Error al buscar inscripcion: {e}")
            return None


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

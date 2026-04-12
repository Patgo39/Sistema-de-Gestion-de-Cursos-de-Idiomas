from db import db

class Recurso(db.Model):
    __tablename__ = 'recurso'

    id_recurso = db.Column(db.Integer, primary_key=True)
    nombre_recurso = db.Column(db.String(100), nullable=False)
    archivo_url = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text)
    id_docente = db.Column(db.Integer, db.ForeignKey('Usuario.id_usuario'))
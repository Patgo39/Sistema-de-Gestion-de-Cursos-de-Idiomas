from datetime import datetime
from db import db

class Inscribir(db.Model):
    __tablename__ = 'Inscribir'
    id_usuario = db.Column(db.Integer, db.ForeignKey('Alumno.id_usuario', ondelete='CASCADE'), primary_key=True)
    id_curso = db.Column(db.Integer, db.ForeignKey('Curso.id_curso', ondelete='CASCADE'), primary_key=True)

    fecha_inscripcion = db.Column(db.DateTime, default=datetime.utcnow)

    alumno = db.relationship('Alumno')
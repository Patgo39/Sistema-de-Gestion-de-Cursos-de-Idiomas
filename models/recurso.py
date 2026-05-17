from db import db
from datetime import date


class Recurso(db.Model):
    __tablename__ = 'Recurso'

    id_recurso = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descripcion = db.Column(db.String(255))
    id_curso = db.Column(db.Integer, db.ForeignKey('Curso.id_curso', ondelete='CASCADE'), nullable=False)
    titulo_recurso = db.Column(db.String(100), nullable=False)
    fecha_subida = db.Column(db.Date, default=date.today)
    archivo_url = db.Column(db.String(1024))

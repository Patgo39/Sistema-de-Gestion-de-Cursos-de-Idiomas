from db import db
from datetime import date


class Recurso(db.Model):
    __tablename__ = 'Recurso'

    id_recurso = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_curso = db.Column(db.Integer, db.ForeignKey('Curso.id_curso', ondelete='CASCADE'), nullable=False)

    titulo_recurso = db.Column(db.String(80), nullable=False)
    descripcion = db.Column(db.Text)
    fecha_subida = db.Column(db.Date, default=date.today)
    archivo_url = db.Column(db.String(1024))

from db import db

class Dominar(db.Model):
    __tablename__ = 'Dominar'
    id_idioma = db.Column(db.Integer, db.ForeignKey('Idioma.id_idioma', ondelete='CASCADE'),primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('Alumno.id_usuario', ondelete='CASCADE'), primary_key=True)
    nivel_dominio = db.Column(db.String(30), nullable=False)
    idioma = db.relationship('Idioma')
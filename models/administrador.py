from db import db

class Administrador(db.Model):
    __tablename__ = 'Administrador'
    id_usuario = db.Column(db.Integer, db.ForeignKey('Usuario.id_usuario', ondelete='CASCADE'), primary_key=True)
    nivel_privilegio = db.Column(db.Integer)

    perfil_usuario = db.relationship('Usuario', back_populates='administrador')
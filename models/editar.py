from db import db
from datetime import date

class Editar(db.Model):
    __tablename__ = 'Editar'

    # Llave primaria compuesta
    id_administrador = db.Column(db.Integer, db.ForeignKey('Administrador.id_usuario', ondelete='CASCADE'),
                                 primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('Usuario.id_usuario', ondelete='CASCADE'), primary_key=True)
    fecha_edicion = db.Column(db.Date, default=date.today)

from db import db

class Docente(db.Model):
    __tablename__ = 'Docente'
    id_usuario=db.Column(db.Integer,db.ForeignKey('Usuario.id_usuario', ondelete='CASCADE'),primary_key=True)
    tiempo_experiencia=db.Column(db.Integer)
    especialidad=db.Column(db.String(50))
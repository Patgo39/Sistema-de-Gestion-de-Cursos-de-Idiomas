from db import db

class Alumno(db.Model):
    __tablename__ = 'Alumno'
    id_usuario = db.Column(db.Integer, db.ForeignKey('Usuario.id_usuario', ondelete='CASCADE'),primary_key=True)
    grado_actual=db.Column(db.String(50))
    idiomas_dominados=db.relationship('Dominar',cascade='all, delete-orphan', lazy='dynamic')

    perfil_usuario = db.relationship('Usuario', back_populates='alumno')


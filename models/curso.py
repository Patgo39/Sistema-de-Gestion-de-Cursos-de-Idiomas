from db import db

class Curso(db.Model):
    __tablename__ = 'Curso'
    id_curso = db.Column(db.Integer,primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer,db.ForeignKey('Docente.id_usuario', ondelete='CASCADE'), nullable=False)
    docente = db.relationship('Docente')
    id_idioma = db.Column(db.Integer,db.ForeignKey('Idioma.id_idioma', ondelete='CASCADE'), nullable=False)
    idioma = db.relationship('Idioma')
    nombre_curso = db.Column(db.String(100))
    descripcion = db.Column(db.Text)
    nivel = db.Column(db.String(30))
    lista_inscritos = db.relationship('Inscribir', lazy='dynamic' ,cascade='all, delete-orphan')
    lista_recursos = db.relationship('Recurso', lazy='dynamic' ,cascade='all, delete-orphan')
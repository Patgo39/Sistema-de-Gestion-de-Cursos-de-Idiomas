from db import db

class Usuario(db.Model):
    __tablename__ = 'Usuario'
    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(25), nullable=False)
    nombre = db.Column(db.String(50))
    apellido_paterno = db.Column(db.String(50))
    apellido_materno = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(255))
    genero=db.Column(db.String(50))
    pais=db.Column(db.String(50))
    ultima_fecha_acceso=db.Column(db.DateTime)
    rol=db.Column(db.String(50))

    alumno = db.relationship('Alumno', backref='usuario', cascade='all, delete', uselist=False)
    docente = db.relationship('Docente', backref='usuario', cascade='all, delete', uselist=False)


from db import db

class Idioma(db.Model):
    __tablename__ = 'Idioma'
    id_idioma = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_idioma = db.Column(db.String(50), unique=True, nullable=False)
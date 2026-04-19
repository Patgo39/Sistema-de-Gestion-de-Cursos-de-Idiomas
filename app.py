from flask import Flask, redirect, url_for
from db import db
import os
from dotenv import load_dotenv
from controllers.login_controller import login_bp
from controllers.registro_controller import registro_bp
from controllers.alumno_controller import alumno_bp
from controllers.docente_controller import docente_bp
from controllers.curso_controller import curso_bp
from datetime import timedelta

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

app.config['UPLOAD_FOLDER'] = 'static/uploads/recursos'
user = os.getenv('DB_USER')
password = os.getenv('DB_PASS')
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{user}:{password}@{host}:{port}/defaultdb?ssl_ca=ca.pem"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)

app.register_blueprint(login_bp, url_prefix='/auth')
app.register_blueprint(registro_bp, url_prefix='/sign_up')

app.register_blueprint(alumno_bp, url_prefix='/alumno')
app.register_blueprint(docente_bp, url_prefix='/docente')
app.register_blueprint(curso_bp, url_prefix='/curso')

@app.route('/')
def index():
    return redirect(url_for('auth.iniciar_sesion'))

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)
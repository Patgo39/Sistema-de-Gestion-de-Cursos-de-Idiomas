from flask import Flask, redirect, url_for, render_template, request
from db import db
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus
from controllers.login_controller import login_bp
from controllers.recurso_controller import recursos_bp
from controllers.registro_controller import registro_bp
from controllers.alumno_controller import alumno_bp
from controllers.docente_controller import docente_bp
from controllers.admin_controller import admin_bp
from datetime import timedelta
''''
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
'''

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config['UPLOAD_FOLDER'] = 'static/uploads/recursos'

user = os.getenv('DB_USER')
# 1. Codificamos la contraseña de forma segura
password = quote_plus(os.getenv('DB_PASS'))
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')

# 2. Generamos una ruta absoluta para el certificado (asumiendo que ca.pem está en la misma carpeta que este script)
basedir = os.path.abspath(os.path.dirname(__file__))
ca_cert = os.path.join(basedir, 'ca.pem')

# 3. Armamos la URI inyectando la contraseña codificada y la ruta exacta del certificado
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{user}:{password}@{host}:{port}/defaultdb?ssl_ca={ca_cert}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
app.register_blueprint(login_bp, url_prefix='/auth')
app.register_blueprint(registro_bp, url_prefix='/sign_up')
app.register_blueprint(alumno_bp, url_prefix='/alumno')
app.register_blueprint(docente_bp, url_prefix='/docente')

app.register_blueprint(recursos_bp, url_prefix='/recursos')
app.register_blueprint(admin_bp, url_prefix='/admin')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
      app.run(host="127.0.0.1", port=5000, debug=True)
from flask import Flask, redirect, url_for
from db import db
import os
from dotenv import load_dotenv
from controllers.login_controller import login_bp

# Cargar variables de entorno
load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Configuración de Aiven
user = os.getenv('DB_USER')
password = os.getenv('DB_PASS')
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{user}:{password}@{host}:{port}/defaultdb?ssl_ca=ca.pem"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Conectar la base de datos a la app
db.init_app(app)

app.register_blueprint(login_bp, url_prefix='/auth')

@app.route('/')
def index():
    return redirect(url_for('auth.iniciar_sesion'))

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)
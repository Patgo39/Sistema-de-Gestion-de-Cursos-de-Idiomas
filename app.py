from flask import Flask
from db import db
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/uploads/recursos'
user = os.getenv('DB_USER')
password = os.getenv('DB_PASS')
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{user}:{password}@{host}:{port}/defaultdb?ssl_ca=ca.pem"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)
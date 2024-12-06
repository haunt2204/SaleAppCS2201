from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_login import LoginManager
import cloudinary

app = Flask(__name__)

app.secret_key = "^&$$%$$FGGFAHGA"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/saledb?charset=utf8mb4" % quote('Admin@123')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"] = 8

db = SQLAlchemy(app)
login = LoginManager(app=app)
cloudinary.config(cloud_name='dy1unykph',
                  api_key='238791983534257',
                  api_secret='_J2MkfDJ1DwRe1uAn5TKozXup0U')

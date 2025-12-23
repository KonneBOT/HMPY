from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.jinja_env.autoescape = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://buguser:Heute000@localhost/zugfahrten'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_LOGIN_ATTEMPTS'] = 5
app.config['SECRET_KEY'] = 'ohmaysosecret'

db = SQLAlchemy(app)

from routes import routes
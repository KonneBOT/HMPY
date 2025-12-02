from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.jinja_env.autoescape = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://buguser:Heute000@localhost/zugfahrten'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_LOGIN_ATTEMPTS'] = 5
app.config['SECRET_KEY'] = 'secret'

db = SQLAlchemy(app)

from routes import routes
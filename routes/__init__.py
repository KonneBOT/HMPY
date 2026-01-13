from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import base64
import json

app = Flask(__name__)
app.jinja_env.autoescape = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://buguser:Heute000@localhost/zugfahrten'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_LOGIN_ATTEMPTS'] = 5
app.config['SECRET_KEY'] = 'ohmaysosecret'

db = SQLAlchemy(app)

# Custom Jinja2 Filter für JWT Dekodierung
@app.template_filter('decode_jwt_payload')
def decode_jwt_payload(token):
    try:
        parts = token.split('.')
        if len(parts) == 3:
            payload = parts[0]
            # Base64 Padding hinzufügen falls nötig
            padding = 4 - len(payload) % 4
            if padding != 4:
                payload += '=' * padding
            decoded = base64.urlsafe_b64decode(payload)
            print(decoded)
            return json.loads(decoded)
    except:
        return {}
    return {}

from routes import routes
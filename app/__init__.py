from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from app.config import Settings

app = Flask(__name__)
app.config.from_object(Settings)

db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

# Endpoint
@app.route('/')
def index():
    return jsonify(message='Hola, bienvenido a mi EFI')

from app.views import users, posts, comments

app.register_blueprint(users.bp, url_prefix='/users')
app.register_blueprint(posts.bp, url_prefix='/posts')
app.register_blueprint(comments.bp, url_prefix='/comments')
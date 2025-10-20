from flask import Flask
from .config import Config
from .db import db,migrate
# from app.routes import 
from flask_cors import CORS

def create_app():

    app= Flask(__name__)
    app.config.from_object(config.Config)

    db.init_app(app)

    migrate.init_app(app,db)
    CORS (app)

    # registering blueprints
    # app.register_blueprint("")
    return app
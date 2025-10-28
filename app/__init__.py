from flask import Flask
from flask_cors import CORS
# from app.journals.routes import journal_bp  
from app.config import Config
from app.auth.routes import auth_bp
from app.mood.routes import mood_bp
from app.journals.models import journals_bp
from app.db import db, migrate, jwt, bcrypt


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    CORS(app)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(mood_bp)
    app.register_blueprint(journals_bp)

    # Import models for migrations
    register_models()

    # Add routes
    add_routes(app)

    return app


def register_models():
    #Import models for Flask-Migrate
    try:
        from app.auth import models as auth_models  # noqa: F401
        from app.community import models as community_models  # noqa: F401
        from app.journals import models as journals_models  # noqa: F401
        from app.mood import models as mood_models  # noqa: F401
    except ImportError:
        pass


def add_routes(app):
    @app.route("/")
    def home():
        return {"message": "Welcome to EMAGE home of emotional awereness"}, 200

    @app.route('/test')
    def test():
        return {"message": "Test route works!"}, 200

    @app.route('/routes')
    def list_routes():
        return {
            "routes": [
                {
                    'endpoint': rule.endpoint,
                    'methods': list(rule.methods - {'HEAD', 'OPTIONS'}),
                    'path': str(rule.rule)
                }
                for rule in app.url_map.iter_rules()
            ]
        }, 200
from flask import Flask
from flask_cors import CORS
from app.config import Config
from app.auth.routes import bp
from app.db import db,migrate,jwt,bcrypt
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize app-specific configurations
    # Config.init_app(app)


    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    CORS(app)

    # Import model modules so they are registered with SQLAlchemy metadata.
    # This is necessary for Flask-Migrate / Alembic autogeneration to see
    # all models when you run `flask db migrate`.
    try:
        # these modules define models and may reference `db` from this package
        from app.auth import models as auth_models  # noqa: F401
        from app.community import models as community_models  # noqa: F401
        from app.journals import models as journals_models  # noqa: F401
        from app.mood import models as mood_models  # noqa: F401
    except Exception:
        # If any optional app modules are missing, don't break app creation.
        # Migration autogenerate will only include models that were importable.
        pass

    app.register_blueprint(bp)

    @app.route("/")
    def home():
        # Minimal root route used for health-check / welcome message
        return {"message": "Welcome to the Student Management System"}, 200
    @app.route('/test')
    def test():
        return {"message": "Test route works!"}, 200

    # Also add this to see all registered routes
    @app.route('/routes')
    def list_routes():
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append({
                'endpoint': rule.endpoint,
                'methods': list(rule.methods),
                'path': str(rule.rule)
            })
        return {"routes": routes}, 200

    return app
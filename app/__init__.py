from flask import Flask
from flask_cors import CORS
import os
# from app.journals.routes import journal_bp  
from app.config import Config
from app.db import db, migrate, jwt, bcrypt
from app.auth.routes import auth_bp
from app.mood.routes import mood_bp
from app.journals.routes import journals_bp


def create_app():
    app = Flask(__name__)
    # Allow routes without a trailing slash to be accepted without a redirect.
    app.url_map.strict_slashes = False
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)

    # Configure CORS
    # When requests from the frontend include credentials (cookies/auth headers)
    # the server must set Access-Control-Allow-Credentials: true and must not
    # use a wildcard '*' origin. Use FRONTEND_URL env var or fall back to
    CORS(app, 
         supports_credentials=True,
         origins=[
             "https://emage-app.vercel.app",
             "http://localhost:5173",
             "http://localhost:3000"
         ])
    
     # Add debug route to check CORS
    @app.route('/debug/cors')
    def debug_cors():
        return {
            "message": "CORS test successful",
            "allowed_origins": [
                "https://emage-app.vercel.app",
                "http://localhost:5173", 
                "http://localhost:3000"
            ]
        }, 200

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(mood_bp)
    app.register_blueprint(journals_bp)
    # Register community blueprint (routes define the blueprint)
    try:
        from app.community.routes import community_bp
        app.register_blueprint(community_bp)
    except Exception:
        # If community routes aren't present or error on import, skip registration
        pass


    # Import models for migrations
    register_models()

    # Add routes
    # add_routes(app)

    return app


def register_models():
    #Import models for Flask-Migrate
    try:
        from app.auth import models as auth_models  
        from app.community import models as community_models
        from app.journals import models as journals_models  
        from app.mood import models as mood_models  
    except ImportError:
        pass


# def add_routes(app):
#     @app.route('/routes')
#     def list_routes():
#         return {
#             "routes": [
#                 {
#                     'endpoint': rule.endpoint,
#                     'methods': list(rule.methods - {'HEAD', 'OPTIONS'}),
#                     'path': str(rule.rule)
#                 }
#                 for rule in app.url_map.iter_rules()
#             ]
#         }, 200
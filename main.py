# from app import create_app
# import os
# from dotenv import load_dotenv
# from flask_cors import CORS
# load_dotenv()
#
# app = create_app()
# CORS(app)
#
# # @app.route("/")
# # def home():
# #     return {"message": "Welcome to our mental health app"}, 200
#
#  # Create tables if they don't exist
#  #        from app import db
#
# db.create_all()
#
# if __name__ == "__main__":
#     # Create tables if they don't exist
#     from app import db
#
# db.create_all()
#     app.run(debug=True)


"""Application entrypoint.

This script creates the Flask application using `create_app()` and
ensures the database tables exist by calling `db.create_all()` inside
an application context. For production deployments you should prefer
running migrations (Alembic / Flask-Migrate) instead of `create_all()`.
"""

from app import create_app, db
from dotenv import load_dotenv

load_dotenv()

app = create_app()

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()  # create tables if not exist
    app.run(debug=True,port=5501)
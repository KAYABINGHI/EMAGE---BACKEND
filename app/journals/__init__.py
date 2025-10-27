from flask import Blueprint

journals_bp = Blueprint('journals', __name__, url_prefix="/journals")

from app.journals import routes  # Import routes after blueprint creation
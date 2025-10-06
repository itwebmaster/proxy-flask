from flask import Flask
from flask_session import Session
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    app.config["SESSION_TYPE"] = "filesystem"

    debug_env = os.environ.get("DEBUG", "False").lower()
    app.debug = debug_env in ["1", "true", "yes"]

    Session(app)

    # Blueprints
    from .routes import main_bp
    from .logs import logs_bp
    from .api import api_bp
    from .auth import auth_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(logs_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(auth_bp)

    return app

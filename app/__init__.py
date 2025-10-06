from flask import Flask

def create_app():
    app = Flask(__name__)

     # роутери
        from .routes import main_bp
        app.register_blueprint(main_bp)


    # логування
    from .logs import logs_bp
    app.register_blueprint(logs_bp)

    return app

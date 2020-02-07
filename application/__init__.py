from flask import Flask

app = Flask(__name__)

def create_app():

    with app.app_context():
        from .home import home_routes
        app.register_blueprint(home_routes.home_bp)

    return app


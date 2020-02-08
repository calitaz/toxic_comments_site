from flask import Flask

app = Flask(__name__)

def create_app():

    with app.app_context():
        from .home import home_routes
        from .admin import admin_routes
        app.register_blueprint(home_routes.home_bp)
        app.register_blueprint(admin_routes.admin_bp)

    return app


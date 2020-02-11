import os
from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = '\xfb\x1a\xd7\xda\x04\x15,3\xf3v\xe5\xfeG\xe8\x11\xa8\xba\x11>\xd4V\xe5$\xa0'

def create_app():

    with app.app_context():
        from .home import home_routes
        from .admin import admin_routes
        app.register_blueprint(home_routes.home_bp)
        app.register_blueprint(admin_routes.admin)

    return app


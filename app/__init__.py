from flask import Flask
from . import routes

def create_app(config_class="config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize routes
    routes.init_app(app)

    return app

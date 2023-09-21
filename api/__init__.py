from flask import Flask
from api.extensions import db, user_datastore, security

def create_app(config_name):
    app = Flask(__name__)
    # Load your app configuration here
    
    # Initialize extensions
    db.init_app(app)
    user_datastore.init_app(app)
    security.init_app(app, user_datastore)

    # Register your routes and blueprints here

    return app

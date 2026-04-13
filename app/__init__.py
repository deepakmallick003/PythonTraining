"""
Flask application factory
"""
import os
import secrets
from flask import Flask
from .routes import main_bp, api_bp

def create_app():
    # Get the app directory
    basedir = os.path.abspath(os.path.dirname(__file__))
    
    app = Flask(
        __name__,
        static_folder=os.path.join(basedir, 'static'),
        static_url_path='/static',
        template_folder=os.path.join(basedir, 'templates')
    )
    app.config['JSON_SORT_KEYS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(16))
    app.config['SESSION_TYPE'] = 'filesystem'
    
    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app

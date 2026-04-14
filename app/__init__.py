"""
Flask application factory
"""
import os
import secrets
from pathlib import Path
from flask import Flask


def _load_env_file() -> None:
    """Load simple KEY=VALUE pairs from the project .env file if present."""
    project_root = Path(__file__).resolve().parent.parent
    env_path = project_root / '.env'
    if not env_path.exists():
        return

    for raw_line in env_path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue

        key, value = line.split('=', 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def env_flag(name: str, default: bool = False) -> bool:
    """Read a boolean env flag."""
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {'1', 'true', 'yes', 'on'}


_load_env_file()

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

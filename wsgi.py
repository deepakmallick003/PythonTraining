"""WSGI entry point for hosted deployments."""

from app import create_app


app = create_app()

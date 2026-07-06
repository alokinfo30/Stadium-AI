# app/__init__.py
import logging
import os

from dotenv import load_dotenv
from flask import Flask, request
from flask_cors import CORS

load_dotenv()


def create_app():
    """Application factory pattern for Flask app."""
    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static",
    )

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    app.config["DEBUG"] = os.getenv("DEBUG", "True").lower() == "true"
    app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.before_request
    def limit_body_size():
        if request.content_length and request.content_length > app.config["MAX_CONTENT_LENGTH"]:
            return {"error": "Request body too large", "status": "error"}, 413

    @app.after_request
    def add_security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com; img-src 'self' data:; object-src 'none'; base-uri 'self'"
        )
        return response

    try:
        from app.main import main_bp

        app.register_blueprint(main_bp)
    except ImportError as exc:
        logging.warning(f"Main blueprint not loaded: {exc}")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    return app
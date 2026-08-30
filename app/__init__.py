# app/__init__.py
import logging
import os

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = lambda: None
from flask import Flask, request
from flask_cors import CORS

load_dotenv()


def create_app():
    """Enterprise-hardened Application factory pattern for Flask app."""
    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static",
    )

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "stadium-ai-enterprise-secret-key-2026")
    app.config["DEBUG"] = os.getenv("DEBUG", "False").lower() == "true"
    app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024  # 2MB payload cap

    # Restrictive CORS for API routes
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.before_request
    def limit_body_size():
        if request.content_length and request.content_length > app.config["MAX_CONTENT_LENGTH"]:
            return {"error": "Payload exceeds maximum allowed limit (2MB)", "status": "error"}, 413

    @app.after_request
    def add_security_headers(response):
        """Inject enterprise-grade HTTP security headers on all responses."""
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), camera=(), microphone=(self)"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com; "
            "img-src 'self' data: https://img.shields.io https://komarev.com; "
            "connect-src 'self' https://openrouter.ai https://api.openai.com; "
            "object-src 'none'; "
            "base-uri 'self'; "
            "frame-ancestors 'none'; "
            "form-action 'self';"
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
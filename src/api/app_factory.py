"""Flask Application Factory for modular service initialization."""

from flask import Flask
from flask_cors import CORS
from src.api.middleware import setup_middleware


def create_app(test_config=None) -> Flask:
    """Create and configure an instance of the Flask application."""
    app = Flask(
        "semantic_similarity_studio",
        static_folder="../../static",
        template_folder="../../templates"
    )
    CORS(app)
    setup_middleware(app)

    if test_config:
        app.config.update(test_config)

    # Attach health check
    @app.route("/health", methods=["GET"])
    def health():
        return {"status": "healthy", "service": "semantic-similarity-studio"}, 200

    return app

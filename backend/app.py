"""
Flask Application
Main entry point for the Resume Analyzer API.
"""

import os
import logging
from datetime import datetime
from flask import Flask
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from config import config
from routes import api_bp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_app(config_name=None):
    """
    Application factory pattern

    Args:
        config_name: Configuration to use (development, production, testing)

    Returns:
        Flask application instance
    """
    # Determine config
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    # Create Flask app
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Add startup time for health checks
    app.config['STARTUP_TIME'] = datetime.utcnow()

    # Initialize extensions
    _init_cors(app)
    _init_rate_limiter(app)

    # Register blueprints
    app.register_blueprint(api_bp)

    # Register error handlers
    _register_error_handlers(app)

    # Log startup
    logger.info(f"Application started in {config_name} mode")
    logger.info(f"AI suggestions: {'enabled' if app.config.get('ENABLE_AI_SUGGESTIONS') else 'disabled'}")

    return app


def _init_cors(app):
    """Initialize CORS"""
    CORS(app, resources={
        r"/api/*": {
            "origins": app.config['CORS_ORIGINS'],
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type"],
            "max_age": 3600
        }
    })
    logger.info(f"CORS initialized for origins: {app.config['CORS_ORIGINS']}")


def _init_rate_limiter(app):
    """Initialize rate limiting"""
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        storage_uri=app.config['RATELIMIT_STORAGE_URL'],
        default_limits=[app.config['RATELIMIT_DEFAULT']],
        headers_enabled=app.config['RATELIMIT_HEADERS_ENABLED']
    )
    logger.info(f"Rate limiting initialized: {app.config['RATELIMIT_DEFAULT']}")


def _register_error_handlers(app):
    """Register global error handlers"""

    @app.errorhandler(413)
    def request_entity_too_large(error):
        """Handle file too large errors"""
        from flask import jsonify
        max_mb = app.config['MAX_CONTENT_LENGTH'] / (1024 * 1024)
        return jsonify({
            'success': False,
            'error': {
                'code': 'FILE_TOO_LARGE',
                'message': f'File size exceeds {max_mb}MB limit',
                'details': {'max_size_mb': max_mb}
            }
        }), 413

    @app.errorhandler(500)
    def internal_server_error(error):
        """Handle internal server errors"""
        from flask import jsonify
        logger.error(f"Internal server error: {str(error)}")
        return jsonify({
            'success': False,
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'An internal server error occurred'
            }
        }), 500


# Create app instance
app = create_app()


if __name__ == '__main__':
    # Run development server
    port = int(os.getenv('PORT', 5000))
    app.run(
        host='0.0.0.0',
        port=port,
        debug=app.config['DEBUG']
    )

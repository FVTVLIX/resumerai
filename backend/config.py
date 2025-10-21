"""
Application Configuration
Manages all configuration settings for the Flask application.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Base configuration class"""

    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

    # File Upload Configuration
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB max file size
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
    ALLOWED_EXTENSIONS = {'pdf', 'docx'}
    ALLOWED_MIME_TYPES = {
        'application/pdf',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    }

    # CORS Configuration
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:5173').split(',')

    # Rate Limiting
    RATELIMIT_STORAGE_URL = os.getenv('REDIS_URL', 'memory://')
    RATELIMIT_DEFAULT = "10 per minute"
    RATELIMIT_HEADERS_ENABLED = True

    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4')
    OPENAI_MAX_TOKENS = int(os.getenv('OPENAI_MAX_TOKENS', '1000'))
    OPENAI_TEMPERATURE = float(os.getenv('OPENAI_TEMPERATURE', '0.7'))

    # NLP Configuration
    SPACY_MODEL = os.getenv('SPACY_MODEL', 'en_core_web_lg')

    # Processing Configuration
    MAX_PROCESSING_TIME = int(os.getenv('MAX_PROCESSING_TIME', '30'))  # seconds
    ENABLE_AI_SUGGESTIONS = os.getenv('ENABLE_AI_SUGGESTIONS', 'True').lower() == 'true'

    # File Cleanup
    FILE_RETENTION_HOURS = int(os.getenv('FILE_RETENTION_HOURS', '24'))
    AUTO_CLEANUP = os.getenv('AUTO_CLEANUP', 'True').lower() == 'true'

    @staticmethod
    def init_app(app):
        """Initialize application with config"""
        # Create upload folder if it doesn't exist
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)


class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production environment configuration"""
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Testing environment configuration"""
    TESTING = True
    DEBUG = True
    RATELIMIT_ENABLED = False
    ENABLE_AI_SUGGESTIONS = False  # Mock AI responses in tests


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

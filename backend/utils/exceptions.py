"""
Custom Exceptions
Application-specific exception classes.
"""


class ResumeAnalyzerException(Exception):
    """Base exception for resume analyzer"""
    def __init__(self, message: str, code: str = "GENERAL_ERROR", details: dict = None):
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(self.message)

    def to_dict(self):
        """Convert exception to dictionary for API response"""
        return {
            'success': False,
            'error': {
                'code': self.code,
                'message': self.message,
                'details': self.details
            }
        }


class FileValidationError(ResumeAnalyzerException):
    """Raised when file validation fails"""
    def __init__(self, message: str, details: dict = None):
        super().__init__(message, "FILE_VALIDATION_ERROR", details)


class FileProcessingError(ResumeAnalyzerException):
    """Raised when file processing fails"""
    def __init__(self, message: str, details: dict = None):
        super().__init__(message, "FILE_PROCESSING_ERROR", details)


class NLPProcessingError(ResumeAnalyzerException):
    """Raised when NLP processing fails"""
    def __init__(self, message: str, details: dict = None):
        super().__init__(message, "NLP_PROCESSING_ERROR", details)


class AIServiceError(ResumeAnalyzerException):
    """Raised when AI service fails"""
    def __init__(self, message: str, details: dict = None):
        super().__init__(message, "AI_SERVICE_ERROR", details)


class ConfigurationError(ResumeAnalyzerException):
    """Raised when configuration is invalid"""
    def __init__(self, message: str, details: dict = None):
        super().__init__(message, "CONFIGURATION_ERROR", details)


class RateLimitError(ResumeAnalyzerException):
    """Raised when rate limit is exceeded"""
    def __init__(self, message: str = "Rate limit exceeded", retry_after: int = 60):
        super().__init__(
            message,
            "RATE_LIMIT_EXCEEDED",
            {'retry_after': retry_after}
        )

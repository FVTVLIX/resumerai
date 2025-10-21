"""
Validators
Input validation utilities for file uploads and data.
"""

import os
import magic
from werkzeug.datastructures import FileStorage
from typing import Tuple
from .exceptions import FileValidationError


class FileValidator:
    """Validates uploaded resume files"""

    def __init__(self, allowed_extensions: set, allowed_mime_types: set, max_size: int):
        """
        Initialize file validator

        Args:
            allowed_extensions: Set of allowed file extensions (e.g., {'pdf', 'docx'})
            allowed_mime_types: Set of allowed MIME types
            max_size: Maximum file size in bytes
        """
        self.allowed_extensions = allowed_extensions
        self.allowed_mime_types = allowed_mime_types
        self.max_size = max_size

    def validate(self, file: FileStorage) -> Tuple[bool, str]:
        """
        Validate uploaded file

        Args:
            file: Uploaded file object

        Returns:
            Tuple of (is_valid, error_message)

        Raises:
            FileValidationError: If validation fails
        """
        # Check if file exists
        if not file or not file.filename:
            raise FileValidationError(
                "No file provided",
                {'field': 'file'}
            )

        # Check file extension
        if not self._check_extension(file.filename):
            raise FileValidationError(
                f"Invalid file type. Only {', '.join(self.allowed_extensions).upper()} files are supported",
                {
                    'filename': file.filename,
                    'allowed_types': list(self.allowed_extensions)
                }
            )

        # Check MIME type using magic bytes
        if not self._check_mime_type(file):
            raise FileValidationError(
                "File type verification failed. The file may be corrupted or not a valid document",
                {
                    'filename': file.filename,
                    'allowed_mime_types': list(self.allowed_mime_types)
                }
            )

        # Check file size
        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(0)  # Reset file pointer

        if size > self.max_size:
            size_mb = size / (1024 * 1024)
            max_mb = self.max_size / (1024 * 1024)
            raise FileValidationError(
                f"File size exceeds {max_mb}MB limit",
                {
                    'max_size_mb': max_mb,
                    'received_size_mb': round(size_mb, 2)
                }
            )

        if size == 0:
            raise FileValidationError(
                "File is empty",
                {'filename': file.filename}
            )

        return True, ""

    def _check_extension(self, filename: str) -> bool:
        """Check if file extension is allowed"""
        if '.' not in filename:
            return False
        ext = filename.rsplit('.', 1)[1].lower()
        return ext in self.allowed_extensions

    def _check_mime_type(self, file: FileStorage) -> bool:
        """
        Check MIME type using magic bytes

        Args:
            file: Uploaded file object

        Returns:
            True if MIME type is allowed, False otherwise
        """
        try:
            # Read first 2048 bytes for MIME detection
            file.seek(0)
            header = file.read(2048)
            file.seek(0)  # Reset file pointer

            # Detect MIME type
            mime = magic.from_buffer(header, mime=True)

            return mime in self.allowed_mime_types
        except Exception:
            # If magic fails, fall back to extension check only
            return True


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to prevent security issues

    Args:
        filename: Original filename

    Returns:
        Sanitized filename
    """
    # Remove path components
    filename = os.path.basename(filename)

    # Remove or replace dangerous characters
    dangerous_chars = ['..', '/', '\\', '\x00', '\n', '\r']
    for char in dangerous_chars:
        filename = filename.replace(char, '_')

    # Limit length
    name, ext = os.path.splitext(filename)
    if len(name) > 100:
        name = name[:100]

    return f"{name}{ext}"


def validate_api_key(api_key: str, service_name: str = "API") -> None:
    """
    Validate API key is present

    Args:
        api_key: API key to validate
        service_name: Name of the service (for error messages)

    Raises:
        FileValidationError: If API key is missing or invalid
    """
    if not api_key or api_key.strip() == "":
        from .exceptions import ConfigurationError
        raise ConfigurationError(
            f"{service_name} key is not configured. Please set the API key in environment variables.",
            {'service': service_name}
        )


def is_text_extractable(text: str) -> bool:
    """
    Check if extracted text is valid and meaningful

    Args:
        text: Extracted text

    Returns:
        True if text is valid, False otherwise
    """
    if not text or not text.strip():
        return False

    # Check minimum length (at least 50 characters)
    if len(text.strip()) < 50:
        return False

    # Check if text has at least some alphabetic characters
    alpha_count = sum(c.isalpha() for c in text)
    if alpha_count < 20:
        return False

    return True

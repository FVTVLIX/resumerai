"""
API Routes
Defines all API endpoints for the resume analyzer.
"""

import logging
from flask import Blueprint, request, jsonify, current_app
from werkzeug.exceptions import RequestEntityTooLarge

from services import ResumeAnalyzer
from services.job_scraper import JobScraperService
from services.job_matcher import JobMatcherService
from utils.validators import FileValidator
from utils.exceptions import ResumeAnalyzerException

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint

    Returns:
        JSON response with service status
    """
    try:
        # Check if services are ready
        services_status = {
            'nlp': 'ready',  # Could add actual checks here
            'ai': 'ready' if current_app.config.get('ENABLE_AI_SUGGESTIONS') else 'disabled',
            'file_processor': 'ready'
        }

        return jsonify({
            'status': 'healthy',
            'timestamp': str(current_app.config.get('STARTUP_TIME', '')),
            'services': services_status,
            'version': '1.0.0'
        }), 200

    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500


@api_bp.route('/analyze', methods=['POST'])
def analyze_resume():
    """
    Analyze uploaded resume

    Request:
        - multipart/form-data with 'file' field
        - optional 'job_url' form field for job posting comparison

    Returns:
        JSON response with analysis results and optional job match data

    Errors:
        - 400: Invalid request
        - 413: File too large
        - 422: Processing error
        - 500: Server error
    """
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'NO_FILE',
                    'message': 'No file provided in request',
                    'details': {'field': 'file'}
                }
            }), 400

        file = request.files['file']
        job_url = request.form.get('job_url', '').strip()

        # Validate file
        validator = FileValidator(
            allowed_extensions=current_app.config['ALLOWED_EXTENSIONS'],
            allowed_mime_types=current_app.config['ALLOWED_MIME_TYPES'],
            max_size=current_app.config['MAX_CONTENT_LENGTH']
        )

        try:
            validator.validate(file)
        except ResumeAnalyzerException as e:
            return jsonify(e.to_dict()), 400

        # Initialize analyzer
        analyzer = ResumeAnalyzer(
            upload_folder=current_app.config['UPLOAD_FOLDER'],
            nlp_model=current_app.config['SPACY_MODEL'],
            openai_api_key=current_app.config.get('OPENAI_API_KEY'),
            openai_model=current_app.config.get('OPENAI_MODEL', 'gpt-4'),
            enable_ai_suggestions=current_app.config.get('ENABLE_AI_SUGGESTIONS', True)
        )

        # Perform resume analysis
        result = analyzer.analyze(file)
        response_data = result.to_dict()

        # If job URL provided, perform job matching
        if job_url:
            logger.info(f"Job URL provided: {job_url}")
            try:
                # Scrape job posting
                job_scraper = JobScraperService()
                job_data = job_scraper.scrape_job_posting(job_url)
                logger.info(f"Job scraped successfully: {job_data.get('title', 'N/A')}")

                # Match resume to job
                job_matcher = JobMatcherService()
                job_match_result = job_matcher.match_resume_to_job(response_data, job_data)

                # Add job match data to response
                response_data['job_match'] = job_match_result
                logger.info(f"Job match score: {job_match_result.get('overall_match_score', 0)}")

            except Exception as e:
                # Log error but don't fail the entire request
                logger.error(f"Job matching failed: {str(e)}")
                response_data['job_match'] = {
                    'error': True,
                    'error_message': f"Failed to analyze job posting: {str(e)}",
                    'overall_match_score': 0
                }

        # Return successful response
        return jsonify({
            'success': True,
            'data': response_data
        }), 200

    except ResumeAnalyzerException as e:
        # Handle known exceptions
        logger.error(f"Analysis error: {e.message}")
        return jsonify(e.to_dict()), 422

    except RequestEntityTooLarge:
        # Handle file too large error
        max_mb = current_app.config['MAX_CONTENT_LENGTH'] / (1024 * 1024)
        return jsonify({
            'success': False,
            'error': {
                'code': 'FILE_TOO_LARGE',
                'message': f'File size exceeds {max_mb}MB limit',
                'details': {'max_size_mb': max_mb}
            }
        }), 413

    except Exception as e:
        # Handle unexpected errors
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': {
                'code': 'SERVER_ERROR',
                'message': 'An unexpected error occurred. Please try again later.',
                'details': {}
            }
        }), 500


@api_bp.route('/skills/categories', methods=['GET'])
def get_skill_categories():
    """
    Get list of skill categories

    Returns:
        JSON response with skill categories
    """
    try:
        from utils.constants import SKILL_CATEGORIES

        categories = []
        for key, data in SKILL_CATEGORIES.items():
            categories.append({
                'name': key,
                'display_name': data['display_name'],
                'example_skills': data['keywords'][:5]  # First 5 as examples
            })

        return jsonify({
            'success': True,
            'categories': categories
        }), 200

    except Exception as e:
        logger.error(f"Failed to get skill categories: {str(e)}")
        return jsonify({
            'success': False,
            'error': {
                'code': 'SERVER_ERROR',
                'message': 'Failed to retrieve skill categories'
            }
        }), 500


@api_bp.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': {
            'code': 'NOT_FOUND',
            'message': 'The requested endpoint does not exist'
        }
    }), 404


@api_bp.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    return jsonify({
        'success': False,
        'error': {
            'code': 'METHOD_NOT_ALLOWED',
            'message': 'The HTTP method is not allowed for this endpoint'
        }
    }), 405


@api_bp.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({
        'success': False,
        'error': {
            'code': 'INTERNAL_ERROR',
            'message': 'An internal server error occurred'
        }
    }), 500

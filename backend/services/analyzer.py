"""
Resume Analyzer Service
Orchestrates all services to perform complete resume analysis.
"""

import time
import logging
from typing import Tuple
from werkzeug.datastructures import FileStorage

from models import AnalysisResult
from .file_processor import FileProcessor, clean_text
from .nlp_service import NLPService
from .ai_service import AIService
from utils.exceptions import ResumeAnalyzerException

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ResumeAnalyzer:
    """
    Main analyzer that coordinates all services.

    Workflow:
    1. Process file and extract text
    2. Perform NLP analysis (skills, experience, metrics)
    3. Generate AI suggestions
    4. Calculate scores
    5. Return complete analysis result
    """

    def __init__(
        self,
        upload_folder: str,
        nlp_model: str,
        openai_api_key: str,
        openai_model: str,
        enable_ai_suggestions: bool = True
    ):
        """
        Initialize resume analyzer

        Args:
            upload_folder: Directory for temporary file storage
            nlp_model: spaCy model name
            openai_api_key: OpenAI API key
            openai_model: OpenAI model to use
            enable_ai_suggestions: Whether to generate AI suggestions
        """
        self.file_processor = FileProcessor(upload_folder)
        self.nlp_service = NLPService(nlp_model)
        self.enable_ai_suggestions = enable_ai_suggestions

        if enable_ai_suggestions and openai_api_key:
            self.ai_service = AIService(
                api_key=openai_api_key,
                model=openai_model
            )
        else:
            self.ai_service = None
            logger.warning("AI suggestions disabled")

        logger.info("Resume analyzer initialized")

    def analyze(self, file: FileStorage) -> AnalysisResult:
        """
        Perform complete resume analysis

        Args:
            file: Uploaded resume file

        Returns:
            AnalysisResult object

        Raises:
            ResumeAnalyzerException: If analysis fails
        """
        start_time = time.time()

        try:
            logger.info(f"Starting analysis for file: {file.filename}")

            # Step 1: Extract text from file
            logger.info("Step 1: Extracting text from file")
            text, file_metadata = self.file_processor.process_file(file)
            text = clean_text(text)

            # Step 2: Perform NLP analysis
            logger.info("Step 2: Performing NLP analysis")
            nlp_result = self.nlp_service.analyze(text)

            skills = nlp_result['skills']
            experience = nlp_result['experience']
            education = nlp_result['education']
            metrics = nlp_result['metrics']

            # Calculate total experience years
            if experience:
                total_months = sum(
                    exp.duration_months for exp in experience
                    if exp.duration_months
                )
                metrics.total_experience_years = total_months / 12

            # Step 3: Calculate ATS score
            logger.info("Step 3: Calculating ATS score")
            ats_score = self.nlp_service.calculate_ats_score(text, skills, metrics)

            # Step 4: Generate AI suggestions
            suggestions = []
            if self.enable_ai_suggestions and self.ai_service:
                logger.info("Step 4: Generating AI suggestions")
                try:
                    suggestions = self.ai_service.generate_suggestions({
                        'text': text,
                        'skills': skills,
                        'experience': experience,
                        'metrics': metrics.__dict__
                    })
                except Exception as e:
                    logger.error(f"AI suggestion generation failed: {str(e)}")
                    # Continue without AI suggestions
                    suggestions = []

            # Step 5: Create analysis result
            logger.info("Step 5: Compiling results")
            result = AnalysisResult(
                skills=skills,
                experience=experience,
                education=education,
                suggestions=suggestions,
                metrics=metrics,
                ats_score=ats_score
            )

            # Calculate overall score
            result.calculate_overall_score()

            # Calculate processing time
            result.processing_time = time.time() - start_time

            logger.info(f"Analysis complete in {result.processing_time:.2f}s - Score: {result.overall_score:.2f}")

            return result

        except ResumeAnalyzerException:
            # Re-raise our custom exceptions
            raise
        except Exception as e:
            logger.error(f"Unexpected error during analysis: {str(e)}", exc_info=True)
            raise ResumeAnalyzerException(
                f"Analysis failed: {str(e)}",
                "ANALYSIS_ERROR"
            )

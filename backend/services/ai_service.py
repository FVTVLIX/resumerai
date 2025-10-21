"""
AI Service
Handles AI-powered resume analysis using OpenAI's GPT-4.
Generates personalized improvement suggestions and content analysis.
"""

import logging
import json
from typing import List, Dict
from openai import OpenAI
import time

from models import Skill, Experience
from models.analysis import Suggestion
from utils.exceptions import AIServiceError
from utils.validators import validate_api_key

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AIService:
    """
    Provides AI-powered resume analysis and suggestions.

    Features:
    - Generate improvement suggestions
    - Analyze content quality
    - Provide ATS optimization tips
    """

    def __init__(self, api_key: str, model: str = "gpt-4", max_tokens: int = 1000, temperature: float = 0.7):
        """
        Initialize AI service

        Args:
            api_key: OpenAI API key
            model: Model to use (gpt-4, gpt-3.5-turbo)
            max_tokens: Maximum tokens in response
            temperature: Temperature for generation (0.0-1.0)
        """
        validate_api_key(api_key, "OpenAI")

        self.api_key = api_key
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.client = OpenAI(api_key=api_key)

        logger.info(f"Initialized AI service with model: {model}")

    def generate_suggestions(self, resume_data: Dict) -> List[Suggestion]:
        """
        Generate AI-powered improvement suggestions

        Args:
            resume_data: Dictionary containing resume analysis data
                - text: Resume text
                - skills: List of skills
                - experience: List of experience
                - metrics: Content metrics

        Returns:
            List of Suggestion objects
        """
        try:
            # Construct prompt
            prompt = self._build_suggestions_prompt(resume_data)

            # Call OpenAI API
            response = self._call_openai(
                system_prompt="""You are an expert resume reviewer and career coach with 15+ years of experience.
                Your role is to provide specific, actionable, and constructive feedback to help job seekers improve their resumes.
                Focus on concrete improvements rather than generic advice. Be encouraging but honest.""",
                user_prompt=prompt
            )

            # Parse response into suggestions
            suggestions = self._parse_suggestions_response(response)

            logger.info(f"Generated {len(suggestions)} AI suggestions")
            return suggestions

        except Exception as e:
            logger.error(f"Failed to generate AI suggestions: {str(e)}")
            # Return fallback suggestions instead of failing
            return self._get_fallback_suggestions(resume_data)

    def analyze_content_quality(self, text: str) -> Dict:
        """
        Analyze resume content quality using AI

        Args:
            text: Resume text

        Returns:
            Dictionary with quality analysis
        """
        try:
            prompt = f"""Analyze the following resume content and provide a brief assessment of:
1. Overall writing quality (clarity, professionalism, grammar)
2. Quantification of achievements (use of metrics and numbers)
3. Action verb usage and strength
4. Specificity vs. vagueness

Resume:
{text[:2000]}  # Limit text to avoid token limits

Provide a JSON response with the following structure:
{{
    "writing_quality": "assessment",
    "quantification": "assessment",
    "action_verbs": "assessment",
    "specificity": "assessment",
    "overall_impression": "brief overall assessment"
}}
"""

            response = self._call_openai(
                system_prompt="You are a resume analysis expert. Provide concise, specific assessments.",
                user_prompt=prompt
            )

            # Try to parse JSON response
            try:
                quality_analysis = json.loads(response)
            except json.JSONDecodeError:
                # If not JSON, return text analysis
                quality_analysis = {"overall_impression": response}

            return quality_analysis

        except Exception as e:
            logger.error(f"Failed to analyze content quality: {str(e)}")
            return {
                "overall_impression": "Unable to analyze content quality at this time."
            }

    def _build_suggestions_prompt(self, resume_data: Dict) -> str:
        """Build prompt for generating suggestions"""
        text = resume_data.get('text', '')
        skills = resume_data.get('skills', [])
        experience = resume_data.get('experience', [])
        metrics = resume_data.get('metrics', {})

        prompt = f"""Analyze this resume and provide 5-7 specific, actionable improvement suggestions.

Resume Excerpt:
{text[:1500]}  # Limit to avoid token limits

Current Analysis:
- Skills identified: {len(skills)}
- Experience entries: {len(experience)}
- Action verb usage: {metrics.action_verb_usage:.0%}
- Quantification rate: {metrics.quantification_rate:.0%}

Provide suggestions in the following JSON format:
[
    {{
        "category": "content|formatting|ats|skills|experience",
        "priority": "high|medium|low",
        "suggestion": "Specific suggestion text",
        "examples": ["example 1", "example 2"],
        "rationale": "Why this matters"
    }},
    ...
]

Focus on:
1. Adding quantifiable metrics to achievements
2. Improving action verb usage
3. ATS (Applicant Tracking System) optimization
4. Content clarity and impact
5. Skills presentation
6. Experience description improvements

Be specific and provide before/after examples where possible."""

        return prompt

    def _call_openai(self, system_prompt: str, user_prompt: str, retry_count: int = 3) -> str:
        """
        Call OpenAI API with retry logic

        Args:
            system_prompt: System message
            user_prompt: User message
            retry_count: Number of retries on failure

        Returns:
            Response text

        Raises:
            AIServiceError: If all retries fail
        """
        for attempt in range(retry_count):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    max_tokens=self.max_tokens,
                    temperature=self.temperature
                )

                return response.choices[0].message.content.strip()

            except Exception as e:
                logger.warning(f"OpenAI API call failed (attempt {attempt + 1}/{retry_count}): {str(e)}")

                if attempt < retry_count - 1:
                    # Exponential backoff
                    sleep_time = 2 ** attempt
                    time.sleep(sleep_time)
                else:
                    raise AIServiceError(
                        f"Failed to call OpenAI API after {retry_count} attempts: {str(e)}"
                    )

    def _parse_suggestions_response(self, response: str) -> List[Suggestion]:
        """Parse AI response into Suggestion objects"""
        suggestions = []

        try:
            # Try to parse as JSON
            data = json.loads(response)

            if isinstance(data, list):
                for item in data:
                    suggestion = Suggestion(
                        category=item.get('category', 'content'),
                        priority=item.get('priority', 'medium'),
                        suggestion=item.get('suggestion', ''),
                        examples=item.get('examples', []),
                        rationale=item.get('rationale')
                    )
                    suggestions.append(suggestion)

        except json.JSONDecodeError:
            # If not valid JSON, try to parse as text
            logger.warning("AI response not in JSON format, parsing as text")
            suggestions = self._parse_text_suggestions(response)

        return suggestions

    def _parse_text_suggestions(self, text: str) -> List[Suggestion]:
        """Parse text-based suggestions (fallback)"""
        suggestions = []

        # Split by numbered points
        lines = text.strip().split('\n')
        current_suggestion = []

        for line in lines:
            line = line.strip()

            # Check if line starts with a number (1., 2., etc.)
            if line and line[0].isdigit() and '.' in line[:3]:
                if current_suggestion:
                    # Save previous suggestion
                    suggestion_text = ' '.join(current_suggestion)
                    suggestions.append(Suggestion(
                        category='content',
                        priority='medium',
                        suggestion=suggestion_text
                    ))

                # Start new suggestion
                current_suggestion = [line.split('.', 1)[1].strip() if '.' in line else line]
            elif line:
                current_suggestion.append(line)

        # Add last suggestion
        if current_suggestion:
            suggestion_text = ' '.join(current_suggestion)
            suggestions.append(Suggestion(
                category='content',
                priority='medium',
                suggestion=suggestion_text
            ))

        return suggestions

    def _get_fallback_suggestions(self, resume_data: Dict) -> List[Suggestion]:
        """Return fallback suggestions if AI fails"""
        metrics = resume_data.get('metrics', {})
        suggestions = []

        # Quantification suggestion
        if metrics.quantification_rate < 0.5:
            suggestions.append(Suggestion(
                category='content',
                priority='high',
                suggestion='Add quantifiable metrics to your achievements',
                examples=[
                    'Instead of: "Improved system performance"',
                    'Write: "Improved system performance by 40%, reducing load time from 5s to 3s"'
                ],
                rationale='Numbers make your achievements tangible and memorable'
            ))

        # Action verb suggestion
        if metrics.action_verb_usage < 0.6:
            suggestions.append(Suggestion(
                category='content',
                priority='high',
                suggestion='Start more bullet points with strong action verbs',
                examples=[
                    'Instead of: "Responsible for managing team"',
                    'Write: "Led cross-functional team of 8 developers"'
                ],
                rationale='Action verbs make your resume more dynamic and impactful'
            ))

        # Skills suggestion
        skills_count = len(resume_data.get('skills', []))
        if skills_count < 10:
            suggestions.append(Suggestion(
                category='skills',
                priority='medium',
                suggestion='Include more relevant technical skills',
                examples=[
                    'Add specific technologies, frameworks, and tools you have used',
                    'Include both hard skills (programming languages) and soft skills (leadership)'
                ],
                rationale='ATS systems and recruiters scan for specific skill keywords'
            ))

        # ATS suggestion
        if metrics.keyword_density < 0.10:
            suggestions.append(Suggestion(
                category='ats',
                priority='medium',
                suggestion='Optimize for Applicant Tracking Systems (ATS)',
                examples=[
                    'Use industry-standard job titles',
                    'Include keywords from the job description',
                    'Avoid complex formatting, tables, and graphics'
                ],
                rationale='Most companies use ATS to screen resumes before human review'
            ))

        # Formatting suggestion
        suggestions.append(Suggestion(
            category='formatting',
            priority='low',
            suggestion='Ensure consistent formatting throughout',
            examples=[
                'Use consistent date formats (e.g., "Jan 2020" or "01/2020")',
                'Keep bullet point style uniform',
                'Maintain consistent spacing and font sizes'
            ],
            rationale='Consistent formatting shows attention to detail and professionalism'
        ))

        return suggestions

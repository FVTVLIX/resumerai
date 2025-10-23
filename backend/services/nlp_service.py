"""
NLP Service
Handles natural language processing tasks for resume analysis.
Uses spaCy for entity recognition and skill extraction.
"""

import re
import logging
from typing import List, Dict, Tuple
from collections import Counter
import spacy
from spacy.language import Language

from models import Skill, Experience, Education
from models.analysis import AnalysisMetrics
from utils.constants import (
    SKILL_CATEGORIES, ACTION_VERBS, WEAK_VERBS, JOB_TITLES,
    DEGREE_TYPES, EDUCATION_FIELDS, DATE_PATTERNS, ATS_KEYWORDS
)
from utils.exceptions import NLPProcessingError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NLPService:
    """
    Provides NLP capabilities for resume analysis.

    Features:
    - Skill extraction and categorization
    - Experience parsing
    - Education extraction
    - Content quality analysis
    """

    def __init__(self, model_name: str = "en_core_web_lg"):
        """
        Initialize NLP service

        Args:
            model_name: spaCy model to use
        """
        self.model_name = model_name
        self.nlp = None
        self._load_model()

    def _load_model(self) -> None:
        """Load spaCy model"""
        try:
            self.nlp = spacy.load(self.model_name)
            logger.info(f"Loaded spaCy model: {self.model_name}")
        except OSError:
            logger.error(f"spaCy model '{self.model_name}' not found. Please run: python -m spacy download {self.model_name}")
            raise NLPProcessingError(
                f"NLP model not found. Please install it using: python -m spacy download {self.model_name}",
                {'model': self.model_name}
            )

    def analyze(self, text: str) -> Dict:
        """
        Perform complete NLP analysis on resume text

        Args:
            text: Resume text

        Returns:
            Dictionary containing skills, experience, education, and metrics
        """
        try:
            doc = self.nlp(text)

            return {
                'skills': self.extract_skills(text, doc),
                'experience': self.extract_experience(text, doc),
                'education': self.extract_education(text, doc),
                'metrics': self.analyze_content_quality(text, doc)
            }
        except Exception as e:
            logger.error(f"NLP analysis failed: {str(e)}")
            raise NLPProcessingError(
                f"Failed to analyze resume text: {str(e)}"
            )

    def extract_skills(self, text: str, doc: Language = None) -> List[Skill]:
        """
        Extract skills from resume text

        Args:
            text: Resume text
            doc: spaCy doc object (optional, will create if not provided)

        Returns:
            List of Skill objects
        """
        if doc is None:
            doc = self.nlp(text)

        skills = []
        text_lower = text.lower()

        # Extract skills by category
        for category, data in SKILL_CATEGORIES.items():
            for keyword in data['keywords']:
                # Use regex for whole word matching (case-insensitive)
                pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
                matches = list(re.finditer(pattern, text_lower))

                if matches:
                    # Determine proficiency based on mention count
                    count = len(matches)
                    proficiency = self._determine_proficiency(count)

                    skill = Skill(
                        name=keyword,
                        category=category,
                        proficiency=proficiency,
                        count=count
                    )

                    # Avoid duplicates
                    if skill not in skills:
                        skills.append(skill)

        logger.info(f"Extracted {len(skills)} skills")
        return skills

    def extract_experience(self, text: str, doc: Language = None) -> List[Experience]:
        """
        Extract work experience from resume text

        Args:
            text: Resume text
            doc: spaCy doc object (optional)

        Returns:
            List of Experience objects
        """
        if doc is None:
            doc = self.nlp(text)

        experiences = []

        # Split text into sections
        sections = self._split_into_sections(text)

        # Find experience section
        experience_section = self._find_section(sections, ['experience', 'work history', 'employment', 'professional experience'])

        if not experience_section:
            logger.warning("No experience section found")
            return experiences

        # Extract job entries
        job_entries = self._extract_job_entries(experience_section)

        for entry in job_entries:
            try:
                exp = self._parse_job_entry(entry, doc)
                if exp:
                    experiences.append(exp)
            except Exception as e:
                logger.warning(f"Failed to parse job entry: {str(e)}")
                continue

        logger.info(f"Extracted {len(experiences)} experience entries")
        return experiences

    def extract_education(self, text: str, doc: Language = None) -> List[Education]:
        """
        Extract education from resume text

        Args:
            text: Resume text
            doc: spaCy doc object (optional)

        Returns:
            List of Education objects
        """
        if doc is None:
            doc = self.nlp(text)

        education_list = []

        # Split text into sections
        sections = self._split_into_sections(text)

        # Find education section
        education_section = self._find_section(sections, ['education', 'academic background', 'qualifications'])

        if not education_section:
            logger.warning("No education section found")
            return education_list

        # Extract degrees
        for degree_type in DEGREE_TYPES:
            pattern = r'\b' + re.escape(degree_type) + r'\b'
            matches = re.finditer(pattern, education_section, re.IGNORECASE)

            for match in matches:
                # Extract surrounding context (100 chars before and after)
                start = max(0, match.start() - 100)
                end = min(len(education_section), match.end() + 100)
                context = education_section[start:end]

                # Find field of study
                field = self._extract_field_of_study(context)

                # Find institution (organization entities)
                doc_context = self.nlp(context)
                institutions = [ent.text for ent in doc_context.ents if ent.label_ == "ORG"]
                institution = institutions[0] if institutions else ""

                # Find year
                year = self._extract_year(context)

                education = Education(
                    degree=match.group(),
                    field_of_study=field,
                    institution=institution,
                    year=year
                )

                if education not in education_list:
                    education_list.append(education)

        logger.info(f"Extracted {len(education_list)} education entries")
        return education_list

    def analyze_content_quality(self, text: str, doc: Language = None) -> AnalysisMetrics:
        """
        Analyze content quality of resume

        Args:
            text: Resume text
            doc: spaCy doc object (optional)

        Returns:
            AnalysisMetrics object
        """
        if doc is None:
            doc = self.nlp(text)

        metrics = AnalysisMetrics()

        # Total words
        metrics.total_words = len([token for token in doc if not token.is_punct and not token.is_space])

        # Extract bullet points
        bullets = self._extract_bullet_points(text)

        # Action verb usage
        if bullets:
            action_verb_count = sum(1 for bullet in bullets if self._starts_with_action_verb(bullet))
            metrics.action_verb_usage = action_verb_count / len(bullets)
        else:
            metrics.action_verb_usage = 0.0

        # Quantification rate (bullets with numbers)
        if bullets:
            quantified_count = sum(1 for bullet in bullets if any(char.isdigit() for char in bullet))
            metrics.quantification_rate = quantified_count / len(bullets)
        else:
            metrics.quantification_rate = 0.0

        # Keyword density (ATS keywords per 100 words)
        if metrics.total_words > 0:
            text_lower = text.lower()
            keyword_count = sum(1 for keyword in ATS_KEYWORDS if keyword in text_lower)
            metrics.keyword_density = (keyword_count / metrics.total_words) * 100
        else:
            metrics.keyword_density = 0.0

        # Average bullet length
        if bullets:
            total_bullet_words = sum(len(bullet.split()) for bullet in bullets)
            metrics.avg_bullet_length = total_bullet_words / len(bullets)
        else:
            metrics.avg_bullet_length = 0.0

        return metrics

    # Helper methods

    def _determine_proficiency(self, count: int) -> str:
        """Determine proficiency level based on mention count"""
        if count >= 5:
            return "advanced"
        elif count >= 3:
            return "intermediate"
        else:
            return "beginner"

    def _split_into_sections(self, text: str) -> List[str]:
        """Split resume text into sections"""
        # Common section headers
        section_headers = [
            'experience', 'work history', 'employment', 'professional experience',
            'education', 'academic background', 'qualifications',
            'skills', 'technical skills', 'core competencies',
            'projects', 'certifications', 'awards', 'summary', 'objective'
        ]

        # Create regex pattern for section headers
        pattern = r'\n\s*(' + '|'.join(section_headers) + r')[\s:]*\n'
        sections = re.split(pattern, text, flags=re.IGNORECASE)

        return sections

    def _find_section(self, sections: List[str], keywords: List[str]) -> str:
        """Find section matching keywords"""
        for i, section in enumerate(sections):
            section_lower = section.lower().strip()
            if any(keyword in section_lower for keyword in keywords):
                # Return the next section (content)
                if i + 1 < len(sections):
                    return sections[i + 1]
        return ""

    def _extract_job_entries(self, text: str) -> List[str]:
        """Split experience section into individual job entries"""
        # Try to split by job titles or dates
        lines = text.strip().split('\n')

        entries = []
        current_entry = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Check if line looks like a job title (matches known titles or all caps)
            is_title_line = (
                any(title.lower() in line.lower() for title in JOB_TITLES) or
                self._looks_like_date_range(line)
            )

            if is_title_line and current_entry:
                # Start new entry
                entries.append('\n'.join(current_entry))
                current_entry = [line]
            else:
                current_entry.append(line)

        # Add last entry
        if current_entry:
            entries.append('\n'.join(current_entry))

        return entries

    def _parse_job_entry(self, entry: str, doc: Language) -> Experience:
        """Parse individual job entry"""
        lines = [line.strip() for line in entry.split('\n') if line.strip()]

        if not lines:
            return None

        # First line is usually title/company
        first_line = lines[0]

        # Extract title and company
        title, company = self._extract_title_and_company(first_line, doc)

        # Extract dates
        start_date, end_date = self._extract_dates(entry)

        # Extract responsibilities (bullet points)
        responsibilities = self._extract_bullet_points('\n'.join(lines[1:]))

        exp = Experience(
            title=title or "Position",
            company=company or "Company",
            start_date=start_date,
            end_date=end_date,
            responsibilities=responsibilities
        )

        # Calculate duration
        exp.calculate_duration()

        return exp

    def _extract_title_and_company(self, text: str, doc: Language) -> Tuple[str, str]:
        """Extract job title and company from text"""
        title = ""
        company = ""

        # Check for known job titles
        for job_title in JOB_TITLES:
            if job_title.lower() in text.lower():
                title = job_title
                break

        # Extract company using NER
        doc_text = doc if isinstance(doc, Language) else self.nlp(text)
        for ent in doc_text.ents:
            if ent.label_ == "ORG" and not company:
                company = ent.text
                break

        # If no title found, use first part before comma or dash
        if not title:
            parts = re.split(r'[,|\-–—]', text)
            if parts:
                title = parts[0].strip()

        return title, company

    def _extract_dates(self, text: str) -> Tuple[str, str]:
        """Extract start and end dates from text"""
        # Find date ranges
        date_range_pattern = r'(\d{4})\s*[-–—]\s*(\d{4}|present|current)'
        match = re.search(date_range_pattern, text, re.IGNORECASE)

        if match:
            start_date = match.group(1)
            end_date = match.group(2)
            return start_date, end_date

        # Find individual dates
        year_pattern = r'\b(19|20)\d{2}\b'
        years = re.findall(year_pattern, text)

        if years:
            if len(years) >= 2:
                return years[0], years[1]
            else:
                return years[0], "Present"

        return None, None

    def _extract_field_of_study(self, text: str) -> str:
        """Extract field of study from education text"""
        for field in EDUCATION_FIELDS:
            if field.lower() in text.lower():
                return field
        return None

    def _extract_year(self, text: str) -> int:
        """Extract graduation year from text"""
        year_pattern = r'\b(19|20)\d{2}\b'
        matches = re.findall(year_pattern, text)

        if matches:
            # Return the most recent year
            years = [int(year) for year in matches]
            return max(years)

        return None

    def _extract_bullet_points(self, text: str) -> List[str]:
        """Extract bullet points from text"""
        bullets = []

        # Common bullet point markers
        bullet_markers = [r'•', r'\*', r'-', r'·', r'○', r'▪']

        for line in text.split('\n'):
            line = line.strip()

            # Check if line starts with a bullet marker
            for marker in bullet_markers:
                if re.match(f'^{marker}\\s+', line):
                    bullet = re.sub(f'^{marker}\\s+', '', line)
                    if bullet:
                        bullets.append(bullet)
                    break

        return bullets

    def _starts_with_action_verb(self, text: str) -> bool:
        """Check if text starts with an action verb"""
        words = text.lower().split()
        if not words:
            return False

        first_word = words[0]

        # Check if first word is an action verb
        return first_word in ACTION_VERBS

    def _looks_like_date_range(self, text: str) -> bool:
        """Check if text contains a date range"""
        date_range_pattern = r'\d{4}\s*[-–—]\s*(\d{4}|present|current)'
        return bool(re.search(date_range_pattern, text, re.IGNORECASE))

    def calculate_ats_score(self, text: str, skills: List[Skill], metrics: AnalysisMetrics) -> float:
        """
        Calculate ATS (Applicant Tracking System) compatibility score

        Args:
            text: Resume text
            skills: Extracted skills
            metrics: Content metrics

        Returns:
            ATS score (0-100)
        """
        score = 0.0

        # Skills presence (40 points)
        skill_count = len(skills)
        if skill_count >= 15:
            score += 40
        elif skill_count >= 10:
            score += 30
        elif skill_count >= 5:
            score += 20
        else:
            score += skill_count * 3

        # Keyword density (30 points)
        if metrics.keyword_density >= 0.15:
            score += 30
        elif metrics.keyword_density >= 0.10:
            score += 20
        else:
            score += metrics.keyword_density * 150

        # Action verb usage (20 points)
        score += metrics.action_verb_usage * 20

        # Quantification (10 points)
        score += metrics.quantification_rate * 10

        return min(100, score)

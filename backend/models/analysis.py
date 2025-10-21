"""
Analysis Model
Represents the complete resume analysis result.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from .skill import Skill
from .experience import Experience, Education


@dataclass
class Suggestion:
    """Model for an AI-generated suggestion"""

    category: str  # 'content', 'formatting', 'ats', 'skills'
    priority: str  # 'high', 'medium', 'low'
    suggestion: str
    examples: List[str] = field(default_factory=list)
    rationale: Optional[str] = None

    def to_dict(self):
        """Convert suggestion to dictionary"""
        return {
            'category': self.category,
            'priority': self.priority,
            'suggestion': self.suggestion,
            'examples': self.examples,
            'rationale': self.rationale
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Create suggestion from dictionary"""
        return cls(
            category=data['category'],
            priority=data['priority'],
            suggestion=data['suggestion'],
            examples=data.get('examples', []),
            rationale=data.get('rationale')
        )


@dataclass
class AnalysisMetrics:
    """Detailed analysis metrics"""

    total_experience_years: float = 0.0
    action_verb_usage: float = 0.0  # Percentage (0.0 - 1.0)
    quantification_rate: float = 0.0  # Percentage of bullets with numbers
    keyword_density: float = 0.0  # Relevant keywords per 100 words
    avg_bullet_length: float = 0.0  # Average words per bullet point
    total_words: int = 0

    def to_dict(self):
        """Convert metrics to dictionary"""
        return {
            'total_experience_years': round(self.total_experience_years, 1),
            'action_verb_usage': round(self.action_verb_usage, 2),
            'quantification_rate': round(self.quantification_rate, 2),
            'keyword_density': round(self.keyword_density, 2),
            'avg_bullet_length': round(self.avg_bullet_length, 1),
            'total_words': self.total_words
        }


@dataclass
class AnalysisResult:
    """Complete analysis result"""

    overall_score: float = 0.0
    ats_score: float = 0.0
    skills: List[Skill] = field(default_factory=list)
    experience: List[Experience] = field(default_factory=list)
    education: List[Education] = field(default_factory=list)
    suggestions: List[Suggestion] = field(default_factory=list)
    metrics: AnalysisMetrics = field(default_factory=AnalysisMetrics)
    processing_time: float = 0.0

    def to_dict(self):
        """Convert analysis result to dictionary"""
        # Categorize skills
        skills_by_category = {}
        for skill in self.skills:
            if skill.category not in skills_by_category:
                skills_by_category[skill.category] = []
            skills_by_category[skill.category].append(skill.to_dict())

        return {
            'overall_score': round(self.overall_score, 2),
            'ats_score': round(self.ats_score, 2),
            'skills': {
                'technical': [s.to_dict() for s in self.skills if s.category in [
                    'programming_languages', 'frameworks', 'databases', 'tools', 'cloud'
                ]],
                'soft': [s.to_dict() for s in self.skills if s.category == 'soft_skills'],
                'categories': skills_by_category
            },
            'experience': [exp.to_dict() for exp in self.experience],
            'education': [edu.to_dict() for edu in self.education],
            'ai_suggestions': [sug.to_dict() for sug in self.suggestions],
            'ats_recommendations': self._get_ats_recommendations(),
            'analysis': self.metrics.to_dict(),
            'processing_time': round(self.processing_time, 2)
        }

    def _get_ats_recommendations(self) -> List[str]:
        """Generate ATS-specific recommendations based on analysis"""
        recommendations = []

        if self.ats_score < 70:
            recommendations.append("Add more industry-specific keywords")

        if self.metrics.keyword_density < 0.10:
            recommendations.append("Increase keyword density for better ATS matching")

        if len(self.skills) < 10:
            recommendations.append("Include more relevant technical skills")

        if self.metrics.action_verb_usage < 0.60:
            recommendations.append("Start more bullet points with strong action verbs")

        return recommendations

    def calculate_overall_score(self):
        """Calculate overall score based on multiple factors"""
        scores = {
            'skills_diversity': self._score_skills_diversity(),
            'experience_depth': self._score_experience_depth(),
            'content_quality': self._score_content_quality(),
            'ats_optimization': self.ats_score
        }

        # Weighted average
        weights = {
            'skills_diversity': 0.30,
            'experience_depth': 0.25,
            'content_quality': 0.25,
            'ats_optimization': 0.20
        }

        self.overall_score = sum(
            scores[key] * weights[key] for key in scores
        )

        return self.overall_score

    def _score_skills_diversity(self) -> float:
        """Score based on number and diversity of skills"""
        skill_count = len(self.skills)
        category_count = len(set(skill.category for skill in self.skills))

        # Base score on skill count (0-70 points)
        if skill_count >= 15:
            count_score = 70
        elif skill_count >= 10:
            count_score = 50
        elif skill_count >= 5:
            count_score = 30
        else:
            count_score = skill_count * 5

        # Bonus for category diversity (0-30 points)
        if category_count >= 5:
            diversity_score = 30
        elif category_count >= 3:
            diversity_score = 20
        else:
            diversity_score = category_count * 7

        return min(100, count_score + diversity_score)

    def _score_experience_depth(self) -> float:
        """Score based on years and quality of experience"""
        years = self.metrics.total_experience_years

        # Years score (0-60 points)
        if years >= 5:
            years_score = 60
        elif years >= 3:
            years_score = 45
        elif years >= 1:
            years_score = 30
        else:
            years_score = years * 20

        # Quality score based on bullet points (0-40 points)
        total_bullets = sum(
            len(exp.responsibilities) + len(exp.achievements)
            for exp in self.experience
        )
        if total_bullets >= 15:
            quality_score = 40
        elif total_bullets >= 10:
            quality_score = 30
        elif total_bullets >= 5:
            quality_score = 20
        else:
            quality_score = total_bullets * 3

        return min(100, years_score + quality_score)

    def _score_content_quality(self) -> float:
        """Score based on writing quality metrics"""
        # Action verb usage (0-40 points)
        action_verb_score = self.metrics.action_verb_usage * 40

        # Quantification (0-30 points)
        quantification_score = self.metrics.quantification_rate * 30

        # Keyword density (0-30 points)
        keyword_score = min(30, self.metrics.keyword_density * 200)

        return action_verb_score + quantification_score + keyword_score

    @classmethod
    def from_dict(cls, data: dict):
        """Create analysis result from dictionary"""
        skills = [Skill.from_dict(s) for s in data.get('skills', [])]
        experience = [Experience.from_dict(e) for e in data.get('experience', [])]
        education = [Education.from_dict(e) for e in data.get('education', [])]
        suggestions = [Suggestion.from_dict(s) for s in data.get('suggestions', [])]

        return cls(
            overall_score=data.get('overall_score', 0.0),
            ats_score=data.get('ats_score', 0.0),
            skills=skills,
            experience=experience,
            education=education,
            suggestions=suggestions,
            processing_time=data.get('processing_time', 0.0)
        )

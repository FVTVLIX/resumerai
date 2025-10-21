"""
Skill Model
Represents a skill extracted from a resume.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Skill:
    """Model for a skill identified in a resume"""

    name: str
    category: str  # e.g., 'programming_languages', 'frameworks', 'tools'
    proficiency: Optional[str] = None  # 'beginner', 'intermediate', 'advanced'
    count: int = 1  # Number of times mentioned in resume

    def to_dict(self):
        """Convert skill to dictionary"""
        return {
            'name': self.name,
            'category': self.category,
            'proficiency': self.proficiency,
            'count': self.count
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Create skill from dictionary"""
        return cls(
            name=data['name'],
            category=data['category'],
            proficiency=data.get('proficiency'),
            count=data.get('count', 1)
        )

    def __str__(self):
        """String representation"""
        return f"{self.name} ({self.category})"

    def __eq__(self, other):
        """Check equality based on name and category"""
        if not isinstance(other, Skill):
            return False
        return self.name.lower() == other.name.lower() and self.category == other.category

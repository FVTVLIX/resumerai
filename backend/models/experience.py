"""
Experience Model
Represents work experience extracted from a resume.
"""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime


@dataclass
class Experience:
    """Model for work experience"""

    title: str
    company: str
    start_date: Optional[str] = None  # Format: YYYY-MM or YYYY
    end_date: Optional[str] = None  # Format: YYYY-MM or YYYY or 'Present'
    duration_months: Optional[int] = None
    location: Optional[str] = None
    responsibilities: List[str] = field(default_factory=list)
    achievements: List[str] = field(default_factory=list)

    def to_dict(self):
        """Convert experience to dictionary"""
        return {
            'title': self.title,
            'company': self.company,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'duration_months': self.duration_months,
            'location': self.location,
            'responsibilities': self.responsibilities,
            'achievements': self.achievements
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Create experience from dictionary"""
        return cls(
            title=data['title'],
            company=data['company'],
            start_date=data.get('start_date'),
            end_date=data.get('end_date'),
            duration_months=data.get('duration_months'),
            location=data.get('location'),
            responsibilities=data.get('responsibilities', []),
            achievements=data.get('achievements', [])
        )

    def calculate_duration(self):
        """Calculate duration in months from dates"""
        if not self.start_date:
            return None

        try:
            # Parse start date
            start = self._parse_date(self.start_date)

            # Parse end date or use current date
            if self.end_date and self.end_date.lower() != 'present':
                end = self._parse_date(self.end_date)
            else:
                end = datetime.now()

            # Calculate months
            months = (end.year - start.year) * 12 + (end.month - start.month)
            self.duration_months = max(1, months)  # Minimum 1 month
            return self.duration_months

        except Exception:
            return None

    @staticmethod
    def _parse_date(date_str: str) -> datetime:
        """Parse date string in various formats"""
        # Try YYYY-MM format
        try:
            return datetime.strptime(date_str, '%Y-%m')
        except ValueError:
            pass

        # Try YYYY format
        try:
            return datetime.strptime(date_str, '%Y')
        except ValueError:
            pass

        # Default to current date if parsing fails
        return datetime.now()

    def __str__(self):
        """String representation"""
        return f"{self.title} at {self.company}"


@dataclass
class Education:
    """Model for education"""

    degree: str
    field_of_study: Optional[str] = None
    institution: str = ""
    year: Optional[int] = None
    gpa: Optional[float] = None
    honors: List[str] = field(default_factory=list)

    def to_dict(self):
        """Convert education to dictionary"""
        return {
            'degree': self.degree,
            'field': self.field_of_study,  # Keep 'field' in dict for API compatibility
            'institution': self.institution,
            'year': self.year,
            'gpa': self.gpa,
            'honors': self.honors
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Create education from dictionary"""
        return cls(
            degree=data['degree'],
            field_of_study=data.get('field'),  # Accept 'field' from API
            institution=data.get('institution', ''),
            year=data.get('year'),
            gpa=data.get('gpa'),
            honors=data.get('honors', [])
        )

    def __str__(self):
        """String representation"""
        parts = [self.degree]
        if self.field_of_study:
            parts.append(f"in {self.field_of_study}")
        if self.institution:
            parts.append(f"from {self.institution}")
        return " ".join(parts)

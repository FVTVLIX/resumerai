"""
Job Matcher Service

Compares resume analysis results against job posting requirements
to calculate match score and provide recommendations.
"""

from typing import Dict, List, Set
import re


class JobMatcherService:
    """Service for matching resumes to job postings"""

    def __init__(self):
        self.weight_skills = 0.40  # 40% weight on skills match
        self.weight_experience = 0.25  # 25% weight on experience
        self.weight_keywords = 0.20  # 20% weight on keyword match
        self.weight_education = 0.15  # 15% weight on education

    def match_resume_to_job(
        self,
        resume_analysis: Dict,
        job_data: Dict
    ) -> Dict:
        """
        Compare resume analysis to job posting and calculate match score

        Args:
            resume_analysis: Analyzed resume data
            job_data: Scraped job posting data

        Returns:
            Dictionary containing match results
        """
        match_result = {
            'job_title': job_data.get('title', 'N/A'),
            'job_company': job_data.get('company', 'N/A'),
            'job_source': job_data.get('source', 'N/A'),
            'job_url': job_data.get('url', ''),
        }

        # Calculate individual match scores
        skills_match = self._match_skills(resume_analysis, job_data)
        experience_match = self._match_experience(resume_analysis, job_data)
        keywords_match = self._match_keywords(resume_analysis, job_data)
        education_match = self._match_education(resume_analysis, job_data)

        # Calculate overall match score
        overall_score = (
            skills_match['score'] * self.weight_skills +
            experience_match['score'] * self.weight_experience +
            keywords_match['score'] * self.weight_keywords +
            education_match['score'] * self.weight_education
        )

        match_result['overall_match_score'] = round(overall_score, 2)
        match_result['skills_match'] = skills_match
        match_result['experience_match'] = experience_match
        match_result['keywords_match'] = keywords_match
        match_result['education_match'] = education_match

        # Generate recommendations
        match_result['recommendations'] = self._generate_recommendations(
            resume_analysis,
            job_data,
            skills_match,
            keywords_match
        )

        return match_result

    def _match_skills(self, resume: Dict, job: Dict) -> Dict:
        """Match resume skills against job required skills"""
        # Get resume skills
        resume_skills = set()
        for skill in resume.get('skills', {}).get('technical', []):
            resume_skills.add(skill['name'].lower())
        for skill in resume.get('skills', {}).get('soft', []):
            resume_skills.add(skill['name'].lower())

        # Get job required skills
        job_skills = set(skill.lower() for skill in job.get('required_skills', []))

        if not job_skills:
            # If no specific skills found, extract from description
            job_skills = self._extract_skills_from_text(job.get('description', ''))

        # Calculate matches
        matching_skills = resume_skills.intersection(job_skills)
        missing_skills = job_skills - resume_skills

        # Calculate score
        if job_skills:
            score = (len(matching_skills) / len(job_skills)) * 100
        else:
            score = 50  # Neutral score if no job skills found

        return {
            'score': round(score, 2),
            'matching_skills': list(matching_skills),
            'missing_skills': list(missing_skills),
            'total_job_skills': len(job_skills),
            'matched_count': len(matching_skills)
        }

    def _match_experience(self, resume: Dict, job: Dict) -> Dict:
        """Match resume experience against job requirements"""
        resume_years = resume.get('analysis', {}).get('total_experience_years', 0)

        # Try to extract required years from job description
        required_years = self._extract_required_years(job.get('description', ''))

        score = 0
        if required_years == 0:
            # No specific requirement found
            score = 75 if resume_years > 0 else 50
        elif resume_years >= required_years:
            # Meets or exceeds requirement
            score = 100
        elif resume_years >= required_years * 0.8:
            # Close to requirement (80%+)
            score = 80
        elif resume_years >= required_years * 0.5:
            # Halfway there
            score = 60
        else:
            # Below half the requirement
            score = 40

        return {
            'score': score,
            'resume_years': resume_years,
            'required_years': required_years,
            'meets_requirement': resume_years >= required_years if required_years > 0 else None
        }

    def _match_keywords(self, resume: Dict, job: Dict) -> Dict:
        """Match resume content against job keywords"""
        job_keywords = job.get('keywords', [])

        if not job_keywords:
            return {
                'score': 50,
                'matching_keywords': [],
                'suggested_keywords': []
            }

        # Extract resume text for comparison
        resume_text = self._get_resume_text(resume)

        matching = []
        missing = []

        for keyword in job_keywords:
            if self._text_contains_keyword(resume_text, keyword):
                matching.append(keyword)
            else:
                missing.append(keyword)

        score = (len(matching) / len(job_keywords)) * 100 if job_keywords else 50

        return {
            'score': round(score, 2),
            'matching_keywords': matching[:5],  # Top 5
            'suggested_keywords': missing[:5]  # Top 5 missing
        }

    def _match_education(self, resume: Dict, job: Dict) -> Dict:
        """Match education requirements"""
        resume_education = resume.get('education', [])
        job_description = job.get('description', '').lower()

        # Check for degree requirements
        has_bachelors = any('bachelor' in str(edu.get('degree', '')).lower() for edu in resume_education)
        has_masters = any('master' in str(edu.get('degree', '')).lower() for edu in resume_education)
        has_phd = any('phd' in str(edu.get('degree', '')).lower() or 'doctorate' in str(edu.get('degree', '')).lower() for edu in resume_education)

        requires_bachelors = 'bachelor' in job_description
        requires_masters = 'master' in job_description
        requires_phd = 'phd' in job_description or 'doctorate' in job_description

        score = 50  # Default neutral score

        if requires_phd:
            score = 100 if has_phd else 60 if has_masters else 40 if has_bachelors else 20
        elif requires_masters:
            score = 100 if (has_masters or has_phd) else 70 if has_bachelors else 30
        elif requires_bachelors:
            score = 100 if (has_bachelors or has_masters or has_phd) else 50
        else:
            # No specific requirement
            score = 75 if resume_education else 50

        return {
            'score': score,
            'has_degree': len(resume_education) > 0,
            'degree_level': (
                'PhD' if has_phd else
                'Masters' if has_masters else
                'Bachelors' if has_bachelors else
                'None'
            ),
            'meets_requirement': True  # Assume met unless specific requirement found
        }

    def _generate_recommendations(
        self,
        resume: Dict,
        job: Dict,
        skills_match: Dict,
        keywords_match: Dict
    ) -> List[Dict]:
        """Generate personalized recommendations to improve job match"""
        recommendations = []

        # Missing skills recommendations
        if skills_match['missing_skills']:
            missing_count = len(skills_match['missing_skills'])
            recommendations.append({
                'type': 'skills',
                'priority': 'high',
                'title': f"Add {missing_count} missing key skills",
                'description': f"The job posting mentions these skills that are not in your resume: {', '.join(skills_match['missing_skills'][:5])}",
                'action': 'Consider adding these skills to your resume if you have experience with them, or highlight related experience.'
            })

        # Keyword optimization
        if keywords_match['suggested_keywords']:
            recommendations.append({
                'type': 'keywords',
                'priority': 'medium',
                'title': 'Incorporate key phrases from job description',
                'description': 'Your resume is missing some important phrases from the job posting.',
                'action': f"Try to naturally include phrases like: {', '.join(keywords_match['suggested_keywords'][:3])}"
            })

        # Experience recommendations
        resume_years = resume.get('analysis', {}).get('total_experience_years', 0)
        required_years = self._extract_required_years(job.get('description', ''))

        if required_years > 0 and resume_years < required_years:
            recommendations.append({
                'type': 'experience',
                'priority': 'high',
                'title': 'Highlight relevant experience',
                'description': f"The job requires {required_years} years of experience, you have {resume_years} years listed.",
                'action': 'Emphasize transferable skills and any relevant project experience to strengthen your application.'
            })

        # Action verb usage
        action_verb_usage = resume.get('analysis', {}).get('action_verb_usage', 0)
        if action_verb_usage < 0.6:
            recommendations.append({
                'type': 'content',
                'priority': 'medium',
                'title': 'Use more action verbs',
                'description': 'Strong resumes typically start bullet points with action verbs.',
                'action': 'Rewrite accomplishments using verbs like: led, developed, implemented, achieved, improved.'
            })

        # Quantification
        quantification_rate = resume.get('analysis', {}).get('quantification_rate', 0)
        if quantification_rate < 0.5:
            recommendations.append({
                'type': 'content',
                'priority': 'medium',
                'title': 'Add more quantifiable achievements',
                'description': 'Numbers and metrics make your accomplishments more impactful.',
                'action': 'Add specific numbers, percentages, or metrics to demonstrate your impact.'
            })

        return recommendations

    def _extract_skills_from_text(self, text: str) -> Set[str]:
        """Extract skills from text using common patterns"""
        common_skills = [
            'python', 'java', 'javascript', 'react', 'angular', 'vue',
            'node', 'sql', 'aws', 'azure', 'docker', 'kubernetes',
            'agile', 'scrum', 'git', 'machine learning', 'ai'
        ]

        found_skills = set()
        text_lower = text.lower()

        for skill in common_skills:
            if skill in text_lower:
                found_skills.add(skill)

        return found_skills

    def _extract_required_years(self, text: str) -> int:
        """Extract required years of experience from job description"""
        # Common patterns: "5+ years", "3-5 years", "minimum 2 years"
        patterns = [
            r'(\d+)\+?\s*(?:or more\s+)?years',
            r'minimum\s+(?:of\s+)?(\d+)\s+years',
            r'at least\s+(\d+)\s+years',
            r'(\d+)-\d+\s+years'
        ]

        text_lower = text.lower()
        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                return int(match.group(1))

        return 0

    def _get_resume_text(self, resume: Dict) -> str:
        """Get all text content from resume for comparison"""
        text_parts = []

        # Add skills
        for skill in resume.get('skills', {}).get('technical', []):
            text_parts.append(skill['name'])
        for skill in resume.get('skills', {}).get('soft', []):
            text_parts.append(skill['name'])

        # Add experience
        for exp in resume.get('experience', []):
            text_parts.append(exp.get('title', ''))
            text_parts.append(exp.get('company', ''))
            for resp in exp.get('responsibilities', []):
                text_parts.append(resp)

        # Add education
        for edu in resume.get('education', []):
            text_parts.append(edu.get('degree', ''))
            text_parts.append(edu.get('field_of_study', ''))

        return ' '.join(text_parts).lower()

    def _text_contains_keyword(self, text: str, keyword: str) -> bool:
        """Check if text contains keyword (case-insensitive, partial match)"""
        # Simple containment check
        keyword_clean = keyword.lower().strip()
        return keyword_clean in text.lower()

"""
Job Scraper Service

Scrapes job posting URLs to extract job information including
title, description, requirements, and key skills.
"""

import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
import re
from urllib.parse import urlparse


class JobScraperService:
    """Service for scraping job postings from various platforms"""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def scrape_job_posting(self, url: str) -> Dict:
        """
        Scrape a job posting URL and extract relevant information

        Args:
            url: Job posting URL

        Returns:
            Dictionary containing job information
        """
        try:
            # Validate URL
            if not self._is_valid_url(url):
                raise ValueError("Invalid URL provided")

            # Fetch the page
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()

            # Parse HTML
            soup = BeautifulSoup(response.content, 'lxml')

            # Determine platform and use appropriate scraping strategy
            domain = urlparse(url).netloc.lower()

            if 'linkedin' in domain:
                job_data = self._scrape_linkedin(soup, url)
            elif 'indeed' in domain:
                job_data = self._scrape_indeed(soup, url)
            elif 'greenhouse' in domain:
                job_data = self._scrape_greenhouse(soup, url)
            else:
                # Generic scraping for unknown platforms
                job_data = self._scrape_generic(soup, url)

            # Extract keywords and requirements
            job_data['keywords'] = self._extract_keywords(job_data.get('description', ''))
            job_data['required_skills'] = self._extract_skills(job_data.get('description', ''))

            return job_data

        except requests.RequestException as e:
            raise Exception(f"Failed to fetch job posting: {str(e)}")
        except Exception as e:
            raise Exception(f"Error scraping job posting: {str(e)}")

    def _is_valid_url(self, url: str) -> bool:
        """Validate URL format"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False

    def _scrape_linkedin(self, soup: BeautifulSoup, url: str) -> Dict:
        """Scrape LinkedIn job posting"""
        job_data = {
            'source': 'LinkedIn',
            'url': url
        }

        # Extract job title
        title_elem = soup.find('h1', class_=re.compile(r'top-card-layout__title|topcard__title'))
        if title_elem:
            job_data['title'] = title_elem.get_text(strip=True)

        # Extract company name
        company_elem = soup.find('a', class_=re.compile(r'topcard__org-name-link|top-card-layout__company-info'))
        if company_elem:
            job_data['company'] = company_elem.get_text(strip=True)

        # Extract description
        desc_elem = soup.find('div', class_=re.compile(r'description__text|show-more-less-html__markup'))
        if desc_elem:
            job_data['description'] = desc_elem.get_text(separator='\n', strip=True)

        return job_data

    def _scrape_indeed(self, soup: BeautifulSoup, url: str) -> Dict:
        """Scrape Indeed job posting"""
        job_data = {
            'source': 'Indeed',
            'url': url
        }

        # Extract job title
        title_elem = soup.find('h1', class_=re.compile(r'jobsearch-JobInfoHeader-title'))
        if title_elem:
            job_data['title'] = title_elem.get_text(strip=True)

        # Extract company name
        company_elem = soup.find('div', class_=re.compile(r'jobsearch-InlineCompanyRating'))
        if company_elem:
            job_data['company'] = company_elem.get_text(strip=True).split('\n')[0]

        # Extract description
        desc_elem = soup.find('div', id='jobDescriptionText')
        if desc_elem:
            job_data['description'] = desc_elem.get_text(separator='\n', strip=True)

        return job_data

    def _scrape_greenhouse(self, soup: BeautifulSoup, url: str) -> Dict:
        """Scrape Greenhouse job posting"""
        job_data = {
            'source': 'Greenhouse',
            'url': url
        }

        # Extract job title
        title_elem = soup.find('h1', class_='app-title')
        if title_elem:
            job_data['title'] = title_elem.get_text(strip=True)

        # Extract company name
        company_elem = soup.find('span', class_='company-name')
        if company_elem:
            job_data['company'] = company_elem.get_text(strip=True)

        # Extract description
        desc_elem = soup.find('div', id='content')
        if desc_elem:
            job_data['description'] = desc_elem.get_text(separator='\n', strip=True)

        return job_data

    def _scrape_generic(self, soup: BeautifulSoup, url: str) -> Dict:
        """Generic scraping for unknown platforms"""
        job_data = {
            'source': 'Generic',
            'url': url
        }

        # Try to find job title (usually in h1)
        h1_elem = soup.find('h1')
        if h1_elem:
            job_data['title'] = h1_elem.get_text(strip=True)

        # Try to extract all text content
        # Remove script and style elements
        for script in soup(['script', 'style', 'nav', 'header', 'footer']):
            script.decompose()

        # Get text
        text = soup.get_text(separator='\n', strip=True)

        # Clean up text (remove excessive whitespace)
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        job_data['description'] = '\n'.join(lines)

        return job_data

    def _extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords from job description"""
        if not text:
            return []

        # Common job-related keywords to look for
        keyword_patterns = [
            r'\b(?:required|must have|should have|prefer(?:red)?|experience with|knowledge of)\b',
            r'\b(?:bachelor|master|phd|degree|certification)\b',
            r'\b(?:years?)\s+(?:of\s+)?(?:experience|exp)\b',
        ]

        keywords = []
        text_lower = text.lower()

        # Find sentences containing keyword patterns
        sentences = text.split('.')
        for sentence in sentences:
            for pattern in keyword_patterns:
                if re.search(pattern, sentence, re.IGNORECASE):
                    keywords.append(sentence.strip())
                    break

        return keywords[:10]  # Return top 10 keyword sentences

    def _extract_skills(self, text: str) -> List[str]:
        """Extract technical skills and requirements from job description"""
        if not text:
            return []

        # Common technical skills and tools
        common_skills = [
            # Programming Languages
            'python', 'java', 'javascript', 'typescript', 'c\\+\\+', 'c#', 'ruby', 'go', 'rust',
            'php', 'swift', 'kotlin', 'scala', 'r', 'matlab',

            # Web Technologies
            'react', 'angular', 'vue', 'node\\.?js', 'express', 'django', 'flask', 'spring',
            'html', 'css', 'sass', 'tailwind', 'bootstrap',

            # Databases
            'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'dynamodb',
            'oracle', 'cassandra',

            # Cloud & DevOps
            'aws', 'azure', 'gcp', 'google cloud', 'docker', 'kubernetes', 'jenkins', 'ci/cd',
            'terraform', 'ansible', 'git', 'github', 'gitlab',

            # Data & AI
            'machine learning', 'deep learning', 'nlp', 'computer vision', 'tensorflow',
            'pytorch', 'scikit-learn', 'pandas', 'numpy', 'spark', 'hadoop',

            # Other Tools
            'jira', 'agile', 'scrum', 'rest api', 'graphql', 'microservices', 'linux',
            'unix', 'bash', 'powershell'
        ]

        found_skills = []
        text_lower = text.lower()

        for skill in common_skills:
            pattern = r'\b' + skill + r'\b'
            if re.search(pattern, text_lower, re.IGNORECASE):
                # Extract the actual matched text to preserve casing
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    found_skills.append(match.group())

        # Remove duplicates while preserving order
        seen = set()
        unique_skills = []
        for skill in found_skills:
            skill_lower = skill.lower()
            if skill_lower not in seen:
                seen.add(skill_lower)
                unique_skills.append(skill)

        return unique_skills

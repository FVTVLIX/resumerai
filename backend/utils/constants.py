"""
Constants
Application-wide constants and configuration values.
"""

# Skill Categories
SKILL_CATEGORIES = {
    'programming_languages': {
        'display_name': 'Programming Languages',
        'keywords': [
            'Python', 'JavaScript', 'Java', 'C++', 'C#', 'TypeScript', 'Go', 'Rust',
            'Ruby', 'PHP', 'Swift', 'Kotlin', 'Scala', 'R', 'MATLAB', 'Perl',
            'Objective-C', 'Dart', 'Elixir', 'Haskell', 'Lua', 'Shell', 'Bash'
        ]
    },
    'frameworks': {
        'display_name': 'Frameworks & Libraries',
        'keywords': [
            'React', 'Angular', 'Vue', 'Django', 'Flask', 'FastAPI', 'Express',
            'Spring', 'Spring Boot', 'Rails', 'Laravel', 'ASP.NET', '.NET', 'jQuery',
            'Bootstrap', 'Tailwind', 'Next.js', 'Nuxt', 'Svelte', 'Ember',
            'TensorFlow', 'PyTorch', 'Keras', 'Scikit-learn', 'Pandas', 'NumPy'
        ]
    },
    'databases': {
        'display_name': 'Databases',
        'keywords': [
            'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'SQLite', 'Oracle',
            'SQL Server', 'MariaDB', 'Cassandra', 'DynamoDB', 'Elasticsearch',
            'Neo4j', 'CouchDB', 'Firebase', 'Firestore', 'InfluxDB'
        ]
    },
    'tools': {
        'display_name': 'Tools & Technologies',
        'keywords': [
            'Git', 'GitHub', 'GitLab', 'Bitbucket', 'Docker', 'Kubernetes',
            'Jenkins', 'CircleCI', 'Travis CI', 'Webpack', 'Babel', 'npm', 'yarn',
            'Gradle', 'Maven', 'Ansible', 'Terraform', 'Vagrant', 'Nginx',
            'Apache', 'VS Code', 'IntelliJ', 'Postman', 'Jira', 'Confluence'
        ]
    },
    'cloud': {
        'display_name': 'Cloud Platforms',
        'keywords': [
            'AWS', 'Azure', 'Google Cloud', 'GCP', 'Heroku', 'DigitalOcean',
            'Vercel', 'Netlify', 'CloudFlare', 'EC2', 'S3', 'Lambda',
            'Cloud Functions', 'Cloud Run', 'ECS', 'EKS', 'RDS', 'Route53'
        ]
    },
    'soft_skills': {
        'display_name': 'Soft Skills',
        'keywords': [
            'Leadership', 'Communication', 'Teamwork', 'Problem Solving',
            'Critical Thinking', 'Time Management', 'Adaptability', 'Creativity',
            'Collaboration', 'Presentation', 'Mentoring', 'Project Management',
            'Agile', 'Scrum', 'Analytical', 'Strategic Planning'
        ]
    },
    'methodologies': {
        'display_name': 'Methodologies',
        'keywords': [
            'Agile', 'Scrum', 'Kanban', 'DevOps', 'CI/CD', 'TDD', 'BDD',
            'Microservices', 'REST', 'GraphQL', 'SOAP', 'MVC', 'MVVM',
            'Serverless', 'Event-Driven', 'Domain-Driven Design'
        ]
    }
}

# Action Verbs (for resume analysis)
ACTION_VERBS = [
    # Leadership
    'led', 'directed', 'managed', 'supervised', 'coordinated', 'spearheaded',
    'orchestrated', 'mentored', 'guided', 'facilitated',
    # Achievement
    'achieved', 'accomplished', 'delivered', 'exceeded', 'surpassed', 'attained',
    'earned', 'won', 'completed', 'executed',
    # Improvement
    'improved', 'enhanced', 'optimized', 'streamlined', 'upgraded', 'modernized',
    'transformed', 'revitalized', 'refined', 'strengthened',
    # Creation
    'created', 'developed', 'designed', 'built', 'established', 'founded',
    'launched', 'initiated', 'introduced', 'pioneered',
    # Analysis
    'analyzed', 'evaluated', 'assessed', 'identified', 'researched', 'investigated',
    'diagnosed', 'examined', 'measured', 'reviewed',
    # Communication
    'presented', 'communicated', 'authored', 'published', 'reported', 'documented',
    'articulated', 'conveyed', 'negotiated', 'collaborated',
    # Technical
    'implemented', 'deployed', 'configured', 'automated', 'integrated', 'architected',
    'engineered', 'programmed', 'debugged', 'troubleshot',
    # Growth
    'grew', 'increased', 'expanded', 'scaled', 'accelerated', 'boosted',
    'maximized', 'elevated', 'multiplied', 'doubled',
    # Reduction
    'reduced', 'decreased', 'minimized', 'eliminated', 'cut', 'saved',
    'consolidated', 'simplified', 'lowered'
]

# Weak verbs to avoid
WEAK_VERBS = [
    'responsible for', 'worked on', 'helped with', 'assisted with',
    'participated in', 'involved in', 'contributed to', 'handled',
    'dealt with', 'did', 'made', 'got'
]

# Common job titles
JOB_TITLES = [
    # Software Engineering
    'Software Engineer', 'Senior Software Engineer', 'Staff Software Engineer',
    'Principal Engineer', 'Engineering Manager', 'Technical Lead', 'Tech Lead',
    'Full Stack Developer', 'Frontend Developer', 'Backend Developer',
    'Mobile Developer', 'iOS Developer', 'Android Developer',
    # Data & AI
    'Data Scientist', 'Data Analyst', 'Data Engineer', 'Machine Learning Engineer',
    'AI Engineer', 'Research Scientist', 'Analytics Manager',
    # DevOps & Infrastructure
    'DevOps Engineer', 'Site Reliability Engineer', 'SRE', 'Cloud Engineer',
    'Infrastructure Engineer', 'Platform Engineer', 'Systems Engineer',
    # Product & Design
    'Product Manager', 'Senior Product Manager', 'Product Owner',
    'UX Designer', 'UI Designer', 'Product Designer', 'UX Researcher',
    # Leadership
    'CTO', 'VP Engineering', 'Director of Engineering', 'Engineering Director',
    'Technical Director', 'Chief Architect', 'Solutions Architect'
]

# Education degrees
DEGREE_TYPES = [
    "Associate's", 'Associate', 'AS', 'AA', 'AAS',
    "Bachelor's", 'Bachelor', 'BS', 'BA', 'BSc', 'BEng', 'BFA',
    "Master's", 'Master', 'MS', 'MA', 'MSc', 'MEng', 'MBA', 'MFA',
    'PhD', 'Ph.D.', 'Doctorate', 'Doctoral',
    'Certificate', 'Certification', 'Diploma'
]

# Common education fields
EDUCATION_FIELDS = [
    'Computer Science', 'Software Engineering', 'Information Technology',
    'Data Science', 'Artificial Intelligence', 'Machine Learning',
    'Electrical Engineering', 'Mechanical Engineering', 'Civil Engineering',
    'Business Administration', 'Marketing', 'Finance', 'Accounting',
    'Psychology', 'Mathematics', 'Statistics', 'Physics', 'Chemistry',
    'Biology', 'Communications', 'Graphic Design', 'Web Development'
]

# ATS Keywords (commonly sought by Applicant Tracking Systems)
ATS_KEYWORDS = [
    'experience', 'leadership', 'management', 'development', 'analysis',
    'project', 'team', 'technical', 'business', 'communication',
    'problem solving', 'strategic', 'innovation', 'collaboration',
    'results-driven', 'detail-oriented', 'self-motivated'
]

# Date patterns (regex)
DATE_PATTERNS = {
    'full': r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{4}\b',
    'month_year': r'\b\d{1,2}/\d{4}\b',
    'year_only': r'\b(19|20)\d{2}\b',
    'present': r'\b(present|current|now)\b'
}

# Score thresholds
SCORE_THRESHOLDS = {
    'excellent': 90,
    'good': 75,
    'fair': 60,
    'needs_work': 0
}

# Score labels
SCORE_LABELS = {
    90: 'Excellent',
    75: 'Good',
    60: 'Fair',
    0: 'Needs Work'
}

# Suggestion priorities
PRIORITY_LEVELS = ['high', 'medium', 'low']

# Suggestion categories
SUGGESTION_CATEGORIES = ['content', 'formatting', 'ats', 'skills', 'experience']

# Minimum requirements for a good resume
MIN_REQUIREMENTS = {
    'skills': 5,
    'experience_years': 0,
    'bullet_points': 3,
    'words': 200
}

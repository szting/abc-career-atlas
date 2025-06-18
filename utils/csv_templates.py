"""
CSV Template Generator for Career Atlas
Generates sample CSV templates for data upload
"""

import pandas as pd
from typing import Optional

class CSVTemplateGenerator:
    """Generates CSV templates with sample data"""
    
    def generate_template(self, file_type: str) -> Optional[pd.DataFrame]:
        """Generate a template DataFrame for the specified file type"""
        
        templates = {
            "Job Role Description": self._job_roles_template,
            "Job Role-Critical Work Function-Key Tasks": self._job_tasks_template,
            "Job Role-Skills": self._job_skills_template,
            "TSC_CCS_Key (Skills Master)": self._skills_master_template,
            "TSC_CCS_K&A (Knowledge & Abilities)": self._skills_ka_template
        }
        
        template_func = templates.get(file_type)
        if template_func:
            return template_func()
        return None
    
    def _job_roles_template(self) -> pd.DataFrame:
        """Generate Job Role Description template"""
        data = {
            "Sector": [
                "Technology", 
                "Technology", 
                "Healthcare", 
                "Finance"
            ],
            "Track": [
                "Software Development", 
                "Data Science", 
                "Clinical Care", 
                "Investment Banking"
            ],
            "Job Role": [
                "Full Stack Developer", 
                "Data Scientist", 
                "Registered Nurse", 
                "Financial Analyst"
            ],
            "Job Role Description": [
                "Develops and maintains both front-end and back-end components of web applications using modern frameworks and technologies",
                "Analyzes complex data sets to extract insights and build predictive models using statistical methods and machine learning",
                "Provides direct patient care, administers medications, and coordinates with healthcare teams to ensure quality patient outcomes",
                "Analyzes financial data, creates reports, and provides investment recommendations to support business decision-making"
            ]
        }
        return pd.DataFrame(data)
    
    def _job_tasks_template(self) -> pd.DataFrame:
        """Generate Job Tasks template"""
        data = {
            "Sector": [
                "Technology", 
                "Technology", 
                "Technology",
                "Healthcare"
            ],
            "Track": [
                "Software Development", 
                "Software Development", 
                "Data Science",
                "Clinical Care"
            ],
            "Job Role": [
                "Full Stack Developer", 
                "Full Stack Developer", 
                "Data Scientist",
                "Registered Nurse"
            ],
            "Critical Work Function": [
                "Application Development", 
                "System Architecture", 
                "Data Analysis",
                "Patient Care"
            ],
            "Key Tasks": [
                "Write clean, maintainable code; Debug and troubleshoot applications; Implement new features based on requirements",
                "Design scalable system architectures; Create technical documentation; Review and optimize code performance",
                "Clean and preprocess data; Build and validate predictive models; Create data visualizations and reports",
                "Monitor patient vital signs; Administer prescribed medications; Document patient care activities"
            ]
        }
        return pd.DataFrame(data)
    
    def _job_skills_template(self) -> pd.DataFrame:
        """Generate Job Skills template"""
        data = {
            "Sector": [
                "Technology", 
                "Technology", 
                "Technology",
                "Technology",
                "Healthcare"
            ],
            "Track": [
                "Software Development", 
                "Software Development", 
                "Software Development",
                "Data Science",
                "Clinical Care"
            ],
            "Job Role": [
                "Full Stack Developer", 
                "Full Stack Developer", 
                "Full Stack Developer",
                "Data Scientist",
                "Registered Nurse"
            ],
            "TSC_CCS Title": [
                "JavaScript Programming", 
                "Database Management", 
                "Communication Skills",
                "Machine Learning",
                "Patient Assessment"
            ],
            "TSC_CCS Type": [
                "Technical Skills", 
                "Technical Skills", 
                "Core Competencies",
                "Technical Skills",
                "Technical Skills"
            ],
            "Proficiency Level": [
                "Advanced", 
                "Intermediate", 
                "3",
                "4",
                "Expert"
            ]
        }
        return pd.DataFrame(data)
    
    def _skills_master_template(self) -> pd.DataFrame:
        """Generate Skills Master template"""
        data = {
            "TSC Code": [
                "TS001", 
                "TS002", 
                "TS003",
                "CC001",
                "CC002"
            ],
            "Sector": [
                "Technology", 
                "Technology", 
                "Healthcare",
                "Cross-Sector",
                "Cross-Sector"
            ],
            "TSC_CCS Category": [
                "Programming Languages", 
                "Data Management", 
                "Clinical Skills",
                "Communication",
                "Leadership"
            ],
            "TSC_CCS Title": [
                "JavaScript Programming", 
                "Database Management", 
                "Patient Assessment",
                "Communication Skills",
                "Team Leadership"
            ],
            "TSC_CCS Description": [
                "Proficiency in JavaScript programming including ES6+ features, async programming, and framework usage",
                "Ability to design, implement, and maintain relational and non-relational databases",
                "Skills in assessing patient conditions, vital signs, and determining appropriate care interventions",
                "Ability to communicate effectively in verbal and written forms with diverse stakeholders",
                "Capability to lead teams, delegate tasks, and motivate team members toward common goals"
            ],
            "TSC_CCS Type": [
                "Technical Skills", 
                "Technical Skills", 
                "Technical Skills",
                "Core Competencies",
                "Core Competencies"
            ]
        }
        return pd.DataFrame(data)
    
    def _skills_ka_template(self) -> pd.DataFrame:
        """Generate Skills K&A template"""
        data = {
            "Sector": [
                "Technology", 
                "Technology", 
                "Technology",
                "Cross-Sector",
                "Cross-Sector"
            ],
            "TSC_CCS Category": [
                "Programming Languages", 
                "Programming Languages", 
                "Data Management",
                "Communication",
                "Communication"
            ],
            "TSC_CCS Title": [
                "JavaScript Programming", 
                "JavaScript Programming", 
                "Database Management",
                "Communication Skills",
                "Communication Skills"
            ],
            "TSC_CCS Description": [
                "Proficiency in JavaScript programming", 
                "Proficiency in JavaScript programming", 
                "Database design and management",
                "Effective communication abilities",
                "Effective communication abilities"
            ],
            "Proficiency Level": [
                "Advanced", 
                "Advanced", 
                "Intermediate",
                "3",
                "3"
            ],
            "Proficiency Description": [
                "Can independently develop complex applications and mentor others",
                "Can independently develop complex applications and mentor others",
                "Can design and optimize database schemas with guidance",
                "Communicates clearly and adapts style to audience",
                "Communicates clearly and adapts style to audience"
            ],
            "Knowledge-Ability Classification": [
                "Knowledge", 
                "Ability", 
                "Knowledge",
                "Knowledge",
                "Ability"
            ],
            "Knowledge-Ability Items": [
                "ES6+ syntax; Async/await patterns; Popular frameworks (React, Vue, Angular)",
                "Debug complex issues; Write efficient algorithms; Implement design patterns",
                "SQL syntax; Normalization principles; Index optimization; Query performance tuning",
                "Communication theories; Active listening techniques; Presentation best practices",
                "Adapt communication style; Handle difficult conversations; Facilitate meetings"
            ]
        }
        return pd.DataFrame(data)

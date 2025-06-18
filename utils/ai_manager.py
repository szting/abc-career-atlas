import os
import json
from typing import Dict, List, Optional, Any
import streamlit as st
from dotenv import load_dotenv
import openai
import anthropic
import google.generativeai as genai

load_dotenv()

class AIManager:
    def __init__(self):
        """Initialize AI Manager with API keys"""
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        self.google_api_key = os.getenv('GOOGLE_API_KEY')
        
        # Initialize clients
        if self.openai_api_key and self.openai_api_key != 'your_openai_api_key_here':
            openai.api_key = self.openai_api_key
            self.openai_available = True
        else:
            self.openai_available = False
        
        if self.anthropic_api_key and self.anthropic_api_key != 'your_anthropic_api_key_here':
            self.anthropic_client = anthropic.Anthropic(api_key=self.anthropic_api_key)
            self.anthropic_available = True
        else:
            self.anthropic_available = False
        
        if self.google_api_key and self.google_api_key != 'your_google_api_key_here':
            genai.configure(api_key=self.google_api_key)
            self.google_available = True
        else:
            self.google_available = False
    
    def get_available_providers(self) -> List[str]:
        """Get list of available AI providers"""
        providers = []
        if self.openai_available:
            providers.append("OpenAI")
        if self.anthropic_available:
            providers.append("Anthropic")
        if self.google_available:
            providers.append("Google")
        return providers
    
    def generate_career_recommendations(self, 
                                      riasec_scores: Dict[str, float], 
                                      additional_info: Dict[str, Any],
                                      num_recommendations: int = 5) -> List[Dict[str, Any]]:
        """Generate AI-powered career recommendations based on RIASEC scores"""
        
        # Create the prompt
        prompt = self._create_career_prompt(riasec_scores, additional_info, num_recommendations)
        
        # Try providers in order of preference
        try:
            if self.openai_available:
                return self._get_openai_recommendations(prompt)
            elif self.anthropic_available:
                return self._get_anthropic_recommendations(prompt)
            elif self.google_available:
                return self._get_google_recommendations(prompt)
            else:
                return self._get_fallback_recommendations(riasec_scores)
        except Exception as e:
            st.error(f"Error generating recommendations: {str(e)}")
            return self._get_fallback_recommendations(riasec_scores)
    
    def generate_development_plan(self,
                                riasec_scores: Dict[str, float],
                                selected_careers: List[str],
                                additional_info: Dict[str, Any]) -> Dict[str, Any]:
        """Generate personalized development plan"""
        
        prompt = self._create_development_prompt(riasec_scores, selected_careers, additional_info)
        
        try:
            if self.openai_available:
                return self._get_openai_development_plan(prompt)
            elif self.anthropic_available:
                return self._get_anthropic_development_plan(prompt)
            elif self.google_available:
                return self._get_google_development_plan(prompt)
            else:
                return self._get_fallback_development_plan(selected_careers)
        except Exception as e:
            st.error(f"Error generating development plan: {str(e)}")
            return self._get_fallback_development_plan(selected_careers)
    
    def generate_interview_questions(self, career_title: str, level: str = "entry") -> List[Dict[str, str]]:
        """Generate interview preparation questions"""
        
        prompt = self._create_interview_prompt(career_title, level)
        
        try:
            if self.openai_available:
                return self._get_openai_interview_questions(prompt)
            elif self.anthropic_available:
                return self._get_anthropic_interview_questions(prompt)
            elif self.google_available:
                return self._get_google_interview_questions(prompt)
            else:
                return self._get_fallback_interview_questions(career_title)
        except Exception as e:
            st.error(f"Error generating interview questions: {str(e)}")
            return self._get_fallback_interview_questions(career_title)
    
    def analyze_skills_gap(self,
                          current_skills: List[str],
                          target_career: str,
                          riasec_scores: Dict[str, float]) -> Dict[str, Any]:
        """Analyze skills gap for target career"""
        
        prompt = self._create_skills_gap_prompt(current_skills, target_career, riasec_scores)
        
        try:
            if self.openai_available:
                return self._get_openai_skills_analysis(prompt)
            elif self.anthropic_available:
                return self._get_anthropic_skills_analysis(prompt)
            elif self.google_available:
                return self._get_google_skills_analysis(prompt)
            else:
                return self._get_fallback_skills_analysis(target_career)
        except Exception as e:
            st.error(f"Error analyzing skills gap: {str(e)}")
            return self._get_fallback_skills_analysis(target_career)
    
    def _create_career_prompt(self, riasec_scores: Dict[str, float], 
                            additional_info: Dict[str, Any], 
                            num_recommendations: int) -> str:
        """Create prompt for career recommendations"""
        
        sorted_scores = sorted(riasec_scores.items(), key=lambda x: x[1], reverse=True)
        top_types = sorted_scores[:3]
        
        prompt = f"""As a career counselor, analyze these RIASEC assessment results and provide {num_recommendations} specific career recommendations.

RIASEC Scores:
{json.dumps(riasec_scores, indent=2)}

Top 3 Types: {', '.join([f"{t[0]} ({t[1]:.1f})" for t in top_types])}

Additional Information:
- Education Level: {additional_info.get('education', 'Not specified')}
- Years of Experience: {additional_info.get('experience', 0)}
- Interests: {additional_info.get('interests', 'Not specified')}
- Career Goals: {additional_info.get('goals', 'Not specified')}
- Preferred Work Environment: {additional_info.get('work_environment', 'Not specified')}
- Salary Expectations: {additional_info.get('salary_expectations', 'Not specified')}

For each career recommendation, provide:
1. Job title
2. Brief description (2-3 sentences)
3. Why it matches their RIASEC profile
4. Required skills (top 5)
5. Typical education requirements
6. Salary range (entry to senior level)
7. Growth outlook (next 5-10 years)
8. Day-to-day responsibilities

Return the response as a JSON array with the following structure:
[
  {{
    "title": "Job Title",
    "description": "Brief description",
    "match_reason": "Why it matches their profile",
    "required_skills": ["skill1", "skill2", ...],
    "education": "Typical education requirements",
    "salary_range": "Entry to senior level range",
    "growth_outlook": "Growth prospects",
    "daily_tasks": ["task1", "task2", ...]
  }}
]"""
        
        return prompt
    
    def _create_development_prompt(self, riasec_scores: Dict[str, float],
                                 selected_careers: List[str],
                                 additional_info: Dict[str, Any]) -> str:
        """Create prompt for development plan"""
        
        careers_text = ", ".join(selected_careers[:3])
        
        prompt = f"""Create a comprehensive career development plan for someone interested in: {careers_text}

Current Profile:
- Education: {additional_info.get('education', 'Not specified')}
- Experience: {additional_info.get('experience', 0)} years
- Current Skills: {additional_info.get('current_skills', 'Not specified')}
- RIASEC Profile: {', '.join([f"{k}: {v:.1f}" for k, v in sorted(riasec_scores.items(), key=lambda x: x[1], reverse=True)[:3]])}

Create a development plan with:
1. Short-term goals (3-6 months) - 5 specific, actionable goals
2. Medium-term goals (6-12 months) - 5 goals building on short-term
3. Long-term goals (1-3 years) - 5 strategic goals
4. Skills to develop - categorized by priority (high/medium/low)
5. Recommended courses/certifications - at least 10 specific recommendations
6. Networking strategies - 5 specific actions
7. Portfolio projects - 5 project ideas to demonstrate skills
8. Milestones and checkpoints - quarterly milestones for tracking progress

Return as JSON with this structure:
{{
  "short_term_goals": ["goal1", "goal2", ...],
  "medium_term_goals": ["goal1", "goal2", ...],
  "long_term_goals": ["goal1", "goal2", ...],
  "skills_to_develop": {{
    "high_priority": ["skill1", "skill2", ...],
    "medium_priority": ["skill1", "skill2", ...],
    "low_priority": ["skill1", "skill2", ...]
  }},
  "recommended_courses": [
    {{"title": "Course Name", "provider": "Platform", "duration": "X weeks", "cost": "Free/$X"}}
  ],
  "networking_strategies": ["strategy1", "strategy2", ...],
  "portfolio_projects": [
    {{"title": "Project Name", "description": "Brief description", "skills_demonstrated": ["skill1", "skill2"]}}
  ],
  "milestones": {{
    "3_months": ["milestone1", "milestone2"],
    "6_months": ["milestone1", "milestone2"],
    "12_months": ["milestone1", "milestone2"],
    "24_months": ["milestone1", "milestone2"]
  }}
}}"""
        
        return prompt
    
    def _create_interview_prompt(self, career_title: str, level: str) -> str:
        """Create prompt for interview questions"""
        
        prompt = f"""Generate 10 interview preparation questions for a {level}-level {career_title} position.

Include a mix of:
- Technical/skill-based questions (4)
- Behavioral questions (3)
- Situational questions (2)
- Career motivation question (1)

For each question, provide:
1. The question
2. Why it's asked (interviewer's perspective)
3. Key points to cover in the answer
4. Example answer structure

Return as JSON array:
[
  {{
    "question": "The interview question",
    "type": "technical|behavioral|situational|motivation",
    "why_asked": "Interviewer's intent",
    "key_points": ["point1", "point2", ...],
    "answer_structure": "How to structure the response"
  }}
]"""
        
        return prompt
    
    def _create_skills_gap_prompt(self, current_skills: List[str], 
                                target_career: str,
                                riasec_scores: Dict[str, float]) -> str:
        """Create prompt for skills gap analysis"""
        
        prompt = f"""Analyze the skills gap for transitioning to a {target_career} role.

Current Skills: {', '.join(current_skills)}
RIASEC Profile: {', '.join([f"{k}: {v:.1f}" for k, v in sorted(riasec_scores.items(), key=lambda x: x[1], reverse=True)[:3]])}

Provide:
1. Required skills for {target_career} (categorized by importance)
2. Skills gap analysis (what's missing)
3. Transferable skills from current skillset
4. Learning priorities (ordered list)
5. Time estimates for acquiring each skill
6. Recommended learning resources

Return as JSON:
{{
  "required_skills": {{
    "essential": ["skill1", "skill2", ...],
    "important": ["skill1", "skill2", ...],
    "nice_to_have": ["skill1", "skill2", ...]
  }},
  "skills_gap": ["missing_skill1", "missing_skill2", ...],
  "transferable_skills": ["skill1", "skill2", ...],
  "learning_priorities": [
    {{"skill": "Skill name", "priority": 1, "estimated_time": "X months", "difficulty": "easy|medium|hard"}}
  ],
  "learning_resources": [
    {{"skill": "Skill name", "resources": ["resource1", "resource2", ...]}}
  ]
}}"""
        
        return prompt
    
    # OpenAI implementations
    def _get_openai_recommendations(self, prompt: str) -> List[Dict[str, Any]]:
        """Get recommendations using OpenAI"""
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert career counselor specializing in RIASEC assessments and career guidance."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        content = response.choices[0].message.content
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            # Fallback parsing
            return self._parse_text_response(content)
    
    def _get_openai_development_plan(self, prompt: str) -> Dict[str, Any]:
        """Get development plan using OpenAI"""
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a career development expert creating actionable development plans."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        content = response.choices[0].message.content
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return self._get_fallback_development_plan([])
    
    def _get_openai_interview_questions(self, prompt: str) -> List[Dict[str, str]]:
        """Get interview questions using OpenAI"""
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert interviewer and career coach."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1500
        )
        
        content = response.choices[0].message.content
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return self._get_fallback_interview_questions("")
    
    def _get_openai_skills_analysis(self, prompt: str) -> Dict[str, Any]:
        """Get skills analysis using OpenAI"""
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a skills assessment and career transition expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1500
        )
        
        content = response.choices[0].message.content
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return self._get_fallback_skills_analysis("")
    
    # Anthropic implementations
    def _get_anthropic_recommendations(self, prompt: str) -> List[Dict[str, Any]]:
        """Get recommendations using Anthropic"""
        response = self.anthropic_client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=2000,
            temperature=0.7,
            system="You are an expert career counselor specializing in RIASEC assessments.",
            messages=[{"role": "user", "content": prompt}]
        )
        
        content = response.content[0].text
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return self._parse_text_response(content)
    
    def _get_anthropic_development_plan(self, prompt: str) -> Dict[str, Any]:
        """Get development plan using Anthropic"""
        response = self.anthropic_client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=2000,
            temperature=0.7,
            system="You are a career development expert.",
            messages=[{"role": "user", "content": prompt}]
        )
        
        content = response.content[0].text
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return self._get_fallback_development_plan([])
    
    def _get_anthropic_interview_questions(self, prompt: str) -> List[Dict[str, str]]:
        """Get interview questions using Anthropic"""
        response = self.anthropic_client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1500,
            temperature=0.7,
            system="You are an expert interviewer and career coach.",
            messages=[{"role": "user", "content": prompt}]
        )
        
        content = response.content[0].text
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return self._get_fallback_interview_questions("")
    
    def _get_anthropic_skills_analysis(self, prompt: str) -> Dict[str, Any]:
        """Get skills analysis using Anthropic"""
        response = self.anthropic_client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1500,
            temperature=0.7,
            system="You are a skills assessment expert.",
            messages=[{"role": "user", "content": prompt}]
        )
        
        content = response.content[0].text
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return self._get_fallback_skills_analysis("")
    
    # Google implementations
    def _get_google_recommendations(self, prompt: str) -> List[Dict[str, Any]]:
        """Get recommendations using Google Gemini"""
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        
        try:
            return json.loads(response.text)
        except json.JSONDecodeError:
            return self._parse_text_response(response.text)
    
    def _get_google_development_plan(self, prompt: str) -> Dict[str, Any]:
        """Get development plan using Google Gemini"""
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        
        try:
            return json.loads(response.text)
        except json.JSONDecodeError:
            return self._get_fallback_development_plan([])
    
    def _get_google_interview_questions(self, prompt: str) -> List[Dict[str, str]]:
        """Get interview questions using Google Gemini"""
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        
        try:
            return json.loads(response.text)
        except json.JSONDecodeError:
            return self._get_fallback_interview_questions("")
    
    def _get_google_skills_analysis(self, prompt: str) -> Dict[str, Any]:
        """Get skills analysis using Google Gemini"""
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        
        try:
            return json.loads(response.text)
        except json.JSONDecodeError:
            return self._get_fallback_skills_analysis("")
    
    # Fallback implementations
    def _get_fallback_recommendations(self, riasec_scores: Dict[str, float]) -> List[Dict[str, Any]]:
        """Provide fallback recommendations when AI is not available"""
        sorted_scores = sorted(riasec_scores.items(), key=lambda x: x[1], reverse=True)
        top_type = sorted_scores[0][0] if sorted_scores else "Investigative"
        
        # Basic recommendations based on top RIASEC type
        recommendations_db = {
            "Realistic": [
                {
                    "title": "Software Engineer",
                    "description": "Design and develop software applications and systems.",
                    "match_reason": "Combines practical problem-solving with technical skills.",
                    "required_skills": ["Programming", "Problem-solving", "System design", "Debugging", "Version control"],
                    "education": "Bachelor's in Computer Science or related field",
                    "salary_range": "$70,000 - $150,000+",
                    "growth_outlook": "Excellent - 22% growth expected",
                    "daily_tasks": ["Write code", "Debug applications", "Collaborate with team", "Design solutions"]
                }
            ],
            "Investigative": [
                {
                    "title": "Data Scientist",
                    "description": "Analyze complex data to help organizations make better decisions.",
                    "match_reason": "Perfect for analytical minds who enjoy solving complex problems.",
                    "required_skills": ["Statistics", "Machine Learning", "Python/R", "Data visualization", "SQL"],
                    "education": "Bachelor's/Master's in Data Science, Statistics, or related",
                    "salary_range": "$80,000 - $160,000+",
                    "growth_outlook": "Excellent - 35% growth expected",
                    "daily_tasks": ["Analyze datasets", "Build models", "Create visualizations", "Present findings"]
                }
            ],
            "Artistic": [
                {
                    "title": "UX/UI Designer",
                    "description": "Create intuitive and visually appealing user interfaces.",
                    "match_reason": "Combines creativity with problem-solving and user empathy.",
                    "required_skills": ["Design software", "User research", "Prototyping", "Visual design", "Interaction design"],
                    "education": "Bachelor's in Design, HCI, or related field",
                    "salary_range": "$60,000 - $130,000+",
                    "growth_outlook": "Good - 13% growth expected",
                    "daily_tasks": ["Create mockups", "Conduct user research", "Collaborate with developers", "Iterate designs"]
                }
            ],
            "Social": [
                {
                    "title": "Human Resources Manager",
                    "description": "Manage organizational culture and employee development.",
                    "match_reason": "Ideal for those who enjoy helping others and building relationships.",
                    "required_skills": ["Communication", "Conflict resolution", "Leadership", "Employment law", "Strategic planning"],
                    "education": "Bachelor's in HR, Business, or Psychology",
                    "salary_range": "$65,000 - $120,000+",
                    "growth_outlook": "Good - 9% growth expected",
                    "daily_tasks": ["Recruit talent", "Resolve conflicts", "Develop policies", "Train employees"]
                }
            ],
            "Enterprising": [
                {
                    "title": "Product Manager",
                    "description": "Lead product development from conception to launch.",
                    "match_reason": "Perfect for natural leaders who enjoy driving initiatives.",
                    "required_skills": ["Leadership", "Strategic thinking", "Communication", "Analytics", "Project management"],
                    "education": "Bachelor's in Business, Engineering, or related",
                    "salary_range": "$85,000 - $170,000+",
                    "growth_outlook": "Excellent - 19% growth expected",
                    "daily_tasks": ["Define product vision", "Coordinate teams", "Analyze metrics", "Stakeholder management"]
                }
            ],
            "Conventional": [
                {
                    "title": "Financial Analyst",
                    "description": "Analyze financial data to guide business decisions.",
                    "match_reason": "Suits those who enjoy structured work with numbers and data.",
                    "required_skills": ["Financial modeling", "Excel", "Data analysis", "Reporting", "Attention to detail"],
                    "education": "Bachelor's in Finance, Accounting, or Economics",
                    "salary_range": "$60,000 - $110,000+",
                    "growth_outlook": "Good - 8% growth expected",
                    "daily_tasks": ["Analyze financial data", "Create reports", "Build models", "Present recommendations"]
                }
            ]
        }
        
        return recommendations_db.get(top_type, recommendations_db["Investigative"])
    
    def _get_fallback_development_plan(self, selected_careers: List[str]) -> Dict[str, Any]:
        """Provide fallback development plan"""
        return {
            "short_term_goals": [
                "Complete online certification in your field",
                "Build a portfolio with 3 projects",
                "Network with 10 professionals",
                "Update resume and LinkedIn",
                "Learn one new relevant tool/technology"
            ],
            "medium_term_goals": [
                "Gain practical experience through internship/freelance",
                "Develop expertise in a specialized area",
                "Build professional network of 50+ connections",
                "Contribute to open source or community projects",
                "Achieve one professional certification"
            ],
            "long_term_goals": [
                "Secure position in target role",
                "Become recognized expert in your niche",
                "Mentor others in your field",
                "Lead significant projects",
                "Achieve senior-level expertise"
            ],
            "skills_to_develop": {
                "high_priority": ["Technical skills for role", "Communication", "Problem-solving"],
                "medium_priority": ["Leadership", "Project management", "Industry knowledge"],
                "low_priority": ["Advanced specializations", "Cross-functional skills"]
            },
            "recommended_courses": [
                {"title": "Coursera Professional Certificates", "provider": "Coursera", "duration": "3-6 months", "cost": "$49/month"},
                {"title": "LinkedIn Learning Paths", "provider": "LinkedIn", "duration": "2-4 months", "cost": "$29/month"},
                {"title": "Udemy Specialized Courses", "provider": "Udemy", "duration": "Self-paced", "cost": "$50-200"},
                {"title": "edX MicroMasters", "provider": "edX", "duration": "6-12 months", "cost": "$800-1500"}
            ],
            "networking_strategies": [
                "Join professional associations in your field",
                "Attend industry conferences and webinars",
                "Engage on LinkedIn with thought leaders",
                "Participate in local meetups",
                "Find a mentor in your target field"
            ],
            "portfolio_projects": [
                {"title": "Industry Case Study", "description": "Analyze and solve a real industry problem", "skills_demonstrated": ["Analysis", "Problem-solving"]},
                {"title": "Personal Project", "description": "Build something that showcases your skills", "skills_demonstrated": ["Technical skills", "Creativity"]},
                {"title": "Collaborative Project", "description": "Work with others on a meaningful project", "skills_demonstrated": ["Teamwork", "Communication"]}
            ],
            "milestones": {
                "3_months": ["Complete first certification", "Build first portfolio project"],
                "6_months": ["Expand network to 25 connections", "Complete 3 portfolio projects"],
                "12_months": ["Apply for target positions", "Achieve key certification"],
                "24_months": ["Secure role in target field", "Establish industry presence"]
            }
        }
    
    def _get_fallback_interview_questions(self, career_title: str) -> List[Dict[str, str]]:
        """Provide fallback interview questions"""
        return [
            {
                "question": "Tell me about yourself and why you're interested in this role.",
                "type": "motivation",
                "why_asked": "To understand your background and motivation",
                "key_points": ["Relevant experience", "Career goals", "Interest in company"],
                "answer_structure": "Past experience → Current situation → Future goals aligned with role"
            },
            {
                "question": "Describe a challenging project you've worked on.",
                "type": "behavioral",
                "why_asked": "To assess problem-solving and resilience",
                "key_points": ["Challenge faced", "Actions taken", "Results achieved", "Lessons learned"],
                "answer_structure": "Use STAR method: Situation → Task → Action → Result"
            },
            {
                "question": "How do you stay updated with industry trends?",
                "type": "technical",
                "why_asked": "To gauge continuous learning commitment",
                "key_points": ["Learning resources", "Professional development", "Application of knowledge"],
                "answer_structure": "Specific resources → How you apply learning → Recent example"
            }
        ]
    
    def _get_fallback_skills_analysis(self, target_career: str) -> Dict[str, Any]:
        """Provide fallback skills analysis"""
        return {
            "required_skills": {
                "essential": ["Core technical skills", "Communication", "Problem-solving"],
                "important": ["Project management", "Collaboration", "Analytical thinking"],
                "nice_to_have": ["Leadership", "Public speaking", "Advanced specializations"]
            },
            "skills_gap": ["Industry-specific knowledge", "Technical certifications", "Practical experience"],
            "transferable_skills": ["Communication", "Time management", "Teamwork"],
            "learning_priorities": [
                {"skill": "Core Technical Skills", "priority": 1, "estimated_time": "3-6 months", "difficulty": "medium"},
                {"skill": "Industry Knowledge", "priority": 2, "estimated_time": "2-3 months", "difficulty": "easy"},
                {"skill": "Specialized Tools", "priority": 3, "estimated_time": "1-2 months", "difficulty": "medium"}
            ],
            "learning_resources": [
                {"skill": "Technical Skills", "resources": ["Online courses", "Documentation", "Tutorials", "Practice projects"]},
                {"skill": "Industry Knowledge", "resources": ["Industry publications", "Podcasts", "Conferences", "Networking"]}
            ]
        }
    
    def _parse_text_response(self, text: str) -> List[Dict[str, Any]]:
        """Parse text response when JSON parsing fails"""
        # Basic parsing to extract career recommendations
        careers = []
        lines = text.split('\n')
        current_career = {}
        
        for line in lines:
            line = line.strip()
            if line and any(keyword in line.lower() for keyword in ['title:', 'job:', 'career:', 'position:']):
                if current_career:
                    careers.append(current_career)
                current_career = {"title": line.split(':', 1)[-1].strip()}
            elif current_career and line:
                if 'description' not in current_career:
                    current_career['description'] = line
                else:
                    current_career['description'] += ' ' + line
        
        if current_career:
            careers.append(current_career)
        
        # Ensure we have required fields
        for career in careers:
            career.setdefault('match_reason', 'Matches your profile')
            career.setdefault('required_skills', ['Communication', 'Problem-solving', 'Technical skills'])
            career.setdefault('education', 'Bachelor\'s degree preferred')
            career.setdefault('salary_range', '$50,000 - $100,000')
            career.setdefault('growth_outlook', 'Positive growth expected')
            career.setdefault('daily_tasks', ['Varied responsibilities'])
        
        return careers[:5] if careers else self._get_fallback_recommendations({})

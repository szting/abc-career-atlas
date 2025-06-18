import os
import openai
import anthropic
import google.generativeai as genai
from dotenv import load_dotenv
import streamlit as st
import json

load_dotenv()

class LLMManager:
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        self.google_api_key = os.getenv('GOOGLE_API_KEY')
        
        # Initialize clients
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
        
        if self.anthropic_api_key:
            self.anthropic_client = anthropic.Anthropic(api_key=self.anthropic_api_key)
        
        if self.google_api_key:
            genai.configure(api_key=self.google_api_key)
    
    def generate_career_recommendations(self, scores, additional_info):
        """Generate career recommendations based on RIASEC scores"""
        # Create prompt
        prompt = self._create_career_prompt(scores, additional_info)
        
        # Try different LLMs in order of preference
        try:
            if self.openai_api_key:
                return self._get_openai_recommendations(prompt)
            elif self.anthropic_api_key:
                return self._get_anthropic_recommendations(prompt)
            elif self.google_api_key:
                return self._get_gemini_recommendations(prompt)
            else:
                return self._get_fallback_recommendations(scores)
        except Exception as e:
            st.error(f"Error generating recommendations: {str(e)}")
            return self._get_fallback_recommendations(scores)
    
    def generate_development_plan(self, scores, careers, additional_info):
        """Generate a personalized development plan"""
        prompt = self._create_development_prompt(scores, careers, additional_info)
        
        try:
            if self.openai_api_key:
                return self._get_openai_development_plan(prompt)
            elif self.anthropic_api_key:
                return self._get_anthropic_development_plan(prompt)
            elif self.google_api_key:
                return self._get_gemini_development_plan(prompt)
            else:
                return self._get_fallback_development_plan(careers)
        except Exception as e:
            st.error(f"Error generating development plan: {str(e)}")
            return self._get_fallback_development_plan(careers)
    
    def _create_career_prompt(self, scores, additional_info):
        """Create prompt for career recommendations"""
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top_types = sorted_scores[:3]
        
        prompt = f"""Based on the following RIASEC assessment results, provide 5 specific career recommendations:

RIASEC Scores:
{json.dumps(scores, indent=2)}

Top 3 Types: {', '.join([f"{t[0]} ({t[1]:.1f})" for t in top_types])}

Additional Information:
- Education: {additional_info.get('education', 'Not specified')}
- Experience: {additional_info.get('experience', 0)} years
- Interests: {additional_info.get('interests', 'Not specified')}
- Goals: {additional_info.get('goals', 'Not specified')}

For each career recommendation, provide:
1. Job title
2. Brief description (2-3 sentences)
3. Why it matches their profile
4. Required skills (top 5)
5. Match score (0-100)
6. Typical salary range
7. Growth outlook

Format the response as a JSON array of career objects."""
        
        return prompt
    
    def _create_development_prompt(self, scores, careers, additional_info):
        """Create prompt for development plan"""
        career_titles = [c.get('title', 'Unknown') for c in careers[:3]]
        
        prompt = f"""Create a personalized career development plan based on:

Target Careers: {', '.join(career_titles)}
Education: {additional_info.get('education', 'Not specified')}
Experience: {additional_info.get('experience', 0)} years

Provide a comprehensive plan including:
1. Short-term goals (next 6 months) - list of 5 specific goals
2. Skills to develop - list of skills with priority levels
3. Resources - courses, books, certifications (at least 5)
4. Action steps - specific tasks to complete (at least 7)

Format as JSON with keys: short_term_goals, skills_to_develop, resources, action_steps"""
        
        return prompt
    
    def _get_openai_recommendations(self, prompt):
        """Get recommendations using OpenAI"""
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a career counselor expert in RIASEC assessments."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1500
        )
        
        content = response.choices[0].message.content
        try:
            return json.loads(content)
        except:
            return self._parse_text_response(content)
    
    def _get_anthropic_recommendations(self, prompt):
        """Get recommendations using Anthropic"""
        response = self.anthropic_client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1500,
            temperature=0.7,
            system="You are a career counselor expert in RIASEC assessments.",
            messages=[{"role": "user", "content": prompt}]
        )
        
        content = response.content[0].text
        try:
            return json.loads(content)
        except:
            return self._parse_text_response(content)
    
    def _get_gemini_recommendations(self, prompt):
        """Get recommendations using Google Gemini"""
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        
        try:
            return json.loads(response.text)
        except:
            return self._parse_text_response(response.text)
    
    def _get_fallback_recommendations(self, scores):
        """Provide fallback recommendations based on RIASEC scores"""
        # Career database mapped to RIASEC types
        career_database = {
            "Realistic": [
                {"title": "Software Developer", "match_score": 85},
                {"title": "Mechanical Engineer", "match_score": 82},
                {"title": "Data Analyst", "match_score": 78}
            ],
            "Investigative": [
                {"title": "Research Scientist", "match_score": 88},
                {"title": "Data Scientist", "match_score": 85},
                {"title": "Medical Researcher", "match_score": 82}
            ],
            "Artistic": [
                {"title": "UX/UI Designer", "match_score": 87},
                {"title": "Content Creator", "match_score": 84},
                {"title": "Marketing Creative", "match_score": 80}
            ],
            "Social": [
                {"title": "Human Resources Manager", "match_score": 86},
                {"title": "Teacher/Educator", "match_score": 84},
                {"title": "Career Counselor", "match_score": 82}
            ],
            "Enterprising": [
                {"title": "Product Manager", "match_score": 88},
                {"title": "Business Analyst", "match_score": 85},
                {"title": "Sales Manager", "match_score": 82}
            ],
            "Conventional": [
                {"title": "Financial Analyst", "match_score": 86},
                {"title": "Project Coordinator", "match_score": 83},
                {"title": "Operations Manager", "match_score": 80}
            ]
        }
        
        # Get top 3 RIASEC types
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        recommendations = []
        
        for riasec_type, score in sorted_scores[:3]:
            if riasec_type in career_database:
                for career in career_database[riasec_type]:
                    career_copy = career.copy()
                    career_copy.update({
                        "description": f"A great career for {riasec_type} types",
                        "match_reason": f"Aligns with your {riasec_type} interests",
                        "skills": ["Communication", "Problem-solving", "Leadership", "Technical skills", "Creativity"],
                        "salary_range": "$50,000 - $120,000",
                        "growth_outlook": "Above average"
                    })
                    recommendations.append(career_copy)
        
        return recommendations[:5]
    
    def _get_fallback_development_plan(self, careers):
        """Provide fallback development plan"""
        return {
            "short_term_goals": [
                "Complete online certification in your field",
                "Network with 5 professionals in target careers",
                "Update resume and LinkedIn profile",
                "Apply to 10 relevant positions",
                "Develop one key technical skill"
            ],
            "skills_to_develop": [
                {"skill": "Communication", "priority": "High"},
                {"skill": "Leadership", "priority": "Medium"},
                {"skill": "Technical Skills", "priority": "High"},
                {"skill": "Project Management", "priority": "Medium"}
            ],
            "resources": [
                "Coursera - Professional Certificates",
                "LinkedIn Learning - Career Development",
                "Industry-specific conferences and webinars",
                "Professional association memberships",
                "Mentorship programs"
            ],
            "action_steps": [
                "Research target companies and roles",
                "Create a learning schedule",
                "Join professional communities",
                "Practice interview skills",
                "Build a portfolio project",
                "Seek feedback from mentors",
                "Track progress weekly"
            ]
        }
    
    def _parse_text_response(self, text):
        """Parse text response into structured format"""
        # Basic parsing logic - in production, this would be more sophisticated
        careers = []
        lines = text.split('\n')
        current_career = {}
        
        for line in lines:
            if line.strip():
                if "title" in line.lower() or "job" in line.lower():
                    if current_career:
                        careers.append(current_career)
                    current_career = {"title": line.strip()}
                elif current_career:
                    # Add to description
                    current_career["description"] = current_career.get("description", "") + " " + line.strip()
        
        if current_career:
            careers.append(current_career)
        
        return careers[:5] if careers else self._get_fallback_recommendations({})
    
    def _get_openai_development_plan(self, prompt):
        """Get development plan using OpenAI"""
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a career development expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        content = response.choices[0].message.content
        try:
            return json.loads(content)
        except:
            return self._get_fallback_development_plan([])
    
    def _get_anthropic_development_plan(self, prompt):
        """Get development plan using Anthropic"""
        response = self.anthropic_client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1000,
            temperature=0.7,
            system="You are a career development expert.",
            messages=[{"role": "user", "content": prompt}]
        )
        
        content = response.content[0].text
        try:
            return json.loads(content)
        except:
            return self._get_fallback_development_plan([])
    
    def _get_gemini_development_plan(self, prompt):
        """Get development plan using Google Gemini"""
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        
        try:
            return json.loads(response.text)
        except:
            return self._get_fallback_development_plan([])

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
    
    def generate_coaching_questions(self,
                                  coachee_riasec_scores: Dict[str, float],
                                  coaching_context: str = "general",
                                  coachee_info: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Generate RIASEC-tailored coaching questions for career coaches"""
        
        prompt = self._create_coaching_questions_prompt(coachee_riasec_scores, coaching_context, coachee_info)
        
        try:
            if self.openai_available:
                return self._get_openai_coaching_questions(prompt)
            elif self.anthropic_available:
                return self._get_anthropic_coaching_questions(prompt)
            elif self.google_available:
                return self._get_google_coaching_questions(prompt)
            else:
                return self._get_fallback_coaching_questions(coachee_riasec_scores, coaching_context)
        except Exception as e:
            st.error(f"Error generating coaching questions: {str(e)}")
            return self._get_fallback_coaching_questions(coachee_riasec_scores, coaching_context)
    
    def generate_manager_coaching_questions(self,
                                          team_member_riasec: Dict[str, float],
                                          team_member_info: Dict[str, Any],
                                          management_context: str = "development") -> List[Dict[str, Any]]:
        """Generate RIASEC-tailored coaching questions for managers"""
        
        prompt = self._create_manager_coaching_prompt(team_member_riasec, team_member_info, management_context)
        
        try:
            if self.openai_available:
                return self._get_openai_manager_questions(prompt)
            elif self.anthropic_available:
                return self._get_anthropic_manager_questions(prompt)
            elif self.google_available:
                return self._get_google_manager_questions(prompt)
            else:
                return self._get_fallback_manager_questions(team_member_riasec, management_context)
        except Exception as e:
            st.error(f"Error generating manager questions: {str(e)}")
            return self._get_fallback_manager_questions(team_member_riasec, management_context)
    
    def generate_team_insights(self,
                             team_riasec_profiles: List[Dict[str, Any]],
                             team_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate insights about team dynamics based on RIASEC profiles"""
        
        prompt = self._create_team_insights_prompt(team_riasec_profiles, team_context)
        
        try:
            if self.openai_available:
                return self._get_openai_team_insights(prompt)
            elif self.anthropic_available:
                return self._get_anthropic_team_insights(prompt)
            elif self.google_available:
                return self._get_google_team_insights(prompt)
            else:
                return self._get_fallback_team_insights(team_riasec_profiles)
        except Exception as e:
            st.error(f"Error generating team insights: {str(e)}")
            return self._get_fallback_team_insights(team_riasec_profiles)
    
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
    
    def _create_coaching_questions_prompt(self, 
                                        coachee_riasec_scores: Dict[str, float],
                                        coaching_context: str,
                                        coachee_info: Dict[str, Any]) -> str:
        """Create prompt for RIASEC-tailored coaching questions"""
        
        sorted_scores = sorted(coachee_riasec_scores.items(), key=lambda x: x[1], reverse=True)
        top_types = sorted_scores[:3]
        
        prompt = f"""As an expert career coach, generate coaching questions tailored to this coachee's RIASEC profile.

Coachee's RIASEC Profile:
{json.dumps(coachee_riasec_scores, indent=2)}

Top 3 Types: {', '.join([f"{t[0]} ({t[1]:.1f})" for t in top_types])}

Coaching Context: {coaching_context}

Coachee Information:
- Current Role: {coachee_info.get('current_role', 'Not specified')}
- Career Stage: {coachee_info.get('career_stage', 'Not specified')}
- Goals: {coachee_info.get('goals', 'Not specified')}
- Challenges: {coachee_info.get('challenges', 'Not specified')}

Generate 10 powerful coaching questions that:
1. Align with their RIASEC personality type
2. Explore their natural strengths and interests
3. Address potential blind spots for their type
4. Help them discover authentic career paths
5. Challenge them appropriately based on their profile

For each question, provide:
- The question itself
- Why this question matters for their RIASEC type
- What insights it might reveal
- Follow-up probes

Return as JSON array:
[
  {{
    "question": "The coaching question",
    "riasec_relevance": "Why this matters for their type",
    "potential_insights": "What this might reveal",
    "follow_up_probes": ["probe1", "probe2"],
    "category": "strengths|values|challenges|growth|exploration"
  }}
]"""
        
        return prompt
    
    def _create_manager_coaching_prompt(self,
                                      team_member_riasec: Dict[str, float],
                                      team_member_info: Dict[str, Any],
                                      management_context: str) -> str:
        """Create prompt for manager coaching questions"""
        
        sorted_scores = sorted(team_member_riasec.items(), key=lambda x: x[1], reverse=True)
        top_types = sorted_scores[:3]
        
        prompt = f"""As a management coach, generate coaching questions for a manager to use with their team member based on the team member's RIASEC profile.

Team Member's RIASEC Profile:
{json.dumps(team_member_riasec, indent=2)}

Top 3 Types: {', '.join([f"{t[0]} ({t[1]:.1f})" for t in top_types])}

Management Context: {management_context}

Team Member Information:
- Name: {team_member_info.get('name', 'Team Member')}
- Current Role: {team_member_info.get('role', 'Not specified')}
- Time in Role: {team_member_info.get('tenure', 'Not specified')}
- Performance: {team_member_info.get('performance', 'Not specified')}
- Aspirations: {team_member_info.get('aspirations', 'Not specified')}

Generate 8 coaching questions that help the manager:
1. Understand how to motivate based on RIASEC type
2. Assign work that aligns with natural interests
3. Support career development in type-appropriate ways
4. Address potential frustrations common to their type
5. Build on their natural strengths

For each question, provide:
- The question for the manager to ask
- Why this question works for this RIASEC type
- What to listen for in the response
- How to act on the insights

Return as JSON array:
[
  {{
    "question": "The question to ask team member",
    "riasec_rationale": "Why this works for their type",
    "listen_for": ["key point 1", "key point 2"],
    "action_ideas": ["action 1", "action 2"],
    "context": "development|motivation|engagement|performance"
  }}
]"""
        
        return prompt
    
    def _create_team_insights_prompt(self,
                                   team_riasec_profiles: List[Dict[str, Any]],
                                   team_context: Dict[str, Any]) -> str:
        """Create prompt for team insights based on RIASEC profiles"""
        
        prompt = f"""Analyze this team's RIASEC profiles to provide insights on team dynamics and recommendations.

Team RIASEC Profiles:
{json.dumps(team_riasec_profiles, indent=2)}

Team Context:
- Team Size: {len(team_riasec_profiles)}
- Team Purpose: {team_context.get('purpose', 'Not specified')}
- Current Challenges: {team_context.get('challenges', 'Not specified')}
- Goals: {team_context.get('goals', 'Not specified')}

Provide comprehensive team insights including:
1. Team composition analysis (balance of types)
2. Natural strengths of this team combination
3. Potential blind spots or gaps
4. Communication recommendations based on type mix
5. Project assignment suggestions
6. Team development priorities
7. Potential conflicts and how to manage them
8. Collaboration strategies

Return as JSON:
{{
  "composition_summary": {{
    "dominant_types": ["type1", "type2"],
    "missing_types": ["type1", "type2"],
    "balance_assessment": "Well-balanced|Skewed toward X|Lacking Y"
  }},
  "team_strengths": ["strength1", "strength2", ...],
  "potential_gaps": ["gap1", "gap2", ...],
  "communication_tips": [
    {{"tip": "Communication tip", "rationale": "Why this works for this team"}}
  ],
  "project_recommendations": [
    {{"project_type": "Type of project", "why_suitable": "Rationale based on RIASEC mix"}}
  ],
  "development_priorities": ["priority1", "priority2", ...],
  "conflict_areas": [
    {{"potential_conflict": "Description", "prevention_strategy": "How to prevent/manage"}}
  ],
  "collaboration_strategies": ["strategy1", "strategy2", ...]
}}"""
        
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
    
    def _get_openai_coaching_questions(self, prompt: str) -> List[Dict[str, Any]]:
        """Get coaching questions using OpenAI"""
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert career coach specializing in RIASEC-based coaching."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        content = response.choices[0].message.content
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return self._get_fallback_coaching_questions({}, "general")
    
    def _get_openai_manager_questions(self, prompt: str) -> List[Dict[str, Any]]:
        """Get manager coaching questions using OpenAI"""
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a management coach helping managers have effective career conversations."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        content = response.choices[0].message.content
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return self._get_fallback_manager_questions({}, "development")
    
    def _get_openai_team_insights(self, prompt: str) -> Dict[str, Any]:
        """Get team insights using OpenAI"""
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an organizational psychologist specializing in team dynamics and RIASEC profiles."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        content = response.choices[0].message.content
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return self._get_fallback_team_insights([])
    
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
    
    def _get_anthropic_coaching_questions(self, prompt: str) -> List[Dict[str, Any]]:
        """Get coaching questions using Anthropic"""
        response = self.anthropic_client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=2000,
            temperature=0.7,
            system="You are an expert career coach specializing in RIASEC-based coaching.",
            messages=[{"role": "user", "content": prompt}]
        )
        
        content = response.content[0].text
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return self._get_fallback_coaching_questions({}, "general")
    
    def _get_anthropic_manager_questions(self, prompt: str) -> List[Dict[str, Any]]:
        """Get manager coaching questions using Anthropic"""
        response = self.anthropic_client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=2000,
            temperature=0.7,
            system="You are a management coach helping managers have effective career conversations.",
            messages=[{"role": "user", "content": prompt}]
        )
        
        content = response.content[0].text
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return self._get_fallback_manager_questions({}, "development")
    
    def _get_anthropic_team_insights(self, prompt: str) -> Dict[str, Any]:
        """Get team insights using Anthropic"""
        response = self.anthropic_client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=2000,
            temperature=0.7,
            system="You are an organizational psychologist specializing in team dynamics.",
            messages=[{"role": "user", "content": prompt}]
        )
        
        content = response.content[0].text
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return self._get_fallback_team_insights([])
    
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
    
    def _get_google_coaching_questions(self, prompt: str) -> List[Dict[str, Any]]:
        """Get coaching questions using Google Gemini"""
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        
        try:
            return json.loads(response.text)
        except json.JSONDecodeError:
            return self._get_fallback_coaching_questions({}, "general")
    
    def _get_google_manager_questions(self, prompt: str) -> List[Dict[str, Any]]:
        """Get manager coaching questions using Google Gemini"""
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        
        try:
            return json.loads(response.text)
        except json.JSONDecodeError:
            return self._get_fallback_manager_questions({}, "development")
    
    def _get_google_team_insights(self, prompt: str) -> Dict[str, Any]:
        """Get team insights using Google Gemini"""
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        
        try:
            return json.loads(response.text)
        except json.JSONDecodeError:
            return self._get_fallback_team_insights([])
    
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
    
    def _get_fallback_coaching_questions(self, riasec_scores: Dict[str, float], context: str) -> List[Dict[str, Any]]:
        """Provide fallback coaching questions based on RIASEC profile"""
        
        # Get top type
        if riasec_scores:
            top_type = max(riasec_scores.items(), key=lambda x: x[1])[0]
        else:
            top_type = "Investigative"
        
        # RIASEC-specific coaching questions
        questions_by_type = {
            "Realistic": [
                {
                    "question": "What hands-on projects or practical problems have energized you recently?",
                    "riasec_relevance": "Realistic types thrive on tangible, practical work",
                    "potential_insights": "Identifies specific technical interests and preferred working styles",
                    "follow_up_probes": ["What made it satisfying?", "How did you approach the challenge?"],
                    "category": "strengths"
                },
                {
                    "question": "How do you balance your preference for independent work with team collaboration needs?",
                    "riasec_relevance": "Realistic types often prefer working alone but need team skills",
                    "potential_insights": "Reveals collaboration challenges and growth opportunities",
                    "follow_up_probes": ["When is collaboration most valuable to you?", "What team dynamics work best?"],
                    "category": "challenges"
                }
            ],
            "Investigative": [
                {
                    "question": "What complex problems or mysteries are you currently trying to solve?",
                    "riasec_relevance": "Investigative types are driven by intellectual challenges",
                    "potential_insights": "Uncovers intellectual passions and analytical strengths",
                    "follow_up_probes": ["What approaches are you taking?", "What fascinates you about this?"],
                    "category": "strengths"
                },
                {
                    "question": "How do you translate your analytical insights into action and impact?",
                    "riasec_relevance": "Investigative types may struggle with implementation",
                    "potential_insights": "Identifies gaps between analysis and execution",
                    "follow_up_probes": ["What helps you move from thinking to doing?", "Where do you get stuck?"],
                    "category": "growth"
                }
            ],
            "Artistic": [
                {
                    "question": "What creative projects or ideas are you most excited about right now?",
                    "riasec_relevance": "Artistic types need creative expression for fulfillment",
                    "potential_insights": "Reveals creative drivers and potential career directions",
                    "follow_up_probes": ["What would it take to pursue this?", "How could this fit into your career?"],
                    "category": "exploration"
                },
                {
                    "question": "How do you handle the tension between creative freedom and practical constraints?",
                    "riasec_relevance": "Artistic types often struggle with structure and limitations",
                    "potential_insights": "Shows adaptability and professional maturity",
                    "follow_up_probes": ["When have constraints actually helped your creativity?", "What structures support you?"],
                    "category": "challenges"
                }
            ],
            "Social": [
                {
                    "question": "Describe a recent situation where you made a meaningful difference in someone's life.",
                    "riasec_relevance": "Social types are motivated by helping and impact",
                    "potential_insights": "Clarifies values and preferred ways of helping",
                    "follow_up_probes": ["What made this meaningful to you?", "How could you do more of this?"],
                    "category": "values"
                },
                {
                    "question": "How do you maintain boundaries while being naturally helpful and empathetic?",
                    "riasec_relevance": "Social types can overextend themselves helping others",
                    "potential_insights": "Reveals self-care practices and boundary challenges",
                    "follow_up_probes": ["When is it hardest to say no?", "What helps you recharge?"],
                    "category": "growth"
                }
            ],
            "Enterprising": [
                {
                    "question": "What leadership opportunity or business challenge excites you most right now?",
                    "riasec_relevance": "Enterprising types seek influence and leadership roles",
                    "potential_insights": "Identifies leadership aspirations and entrepreneurial interests",
                    "follow_up_probes": ["What impact do you want to have?", "What's holding you back?"],
                    "category": "exploration"
                },
                {
                    "question": "How do you balance your drive for results with developing others?",
                    "riasec_relevance": "Enterprising types may focus on outcomes over people",
                    "potential_insights": "Shows leadership maturity and growth areas",
                    "follow_up_probes": ["When have you seen people development drive better results?", "What's challenging about this?"],
                    "category": "growth"
                }
            ],
            "Conventional": [
                {
                    "question": "What systems or processes have you improved or organized recently?",
                    "riasec_relevance": "Conventional types excel at creating order and efficiency",
                    "potential_insights": "Highlights organizational strengths and process thinking",
                    "follow_up_probes": ["What impact did this have?", "What other areas need this attention?"],
                    "category": "strengths"
                },
                {
                    "question": "How do you stay engaged when work requires flexibility over structure?",
                    "riasec_relevance": "Conventional types may struggle with ambiguity",
                    "potential_insights": "Reveals adaptability and coping strategies",
                    "follow_up_probes": ["What helps you navigate uncertainty?", "When is flexibility actually helpful?"],
                    "category": "challenges"
                }
            ]
        }
        
        return questions_by_type.get(top_type, questions_by_type["Investigative"])
    
    def _get_fallback_manager_questions(self, team_member_riasec: Dict[str, float], context: str) -> List[Dict[str, Any]]:
        """Provide fallback manager coaching questions based on team member's RIASEC"""
        
        # Get top type
        if team_member_riasec:
            top_type = max(team_member_riasec.items(), key=lambda x: x[1])[0]
        else:
            top_type = "Investigative"
        
        # Manager questions tailored to team member's type
        manager_questions = {
            "Realistic": [
                {
                    "question": "What hands-on projects could I assign you that would really energize you?",
                    "riasec_rationale": "Realistic types need tangible, practical work to stay engaged",
                    "listen_for": ["Technical challenges", "Building/fixing things", "Clear outcomes"],
                    "action_ideas": ["Assign technical projects", "Reduce meetings", "Provide tools/resources"],
                    "context": "engagement"
                },
                {
                    "question": "How can I better support your need for independent work while meeting team goals?",
                    "riasec_rationale": "Realistic types often work best with autonomy",
                    "listen_for": ["Collaboration pain points", "Preferred work style", "Communication needs"],
                    "action_ideas": ["Create solo work time", "Clarify when collaboration is essential", "Respect work style"],
                    "context": "performance"
                }
            ],
            "Investigative": [
                {
                    "question": "What complex problems would you love to dig into if you had the time?",
                    "riasec_rationale": "Investigative types are motivated by intellectual challenges",
                    "listen_for": ["Research interests", "Analytical projects", "Learning desires"],
                    "action_ideas": ["Assign research projects", "Provide learning time", "Connect with experts"],
                    "context": "development"
                },
                {
                    "question": "How can I help you see the practical impact of your analytical work?",
                    "riasec_rationale": "Investigative types may
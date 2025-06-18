import os
import streamlit as st
from typing import Optional, Dict, Any
import openai
import anthropic
import google.generativeai as genai

class LLMManager:
    def __init__(self):
        self.providers = {
            'openai': self._call_openai,
            'anthropic': self._call_anthropic,
            'google': self._call_google
        }
        self.initialize_clients()
    
    def initialize_clients(self):
        """Initialize LLM clients with API keys"""
        # OpenAI
        openai_key = st.session_state.get('openai_api_key') or os.getenv('OPENAI_API_KEY')
        if openai_key:
            openai.api_key = openai_key
        
        # Anthropic
        anthropic_key = st.session_state.get('anthropic_api_key') or os.getenv('ANTHROPIC_API_KEY')
        if anthropic_key:
            self.anthropic_client = anthropic.Anthropic(api_key=anthropic_key)
        else:
            self.anthropic_client = None
        
        # Google
        google_key = st.session_state.get('google_api_key') or os.getenv('GOOGLE_API_KEY')
        if google_key:
            genai.configure(api_key=google_key)
            self.google_model = genai.GenerativeModel('gemini-pro')
        else:
            self.google_model = None
    
    def get_response(self, prompt: str, provider: Optional[str] = None, **kwargs) -> str:
        """Get response from selected LLM provider"""
        if provider is None:
            provider = st.session_state.get('llm_provider', 'openai')
        
        if provider not in self.providers:
            return "Invalid LLM provider selected"
        
        try:
            return self.providers[provider](prompt, **kwargs)
        except Exception as e:
            st.error(f"Error calling {provider}: {str(e)}")
            return f"Error: Unable to get response from {provider}. Please check your API key."
    
    def _call_openai(self, prompt: str, model: str = "gpt-3.5-turbo", **kwargs) -> str:
        """Call OpenAI API"""
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful career counselor and coach."},
                    {"role": "user", "content": prompt}
                ],
                temperature=kwargs.get('temperature', 0.7),
                max_tokens=kwargs.get('max_tokens', 1000)
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    def _call_anthropic(self, prompt: str, model: str = "claude-2", **kwargs) -> str:
        """Call Anthropic API"""
        if not self.anthropic_client:
            raise Exception("Anthropic API key not configured")
        
        try:
            response = self.anthropic_client.messages.create(
                model=model,
                max_tokens=kwargs.get('max_tokens', 1000),
                temperature=kwargs.get('temperature', 0.7),
                system="You are a helpful career counselor and coach.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text
        except Exception as e:
            raise Exception(f"Anthropic API error: {str(e)}")
    
    def _call_google(self, prompt: str, **kwargs) -> str:
        """Call Google Gemini API"""
        if not self.google_model:
            raise Exception("Google API key not configured")
        
        try:
            response = self.google_model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=kwargs.get('temperature', 0.7),
                    max_output_tokens=kwargs.get('max_tokens', 1000),
                )
            )
            return response.text
        except Exception as e:
            raise Exception(f"Google API error: {str(e)}")
    
    def generate_coaching_response(self, context: Dict[str, Any], question: str) -> str:
        """Generate a coaching response based on user context"""
        prompt = f"""
        As a professional career coach, provide guidance based on the following context:
        
        User Profile:
        - RIASEC Scores: {context.get('riasec_scores', {})}
        - Top Skills: {context.get('skills', [])}
        - Work Values: {context.get('values', [])}
        - Career Interests: {context.get('career_interests', [])}
        
        Question: {question}
        
        Please provide a thoughtful, personalized response that:
        1. Acknowledges their unique profile
        2. Provides specific, actionable advice
        3. Encourages self-reflection
        4. Suggests next steps
        """
        
        return self.get_response(prompt)
    
    def analyze_career_fit(self, user_profile: Dict[str, Any], career: str) -> Dict[str, Any]:
        """Analyze how well a career fits a user's profile"""
        prompt = f"""
        Analyze the fit between this user profile and career:
        
        User Profile:
        - RIASEC Scores: {user_profile.get('riasec_scores', {})}
        - Skills: {user_profile.get('skills', [])}
        - Values: {user_profile.get('values', [])}
        
        Career: {career}
        
        Provide a JSON response with:
        1. overall_fit_score (0-100)
        2. strengths (list of 3-5 points)
        3. challenges (list of 2-3 points)
        4. development_areas (list of 2-3 skills to develop)
        5. next_steps (list of 3-5 actionable steps)
        """
        
        response = self.get_response(prompt)
        # Parse and return structured data
        try:
            import json
            return json.loads(response)
        except:
            return {"error": "Unable to parse response", "raw": response}

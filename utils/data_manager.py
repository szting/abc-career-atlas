import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import pandas as pd
import streamlit as st

class DataManager:
    def __init__(self, drive_manager):
        self.drive_manager = drive_manager
        self.local_data_path = Path("data")
        self.ensure_directories()
    
    def ensure_directories(self):
        """Ensure necessary directories exist"""
        directories = [
            self.local_data_path,
            self.local_data_path / "users",
            self.local_data_path / "frameworks",
            self.local_data_path / "careers"
        ]
        for directory in directories:
            directory.mkdir(exist_ok=True)
    
    def save_assessment(self, username: str, assessment_type: str, data: Dict[str, Any]):
        """Save assessment data"""
        timestamp = datetime.now().isoformat()
        assessment_data = {
            "timestamp": timestamp,
            "type": assessment_type,
            "data": data
        }
        
        # Save to Google Drive if available, otherwise local
        return self.drive_manager.save_user_data(
            username, 
            f"assessments/{assessment_type}_{timestamp}", 
            assessment_data
        )
    
    def load_latest_assessment(self, username: str, assessment_type: str) -> Optional[Dict[str, Any]]:
        """Load the most recent assessment of a given type"""
        # For now, using local storage
        user_path = self.local_data_path / "users" / username / "assessments"
        if not user_path.exists():
            return None
        
        # Find latest assessment file
        assessment_files = list(user_path.glob(f"{assessment_type}_*.json"))
        if not assessment_files:
            return None
        
        latest_file = max(assessment_files, key=lambda f: f.stat().st_mtime)
        with open(latest_file, 'r') as f:
            return json.load(f)
    
    def save_coaching_session(self, username: str, session_data: Dict[str, Any]):
        """Save coaching session data"""
        timestamp = datetime.now().isoformat()
        session_data["timestamp"] = timestamp
        
        return self.drive_manager.save_user_data(
            username,
            f"coaching_sessions/session_{timestamp}",
            session_data
        )
    
    def load_user_profile(self, username: str) -> Dict[str, Any]:
        """Load complete user profile including all assessments"""
        profile = {
            "username": username,
            "assessments": {},
            "coaching_sessions": [],
            "custom_frameworks": []
        }
        
        # Load RIASEC assessment
        riasec = self.load_latest_assessment(username, "riasec")
        if riasec:
            profile["assessments"]["riasec"] = riasec
        
        # Load skills assessment
        skills = self.load_latest_assessment(username, "skills")
        if skills:
            profile["assessments"]["skills"] = skills
        
        # Load values assessment
        values = self.load_latest_assessment(username, "values")
        if values:
            profile["assessments"]["values"] = values
        
        return profile
    
    def save_custom_framework(self, framework_type: str, name: str, data: Dict[str, Any]):
        """Save custom framework (skills or careers)"""
        framework_path = self.local_data_path / "frameworks" / framework_type
        framework_path.mkdir(exist_ok=True)
        
        file_path = framework_path / f"{name}.json"
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        return str(file_path)
    
    def load_frameworks(self, framework_type: str) -> Dict[str, Any]:
        """Load all frameworks of a given type"""
        framework_path = self.local_data_path / "frameworks" / framework_type
        frameworks = {}
        
        if framework_path.exists():
            for file_path in framework_path.glob("*.json"):
                with open(file_path, 'r') as f:
                    frameworks[file_path.stem] = json.load(f)
        
        return frameworks
    
    def export_user_data(self, username: str) -> Dict[str, Any]:
        """Export all user data for download"""
        profile = self.load_user_profile(username)
        export_data = {
            "export_date": datetime.now().isoformat(),
            "username": username,
            "profile": profile
        }
        
        return export_data
    
    def calculate_riasec_scores(self, responses: List[int]) -> Dict[str, float]:
        """Calculate RIASEC scores from assessment responses"""
        # Group responses by RIASEC type (assuming 10 questions per type)
        riasec_types = ['realistic', 'investigative', 'artistic', 'social', 'enterprising', 'conventional']
        scores = {}
        
        for i, riasec_type in enumerate(riasec_types):
            type_responses = responses[i*10:(i+1)*10]
            scores[riasec_type] = sum(type_responses) / len(type_responses) * 20  # Scale to 0-100
        
        return scores
    
    def get_top_careers(self, riasec_scores: Dict[str, float], num_careers: int = 10) -> List[Dict[str, Any]]:
        """Get top career recommendations based on RIASEC scores"""
        # Load career database
        careers_path = self.local_data_path / "careers" / "default_careers.json"
        
        if careers_path.exists():
            with open(careers_path, 'r') as f:
                careers = json.load(f)
        else:
            # Return placeholder careers if no database
            return [
                {"title": "Software Developer", "match_score": 85},
                {"title": "Data Scientist", "match_score": 82},
                {"title": "UX Designer", "match_score": 78}
            ]
        
        # Calculate match scores for each career
        career_matches = []
        for career in careers:
            match_score = self._calculate_career_match(riasec_scores, career.get('riasec_profile', {}))
            career_matches.append({
                **career,
                'match_score': match_score
            })
        
        # Sort by match score and return top N
        career_matches.sort(key=lambda x: x['match_score'], reverse=True)
        return career_matches[:num_careers]
    
    def _calculate_career_match(self, user_scores: Dict[str, float], career_profile: Dict[str, float]) -> float:
        """Calculate match score between user RIASEC and career profile"""
        if not career_profile:
            return 0
        
        total_diff = 0
        for riasec_type in user_scores:
            user_score = user_scores.get(riasec_type, 0)
            career_score = career_profile.get(riasec_type, 0)
            total_diff += abs(user_score - career_score)
        
        # Convert difference to match percentage
        max_possible_diff = 600  # 6 types * 100 max difference
        match_score = (1 - total_diff / max_possible_diff) * 100
        
        return max(0, min(100, match_score))

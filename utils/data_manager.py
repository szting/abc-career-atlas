import json
import os
from datetime import datetime
import pandas as pd
import streamlit as st

class DataManager:
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        self.ensure_data_directory()
    
    def ensure_data_directory(self):
        """Ensure data directory exists"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        
        # Create subdirectories
        subdirs = ['assessments', 'reports', 'exports', 'user_data']
        for subdir in subdirs:
            path = os.path.join(self.data_dir, subdir)
            if not os.path.exists(path):
                os.makedirs(path)
    
    def save_assessment(self, assessment_data):
        """Save assessment data locally"""
        username = assessment_data['username']
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"assessment_{username}_{timestamp}.json"
        
        # Create user directory if it doesn't exist
        user_dir = os.path.join(self.data_dir, 'user_data', username)
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)
        
        # Save to user directory
        filepath = os.path.join(user_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(assessment_data, f, indent=2)
        
        # Also save to assessments directory for easy access
        assessments_filepath = os.path.join(self.data_dir, 'assessments', filename)
        with open(assessments_filepath, 'w') as f:
            json.dump(assessment_data, f, indent=2)
        
        return filepath
    
    def load_assessment(self, username, latest=True):
        """Load assessment data for a user"""
        user_dir = os.path.join(self.data_dir, 'user_data', username)
        
        # Check if user directory exists
        if not os.path.exists(user_dir):
            return None
        
        user_files = [f for f in os.listdir(user_dir) 
                     if f.startswith(f"assessment_{username}_") and f.endswith('.json')]
        
        if not user_files:
            return None
        
        if latest:
            # Get the most recent assessment
            user_files.sort(reverse=True)
            filepath = os.path.join(user_dir, user_files[0])
            
            with open(filepath, 'r') as f:
                return json.load(f)
        else:
            # Return all assessments
            assessments = []
            for file in sorted(user_files, reverse=True):
                filepath = os.path.join(user_dir, file)
                with open(filepath, 'r') as f:
                    assessments.append(json.load(f))
            return assessments
    
    def get_user_history(self, username):
        """Get assessment history for a user"""
        assessments = self.load_assessment(username, latest=False)
        if not assessments:
            return pd.DataFrame()
        
        history = []
        for assessment in assessments:
            history.append({
                'Date': assessment.get('timestamp', 'Unknown'),
                'Realistic': assessment.get('scores', {}).get('Realistic', 0),
                'Investigative': assessment.get('scores', {}).get('Investigative', 0),
                'Artistic': assessment.get('scores', {}).get('Artistic', 0),
                'Social': assessment.get('scores', {}).get('Social', 0),
                'Enterprising': assessment.get('scores', {}).get('Enterprising', 0),
                'Conventional': assessment.get('scores', {}).get('Conventional', 0),
                'Top Type': assessment.get('top_type', 'Unknown')
            })
        
        return pd.DataFrame(history)
    
    def save_report(self, username, report_data):
        """Save generated report"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"report_{username}_{timestamp}.json"
        
        # Create user directory if it doesn't exist
        user_dir = os.path.join(self.data_dir, 'user_data', username)
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)
        
        # Save to user directory
        filepath = os.path.join(user_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        # Also save to reports directory
        reports_filepath = os.path.join(self.data_dir, 'reports', filename)
        with open(reports_filepath, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        return filepath
    
    def export_to_csv(self, username):
        """Export user data to CSV"""
        history = self.get_user_history(username)
        if history.empty:
            return None
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"export_{username}_{timestamp}.csv"
        filepath = os.path.join(self.data_dir, 'exports', filename)
        
        history.to_csv(filepath, index=False)
        return filepath
    
    def generate_report(self, assessment_data, career_recommendations=None):
        """Generate a comprehensive report"""
        report = {
            'generated_at': datetime.now().isoformat(),
            'user_info': {
                'username': assessment_data['username'],
                'assessment_date': assessment_data.get('timestamp', datetime.now().isoformat())
            },
            'riasec_scores': assessment_data.get('scores', {}),
            'top_types': self._get_top_types(assessment_data.get('scores', {})),
            'career_recommendations': career_recommendations or [],
            'additional_info': assessment_data.get('additional_info', {}),
            'interpretation': self._generate_interpretation(assessment_data.get('scores', {}))
        }
        
        # Save report
        self.save_report(assessment_data['username'], report)
        
        return report
    
    def _get_top_types(self, scores):
        """Get top 3 RIASEC types"""
        if not scores:
            return []
        
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [{'type': t, 'score': s} for t, s in sorted_scores[:3]]
    
    def _generate_interpretation(self, scores):
        """Generate interpretation of RIASEC scores"""
        if not scores:
            return "No assessment data available."
        
        top_types = self._get_top_types(scores)
        if not top_types:
            return "Unable to determine personality types."
        
        interpretations = {
            'Realistic': "You prefer practical, hands-on activities and working with tools or machines.",
            'Investigative': "You enjoy solving complex problems and conducting research.",
            'Artistic': "You value creativity, self-expression, and working in unstructured environments.",
            'Social': "You like helping others and working in collaborative environments.",
            'Enterprising': "You enjoy leadership roles and influencing others.",
            'Conventional': "You prefer organized, structured work with clear procedures."
        }
        
        primary = top_types[0]['type']
        interpretation = f"Your primary type is {primary}. {interpretations.get(primary, '')}"
        
        if len(top_types) > 1:
            secondary = top_types[1]['type']
            interpretation += f"\n\nYour secondary type is {secondary}. {interpretations.get(secondary, '')}"
        
        return interpretation
    
    def get_statistics(self):
        """Get overall statistics from all assessments"""
        assessments_dir = os.path.join(self.data_dir, 'assessments')
        
        if not os.path.exists(assessments_dir):
            return None
        
        all_files = [f for f in os.listdir(assessments_dir) if f.endswith('.json')]
        
        if not all_files:
            return None
        
        all_scores = {
            'Realistic': [],
            'Investigative': [],
            'Artistic': [],
            'Social': [],
            'Enterprising': [],
            'Conventional': []
        }
        
        total_assessments = 0
        users = set()
        
        for file in all_files:
            filepath = os.path.join(assessments_dir, file)
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    scores = data.get('scores', {})
                    username = data.get('username', 'unknown')
                    users.add(username)
                    total_assessments += 1
                    
                    for category, score in scores.items():
                        if category in all_scores:
                            all_scores[category].append(score)
            except Exception as e:
                st.warning(f"Error reading file {file}: {str(e)}")
                continue
        
        # Calculate statistics
        stats = {
            'total_assessments': total_assessments,
            'unique_users': len(users),
            'category_stats': {}
        }
        
        for category, scores in all_scores.items():
            if scores:
                stats['category_stats'][category] = {
                    'mean': sum(scores) / len(scores),
                    'min': min(scores),
                    'max': max(scores),
                    'count': len(scores)
                }
        
        return stats
    
    def load_questions(self):
        """Load RIASEC assessment questions"""
        questions_file = os.path.join(self.data_dir, 'assessments', 'riasec_questions.json')
        
        if not os.path.exists(questions_file):
            st.error(f"Questions file not found at {questions_file}")
            return None
        
        try:
            with open(questions_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            st.error(f"Error loading questions: {str(e)}")
            return None
    
    def load_careers(self, category=None):
        """Load career data"""
        careers_dir = os.path.join(self.data_dir, 'careers')
        
        if not os.path.exists(careers_dir):
            return []
        
        all_careers = []
        
        # Load all career files
        career_files = [f for f in os.listdir(careers_dir) if f.endswith('.json')]
        
        for file in career_files:
            filepath = os.path.join(careers_dir, file)
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    if category and data.get('category') != category:
                        continue
                    all_careers.extend(data.get('careers', []))
            except Exception as e:
                st.warning(f"Error loading career file {file}: {str(e)}")
                continue
        
        return all_careers
    
    def get_career_recommendations(self, riasec_scores, top_n=5):
        """Get career recommendations based on RIASEC scores"""
        all_careers = self.load_careers()
        
        if not all_careers:
            return []
        
        # Get top 2 RIASEC types
        top_types = self._get_top_types(riasec_scores)
        if not top_types:
            return []
        
        primary_type = top_types[0]['type'][0]  # First letter of type
        secondary_type = top_types[1]['type'][0] if len(top_types) > 1 else None
        
        # Score careers based on RIASEC match
        career_scores = []
        for career in all_careers:
            riasec_codes = career.get('riasec_codes', [])
            score = 0
            
            # Primary type match
            if primary_type in riasec_codes:
                score += 3
                if riasec_codes.index(primary_type) == 0:
                    score += 2  # Bonus for primary position
            
            # Secondary type match
            if secondary_type and secondary_type in riasec_codes:
                score += 2
                if riasec_codes.index(secondary_type) == 1:
                    score += 1  # Bonus for secondary position
            
            if score > 0:
                career_scores.append({
                    'career': career,
                    'score': score,
                    'match_percentage': (score / 6) * 100  # Max score is 6
                })
        
        # Sort by score and return top N
        career_scores.sort(key=lambda x: x['score'], reverse=True)
        return career_scores[:top_n]
    
    def save_user_preferences(self, username, preferences):
        """Save user preferences"""
        prefs_file = os.path.join(self.data_dir, 'user_data', username, 'preferences.json')
        
        # Ensure user directory exists
        user_dir = os.path.join(self.data_dir, 'user_data', username)
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)
        
        with open(prefs_file, 'w') as f:
            json.dump(preferences, f, indent=2)
    
    def load_user_preferences(self, username):
        """Load user preferences"""
        prefs_file = os.path.join(self.data_dir, 'user_data', username, 'preferences.json')
        
        if not os.path.exists(prefs_file):
            return {}
        
        try:
            with open(prefs_file, 'r') as f:
                return json.load(f)
        except Exception:
            return {}

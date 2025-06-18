import json
import os
from datetime import datetime
import pandas as pd
from utils.google_drive import GoogleDriveManager
import streamlit as st

class DataManager:
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        self.ensure_data_directory()
        self.drive_manager = GoogleDriveManager()
    
    def ensure_data_directory(self):
        """Ensure data directory exists"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        
        # Create subdirectories
        subdirs = ['assessments', 'reports', 'exports']
        for subdir in subdirs:
            path = os.path.join(self.data_dir, subdir)
            if not os.path.exists(path):
                os.makedirs(path)
    
    def save_assessment(self, assessment_data):
        """Save assessment data locally and to Google Drive"""
        username = assessment_data['username']
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"assessment_{username}_{timestamp}.json"
        
        # Save locally
        filepath = os.path.join(self.data_dir, 'assessments', filename)
        with open(filepath, 'w') as f:
            json.dump(assessment_data, f, indent=2)
        
        # Save to Google Drive
        try:
            self.drive_manager.upload_file(filepath, f"assessments/{filename}")
        except Exception as e:
            st.warning(f"Could not save to Google Drive: {str(e)}")
        
        return filepath
    
    def load_assessment(self, username, latest=True):
        """Load assessment data for a user"""
        assessments_dir = os.path.join(self.data_dir, 'assessments')
        user_files = [f for f in os.listdir(assessments_dir) 
                     if f.startswith(f"assessment_{username}_")]
        
        if not user_files:
            return None
        
        if latest:
            # Get the most recent assessment
            user_files.sort(reverse=True)
            filepath = os.path.join(assessments_dir, user_files[0])
            
            with open(filepath, 'r') as f:
                return json.load(f)
        else:
            # Return all assessments
            assessments = []
            for file in user_files:
                filepath = os.path.join(assessments_dir, file)
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
                'Date': assessment['timestamp'],
                'Realistic': assessment['scores'].get('Realistic', 0),
                'Investigative': assessment['scores'].get('Investigative', 0),
                'Artistic': assessment['scores'].get('Artistic', 0),
                'Social': assessment['scores'].get('Social', 0),
                'Enterprising': assessment['scores'].get('Enterprising', 0),
                'Conventional': assessment['scores'].get('Conventional', 0)
            })
        
        return pd.DataFrame(history)
    
    def save_report(self, username, report_data):
        """Save generated report"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"report_{username}_{timestamp}.json"
        filepath = os.path.join(self.data_dir, 'reports', filename)
        
        with open(filepath, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        # Upload to Google Drive
        try:
            self.drive_manager.upload_file(filepath, f"reports/{filename}")
        except Exception as e:
            st.warning(f"Could not save report to Google Drive: {str(e)}")
        
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
    
    def generate_report(self, assessment_data, career_recommendations):
        """Generate a comprehensive report"""
        report = {
            'generated_at': datetime.now().isoformat(),
            'user_info': {
                'username': assessment_data['username'],
                'assessment_date': assessment_data['timestamp']
            },
            'riasec_scores': assessment_data['scores'],
            'top_types': sorted(assessment_data['scores'].items(), 
                              key=lambda x: x[1], reverse=True)[:3],
            'career_recommendations': career_recommendations,
            'additional_info': assessment_data['additional_info']
        }
        
        # Save report
        self.save_report(assessment_data['username'], report)
        
        # For now, return JSON. In production, this would generate a PDF
        return json.dumps(report, indent=2).encode()
    
    def get_statistics(self):
        """Get overall statistics from all assessments"""
        assessments_dir = os.path.join(self.data_dir, 'assessments')
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
        
        for file in all_files:
            filepath = os.path.join(assessments_dir, file)
            with open(filepath, 'r') as f:
                data = json.load(f)
                scores = data.get('scores', {})
                for category, score in scores.items():
                    if category in all_scores:
                        all_scores[category].append(score)
        
        # Calculate statistics
        stats = {}
        for category, scores in all_scores.items():
            if scores:
                stats[category] = {
                    'mean': sum(scores) / len(scores),
                    'min': min(scores),
                    'max': max(scores),
                    'count': len(scores)
                }
        
        return stats

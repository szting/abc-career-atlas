import json
import os
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import streamlit as st
from .data_manager import DataManager

class AssessmentManager:
    """Manages RIASEC assessments, scoring, and question flow"""
    
    def __init__(self):
        self.data_manager = DataManager()
        self.questions = self._load_questions()
        self.riasec_types = ['Realistic', 'Investigative', 'Artistic', 'Social', 'Enterprising', 'Conventional']
        
    def _load_questions(self) -> List[Dict]:
        """Load assessment questions from data file"""
        questions_path = os.path.join('data', 'assessments', 'riasec_questions.json')
        try:
            with open(questions_path, 'r') as f:
                data = json.load(f)
                return data.get('questions', [])
        except Exception as e:
            st.error(f"Error loading questions: {str(e)}")
            return self._get_default_questions()
    
    def _get_default_questions(self) -> List[Dict]:
        """Return default questions if file loading fails"""
        # Minimal set of questions as fallback
        return [
            {
                "id": 1,
                "text": "I enjoy working with tools and machines",
                "type": "Realistic",
                "category": "interests"
            },
            {
                "id": 2,
                "text": "I like to solve complex problems",
                "type": "Investigative",
                "category": "interests"
            },
            {
                "id": 3,
                "text": "I enjoy creative activities like art, music, or writing",
                "type": "Artistic",
                "category": "interests"
            },
            {
                "id": 4,
                "text": "I like helping and teaching others",
                "type": "Social",
                "category": "interests"
            },
            {
                "id": 5,
                "text": "I enjoy leading and persuading people",
                "type": "Enterprising",
                "category": "interests"
            },
            {
                "id": 6,
                "text": "I prefer working with data and details",
                "type": "Conventional",
                "category": "interests"
            }
        ]
    
    def get_assessment_questions(self, category: Optional[str] = None) -> List[Dict]:
        """Get assessment questions, optionally filtered by category"""
        if category:
            return [q for q in self.questions if q.get('category') == category]
        return self.questions
    
    def get_question_by_id(self, question_id: int) -> Optional[Dict]:
        """Get a specific question by ID"""
        for question in self.questions:
            if question.get('id') == question_id:
                return question
        return None
    
    def get_questions_by_type(self, riasec_type: str) -> List[Dict]:
        """Get all questions for a specific RIASEC type"""
        return [q for q in self.questions if q.get('type') == riasec_type]
    
    def calculate_scores(self, responses: Dict[int, int]) -> Dict[str, float]:
        """
        Calculate RIASEC scores from assessment responses
        
        Args:
            responses: Dict mapping question_id to response value (1-5)
            
        Returns:
            Dict mapping RIASEC type to normalized score (0-100)
        """
        # Initialize scores
        type_scores = {riasec_type: 0 for riasec_type in self.riasec_types}
        type_counts = {riasec_type: 0 for riasec_type in self.riasec_types}
        
        # Calculate raw scores
        for question_id, response_value in responses.items():
            question = self.get_question_by_id(question_id)
            if question:
                question_type = question.get('type')
                if question_type in type_scores:
                    type_scores[question_type] += response_value
                    type_counts[question_type] += 1
        
        # Normalize scores to 0-100 scale
        normalized_scores = {}
        for riasec_type in self.riasec_types:
            if type_counts[riasec_type] > 0:
                # Average score per question * 20 to get 0-100 scale
                avg_score = type_scores[riasec_type] / type_counts[riasec_type]
                normalized_scores[riasec_type] = round(avg_score * 20, 1)
            else:
                normalized_scores[riasec_type] = 0.0
        
        return normalized_scores
    
    def get_top_types(self, scores: Dict[str, float], top_n: int = 3) -> List[Tuple[str, float]]:
        """Get the top N RIASEC types by score"""
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_scores[:top_n]
    
    def generate_holland_code(self, scores: Dict[str, float]) -> str:
        """Generate 3-letter Holland code from scores"""
        top_types = self.get_top_types(scores, 3)
        code_map = {
            'Realistic': 'R',
            'Investigative': 'I',
            'Artistic': 'A',
            'Social': 'S',
            'Enterprising': 'E',
            'Conventional': 'C'
        }
        return ''.join([code_map[type_name] for type_name, _ in top_types])
    
    def interpret_scores(self, scores: Dict[str, float]) -> Dict[str, any]:
        """
        Provide interpretation of RIASEC scores
        
        Returns dict with:
        - holland_code: 3-letter code
        - primary_type: Highest scoring type with description
        - secondary_types: Next two types with descriptions
        - balance_analysis: Analysis of score distribution
        - career_themes: Common themes based on top types
        """
        top_types = self.get_top_types(scores, 3)
        holland_code = self.generate_holland_code(scores)
        
        # Type descriptions
        type_descriptions = {
            'Realistic': {
                'summary': 'Practical, hands-on, and mechanically inclined',
                'strengths': ['Problem-solving', 'Working with tools', 'Physical coordination'],
                'work_style': 'Prefers concrete tasks and tangible results'
            },
            'Investigative': {
                'summary': 'Analytical, intellectual, and scientific',
                'strengths': ['Research', 'Analysis', 'Abstract thinking'],
                'work_style': 'Enjoys solving complex problems and theoretical work'
            },
            'Artistic': {
                'summary': 'Creative, expressive, and imaginative',
                'strengths': ['Creativity', 'Self-expression', 'Innovation'],
                'work_style': 'Prefers unstructured environments and creative freedom'
            },
            'Social': {
                'summary': 'Helpful, cooperative, and people-oriented',
                'strengths': ['Communication', 'Teaching', 'Empathy'],
                'work_style': 'Enjoys working with and helping others'
            },
            'Enterprising': {
                'summary': 'Persuasive, ambitious, and leadership-oriented',
                'strengths': ['Leadership', 'Persuasion', 'Decision-making'],
                'work_style': 'Thrives in competitive environments and enjoys influence'
            },
            'Conventional': {
                'summary': 'Organized, detail-oriented, and systematic',
                'strengths': ['Organization', 'Attention to detail', 'Following procedures'],
                'work_style': 'Prefers structured environments and clear expectations'
            }
        }
        
        # Analyze score balance
        score_values = list(scores.values())
        score_range = max(score_values) - min(score_values)
        
        if score_range < 20:
            balance = "Well-balanced across all types"
        elif score_range < 40:
            balance = "Moderate differentiation with some clear preferences"
        else:
            balance = "Strong differentiation with clear type preferences"
        
        # Determine career themes based on top types
        career_themes = self._get_career_themes(top_types)
        
        interpretation = {
            'holland_code': holland_code,
            'primary_type': {
                'name': top_types[0][0],
                'score': top_types[0][1],
                'description': type_descriptions[top_types[0][0]]
            },
            'secondary_types': [
                {
                    'name': top_types[1][0],
                    'score': top_types[1][1],
                    'description': type_descriptions[top_types[1][0]]
                },
                {
                    'name': top_types[2][0],
                    'score': top_types[2][1],
                    'description': type_descriptions[top_types[2][0]]
                }
            ],
            'balance_analysis': balance,
            'career_themes': career_themes,
            'all_scores': scores
        }
        
        return interpretation
    
    def _get_career_themes(self, top_types: List[Tuple[str, float]]) -> List[str]:
        """Generate career themes based on type combinations"""
        type_combo = tuple(sorted([t[0] for t in top_types[:2]]))
        
        theme_map = {
            ('Realistic', 'Investigative'): ['Technical Problem-Solving', 'Engineering', 'Applied Sciences'],
            ('Realistic', 'Artistic'): ['Design Engineering', 'Architecture', 'Craftsmanship'],
            ('Realistic', 'Social'): ['Technical Training', 'Healthcare Technology', 'Skilled Trades Education'],
            ('Realistic', 'Enterprising'): ['Construction Management', 'Technical Sales', 'Manufacturing Leadership'],
            ('Realistic', 'Conventional'): ['Quality Control', 'Technical Documentation', 'Systems Maintenance'],
            ('Investigative', 'Artistic'): ['Scientific Innovation', 'Research Design', 'Data Visualization'],
            ('Investigative', 'Social'): ['Medical Research', 'Educational Technology', 'Science Communication'],
            ('Investigative', 'Enterprising'): ['Technology Entrepreneurship', 'Research Management', 'Consulting'],
            ('Investigative', 'Conventional'): ['Data Analysis', 'Laboratory Management', 'Technical Writing'],
            ('Artistic', 'Social'): ['Arts Education', 'Creative Therapy', 'Community Arts'],
            ('Artistic', 'Enterprising'): ['Creative Direction', 'Arts Management', 'Media Production'],
            ('Artistic', 'Conventional'): ['Graphic Design', 'Digital Arts', 'Content Management'],
            ('Social', 'Enterprising'): ['Human Resources', 'Educational Leadership', 'Community Development'],
            ('Social', 'Conventional'): ['Healthcare Administration', 'School Counseling', 'Social Services'],
            ('Enterprising', 'Conventional'): ['Business Management', 'Financial Services', 'Operations Management']
        }
        
        # Get themes for the combination
        themes = theme_map.get(type_combo, ['Leadership', 'Innovation', 'Problem-Solving'])
        
        return themes
    
    def save_assessment_result(self, user_id: str, scores: Dict[str, float], 
                             responses: Dict[int, int], additional_info: Dict = None) -> str:
        """
        Save assessment results
        
        Returns: assessment_id
        """
        interpretation = self.interpret_scores(scores)
        
        assessment_data = {
            'user_id': user_id,
            'timestamp': datetime.now().isoformat(),
            'scores': scores,
            'responses': responses,
            'interpretation': interpretation,
            'additional_info': additional_info or {},
            'version': '1.0'
        }
        
        # Save using data manager
        assessment_id = self.data_manager.save_assessment(user_id, assessment_data)
        
        return assessment_id
    
    def get_assessment_progress(self, responses: Dict[int, int]) -> Dict[str, any]:
        """Calculate assessment progress"""
        total_questions = len(self.questions)
        answered_questions = len(responses)
        
        # Calculate progress by category
        categories = set(q.get('category', 'general') for q in self.questions)
        category_progress = {}
        
        for category in categories:
            category_questions = [q for q in self.questions if q.get('category', 'general') == category]
            category_answered = sum(1 for q in category_questions if q['id'] in responses)
            category_progress[category] = {
                'total': len(category_questions),
                'answered': category_answered,
                'percentage': round((category_answered / len(category_questions) * 100) if category_questions else 0)
            }
        
        return {
            'total_questions': total_questions,
            'answered_questions': answered_questions,
            'percentage_complete': round((answered_questions / total_questions * 100) if total_questions > 0 else 0),
            'category_progress': category_progress,
            'is_complete': answered_questions >= total_questions
        }
    
    def validate_responses(self, responses: Dict[int, int]) -> Tuple[bool, List[str]]:
        """
        Validate assessment responses
        
        Returns: (is_valid, error_messages)
        """
        errors = []
        
        # Check if all questions are answered
        question_ids = {q['id'] for q in self.questions}
        answered_ids = set(responses.keys())
        missing_ids = question_ids - answered_ids
        
        if missing_ids:
            errors.append(f"Missing responses for questions: {sorted(missing_ids)}")
        
        # Validate response values (should be 1-5)
        for question_id, value in responses.items():
            if not isinstance(value, int) or value < 1 or value > 5:
                errors.append(f"Invalid response value for question {question_id}: {value}")
        
        # Check for valid question IDs
        invalid_ids = answered_ids - question_ids
        if invalid_ids:
            errors.append(f"Invalid question IDs in responses: {sorted(invalid_ids)}")
        
        return len(errors) == 0, errors
    
    def get_question_statistics(self, user_id: Optional[str] = None) -> Dict[str, any]:
        """Get statistics about question responses"""
        # This would analyze response patterns across assessments
        # For now, return basic stats
        return {
            'total_questions': len(self.questions),
            'questions_by_type': {
                riasec_type: len(self.get_questions_by_type(riasec_type))
                for riasec_type in self.riasec_types
            },
            'questions_by_category': self._count_by_category()
        }
    
    def _count_by_category(self) -> Dict[str, int]:
        """Count questions by category"""
        category_counts = {}
        for question in self.questions:
            category = question.get('category', 'general')
            category_counts[category] = category_counts.get(category, 0) + 1
        return category_counts
    
    def export_assessment_data(self, assessment_id: str, format: str = 'json') -> any:
        """Export assessment data in specified format"""
        # Load assessment data
        assessments = self.data_manager.load_user_assessments(st.session_state.get('username'))
        
        assessment_data = None
        for assessment in assessments:
            if assessment.get('id') == assessment_id:
                assessment_data = assessment
                break
        
        if not assessment_data:
            return None
        
        if format == 'json':
            return json.dumps(assessment_data, indent=2)
        elif format == 'summary':
            return self._format_assessment_summary(assessment_data)
        else:
            return assessment_data
    
    def _format_assessment_summary(self, assessment_data: Dict) -> str:
        """Format assessment data as readable summary"""
        interpretation = assessment_data.get('interpretation', {})
        scores = assessment_data.get('scores', {})
        
        summary = f"""
RIASEC Assessment Summary
========================
Date: {assessment_data.get('timestamp', 'Unknown')}
Holland Code: {interpretation.get('holland_code', 'N/A')}

Scores:
-------
"""
        for riasec_type, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
            summary += f"{riasec_type}: {score:.1f}/100\n"
        
        summary += f"\nPrimary Type: {interpretation.get('primary_type', {}).get('name', 'N/A')}\n"
        summary += f"Balance: {interpretation.get('balance_analysis', 'N/A')}\n"
        
        return summary

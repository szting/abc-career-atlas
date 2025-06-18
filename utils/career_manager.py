import json
import os
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import streamlit as st
import pandas as pd
from .data_manager import DataManager
from .ai_manager import AIManager
from .assessment_manager import AssessmentManager

class CareerManager:
    """Manages career exploration, matching, and recommendations"""
    
    def __init__(self):
        self.data_manager = DataManager()
        self.ai_manager = AIManager()
        self.assessment_manager = AssessmentManager()
        self.careers_data = self._load_careers_data()
        self.skills_data = self._load_skills_data()
        
    def _load_careers_data(self) -> pd.DataFrame:
        """Load careers database"""
        careers_path = os.path.join('data', 'careers', 'careers_database.json')
        try:
            with open(careers_path, 'r') as f:
                data = json.load(f)
                return pd.DataFrame(data.get('careers', []))
        except Exception as e:
            st.error(f"Error loading careers data: {str(e)}")
            return pd.DataFrame()
    
    def _load_skills_data(self) -> pd.DataFrame:
        """Load skills database"""
        skills_path = os.path.join('data', 'skills', 'skills_database.json')
        try:
            with open(skills_path, 'r') as f:
                data = json.load(f)
                return pd.DataFrame(data.get('skills', []))
        except Exception as e:
            st.error(f"Error loading skills data: {str(e)}")
            return pd.DataFrame()
    
    def get_career_by_id(self, career_id: str) -> Optional[Dict]:
        """Get career details by ID"""
        if self.careers_data.empty:
            return None
        
        career = self.careers_data[self.careers_data['id'] == career_id]
        if not career.empty:
            return career.iloc[0].to_dict()
        return None
    
    def search_careers(self, query: str, filters: Dict = None) -> pd.DataFrame:
        """
        Search careers by keyword and filters
        
        Args:
            query: Search query string
            filters: Dict with optional filters:
                - holland_codes: List of Holland codes
                - education_level: Minimum education level
                - salary_range: Tuple of (min, max) salary
                - growth_outlook: Minimum growth percentage
                - categories: List of career categories
        """
        if self.careers_data.empty:
            return pd.DataFrame()
        
        results = self.careers_data.copy()
        
        # Text search across multiple fields
        if query:
            query_lower = query.lower()
            mask = (
                results['title'].str.lower().str.contains(query_lower, na=False) |
                results['description'].str.lower().str.contains(query_lower, na=False) |
                results['category'].str.lower().str.contains(query_lower, na=False)
            )
            results = results[mask]
        
        # Apply filters
        if filters:
            # Holland code filter
            if filters.get('holland_codes'):
                mask = results['holland_codes'].apply(
                    lambda x: any(code in x for code in filters['holland_codes'])
                )
                results = results[mask]
            
            # Education level filter
            if filters.get('education_level'):
                education_levels = ['high_school', 'associate', 'bachelor', 'master', 'doctoral']
                min_level_index = education_levels.index(filters['education_level'])
                results = results[
                    results['education_level'].apply(
                        lambda x: education_levels.index(x) >= min_level_index
                    )
                ]
            
            # Salary range filter
            if filters.get('salary_range'):
                min_sal, max_sal = filters['salary_range']
                results = results[
                    (results['salary_range_min'] >= min_sal) &
                    (results['salary_range_max'] <= max_sal)
                ]
            
            # Growth outlook filter
            if filters.get('growth_outlook'):
                results = results[results['growth_outlook'] >= filters['growth_outlook']]
            
            # Category filter
            if filters.get('categories'):
                results = results[results['category'].isin(filters['categories'])]
        
        return results
    
    def match_careers_to_assessment(self, assessment_data: Dict, top_n: int = 10) -> List[Dict]:
        """
        Match careers based on RIASEC assessment results
        
        Args:
            assessment_data: Assessment results with scores and interpretation
            top_n: Number of top careers to return
            
        Returns:
            List of career matches with match scores
        """
        if self.careers_data.empty:
            return []
        
        holland_code = assessment_data.get('interpretation', {}).get('holland_code', '')
        scores = assessment_data.get('scores', {})
        
        # Calculate match scores for each career
        career_matches = []
        
        for _, career in self.careers_data.iterrows():
            match_score = self._calculate_career_match_score(
                career['holland_codes'],
                holland_code,
                scores
            )
            
            career_dict = career.to_dict()
            career_dict['match_score'] = match_score
            career_dict['match_reasons'] = self._get_match_reasons(
                career['holland_codes'],
                holland_code,
                match_score
            )
            
            career_matches.append(career_dict)
        
        # Sort by match score and return top N
        career_matches.sort(key=lambda x: x['match_score'], reverse=True)
        
        return career_matches[:top_n]
    
    def _calculate_career_match_score(self, career_codes: List[str], 
                                    user_code: str, user_scores: Dict[str, float]) -> float:
        """Calculate match score between career and user profile"""
        if not career_codes or not user_code:
            return 0.0
        
        # Primary code match (40% weight)
        primary_match = 40.0 if user_code[0] in career_codes[0] else 0.0
        
        # Secondary codes match (30% weight)
        secondary_match = 0.0
        if len(user_code) > 1 and len(career_codes) > 0:
            for i, code in enumerate(user_code[1:3]):
                if code in ''.join(career_codes):
                    secondary_match += 15.0 / (i + 1)
        
        # Overall profile similarity (30% weight)
        code_to_type = {
            'R': 'Realistic', 'I': 'Investigative', 'A': 'Artistic',
            'S': 'Social', 'E': 'Enterprising', 'C': 'Conventional'
        }
        
        profile_similarity = 0.0
        for code in ''.join(career_codes):
            if code in code_to_type:
                type_name = code_to_type[code]
                if type_name in user_scores:
                    profile_similarity += user_scores[type_name] / 100 * 10
        
        total_score = primary_match + secondary_match + profile_similarity
        return min(100.0, total_score)
    
    def _get_match_reasons(self, career_codes: List[str], user_code: str, 
                          match_score: float) -> List[str]:
        """Generate reasons for career match"""
        reasons = []
        
        if match_score >= 80:
            reasons.append("Excellent match with your personality profile")
        elif match_score >= 60:
            reasons.append("Strong alignment with your interests")
        elif match_score >= 40:
            reasons.append("Good compatibility with your preferences")
        
        # Specific code matches
        if user_code[0] in career_codes[0]:
            reasons.append(f"Primary type match ({user_code[0]})")
        
        if len(user_code) > 1:
            secondary_matches = [c for c in user_code[1:3] if c in ''.join(career_codes)]
            if secondary_matches:
                reasons.append(f"Secondary type alignment ({', '.join(secondary_matches)})")
        
        return reasons
    
    def get_career_recommendations(self, user_id: str, 
                                 include_ai: bool = True) -> Dict[str, any]:
        """
        Get comprehensive career recommendations for a user
        
        Returns dict with:
        - matched_careers: List of career matches
        - ai_recommendations: AI-generated insights (if enabled)
        - skill_gaps: Identified skill gaps
        - development_paths: Suggested development paths
        - related_resources: Learning resources
        """
        # Get latest assessment
        assessments = self.data_manager.load_user_assessments(user_id)
        if not assessments:
            return {
                'error': 'No assessment found',
                'message': 'Please complete an assessment first'
            }
        
        latest_assessment = assessments[0]  # Assuming sorted by date
        
        # Get career matches
        matched_careers = self.match_careers_to_assessment(latest_assessment, top_n=10)
        
        # Get AI recommendations if enabled
        ai_recommendations = None
        if include_ai and matched_careers:
            top_careers = [c['title'] for c in matched_careers[:5]]
            ai_recommendations = self.ai_manager.get_career_recommendations(
                latest_assessment,
                top_careers
            )
        
        # Analyze skill gaps for top careers
        skill_gaps = self._analyze_skill_gaps(user_id, matched_careers[:3])
        
        # Generate development paths
        development_paths = self._generate_development_paths(
            matched_careers[:3],
            skill_gaps
        )
        
        # Get related resources
        related_resources = self._get_related_resources(matched_careers[:3])
        
        return {
            'matched_careers': matched_careers,
            'ai_recommendations': ai_recommendations,
            'skill_gaps': skill_gaps,
            'development_paths': development_paths,
            'related_resources': related_resources,
            'assessment_summary': {
                'holland_code': latest_assessment.get('interpretation', {}).get('holland_code'),
                'primary_type': latest_assessment.get('interpretation', {}).get('primary_type', {}).get('name'),
                'assessment_date': latest_assessment.get('timestamp')
            }
        }
    
    def _analyze_skill_gaps(self, user_id: str, target_careers: List[Dict]) -> Dict[str, List[Dict]]:
        """Analyze skill gaps between user profile and target careers"""
        skill_gaps = {}
        
        # Get user's current skills (from profile or assessments)
        user_profile = self.data_manager.load_user_profile(user_id)
        user_skills = set(user_profile.get('skills', []))
        
        for career in target_careers:
            career_id = career['id']
            required_skills = set(career.get('required_skills', []))
            
            # Identify missing skills
            missing_skills = required_skills - user_skills
            
            # Categorize skills by priority
            skill_gap_details = []
            for skill in missing_skills:
                skill_info = self._get_skill_info(skill)
                skill_gap_details.append({
                    'skill': skill,
                    'category': skill_info.get('category', 'General'),
                    'difficulty': skill_info.get('difficulty', 'Medium'),
                    'time_to_learn': skill_info.get('time_to_learn', '3-6 months'),
                    'importance': 'High' if skill in career.get('core_skills', []) else 'Medium'
                })
            
            skill_gaps[career['title']] = sorted(
                skill_gap_details,
                key=lambda x: (x['importance'] == 'High', x['difficulty']),
                reverse=True
            )
        
        return skill_gaps
    
    def _get_skill_info(self, skill_name: str) -> Dict:
        """Get detailed information about a skill"""
        if self.skills_data.empty:
            return {'name': skill_name}
        
        skill = self.skills_data[self.skills_data['name'] == skill_name]
        if not skill.empty:
            return skill.iloc[0].to_dict()
        
        # Default skill info if not found
        return {
            'name': skill_name,
            'category': 'General',
            'difficulty': 'Medium',
            'time_to_learn': '3-6 months'
        }
    
    def _generate_development_paths(self, target_careers: List[Dict], 
                                  skill_gaps: Dict[str, List[Dict]]) -> List[Dict]:
        """Generate development paths for career transitions"""
        development_paths = []
        
        for career in target_careers:
            career_title = career['title']
            gaps = skill_gaps.get(career_title, [])
            
            # Group skills by category and difficulty
            skill_groups = {}
            for gap in gaps:
                key = (gap['category'], gap['difficulty'])
                if key not in skill_groups:
                    skill_groups[key] = []
                skill_groups[key].append(gap)
            
            # Create phased learning path
            phases = []
            phase_num = 1
            
            # Phase 1: High importance, lower difficulty
            phase1_skills = [g for g in gaps if g['importance'] == 'High' and g['difficulty'] in ['Easy', 'Medium']]
            if phase1_skills:
                phases.append({
                    'phase': phase_num,
                    'title': 'Foundation Skills',
                    'duration': '3-6 months',
                    'skills': phase1_skills[:5],
                    'focus': 'Build essential skills for immediate impact'
                })
                phase_num += 1
            
            # Phase 2: High importance, higher difficulty
            phase2_skills = [g for g in gaps if g['importance'] == 'High' and g['difficulty'] == 'Hard']
            if phase2_skills:
                phases.append({
                    'phase': phase_num,
                    'title': 'Advanced Core Skills',
                    'duration': '6-12 months',
                    'skills': phase2_skills[:5],
                    'focus': 'Master complex skills critical to the role'
                })
                phase_num += 1
            
            # Phase 3: Medium importance skills
            phase3_skills = [g for g in gaps if g['importance'] == 'Medium']
            if phase3_skills:
                phases.append({
                    'phase': phase_num,
                    'title': 'Complementary Skills',
                    'duration': '3-6 months',
                    'skills': phase3_skills[:5],
                    'focus': 'Round out your skill set for career advancement'
                })
            
            development_paths.append({
                'career': career_title,
                'career_id': career['id'],
                'total_duration': f"{len(phases) * 6}-{len(phases) * 12} months",
                'phases': phases,
                'entry_options': self._get_entry_options(career),
                'success_factors': [
                    'Consistent daily practice',
                    'Real-world project application',
                    'Networking in the field',
                    'Continuous learning mindset'
                ]
            })
        
        return development_paths
    
    def _get_entry_options(self, career: Dict) -> List[Dict]:
        """Get different entry options for a career"""
        education_level = career.get('education_level', 'bachelor')
        
        options = []
        
        # Traditional education path
        if education_level in ['bachelor', 'master', 'doctoral']:
            options.append({
                'type': 'Traditional Education',
                'description': f"Complete {education_level}'s degree in related field",
                'duration': '2-6 years',
                'pros': ['Comprehensive knowledge', 'Networking opportunities', 'Credentials'],
                'cons': ['Time intensive', 'Costly', 'May include irrelevant coursework']
            })
        
        # Bootcamp/Certification path
        if career.get('certifications_available', True):
            options.append({
                'type': 'Bootcamp/Certification',
                'description': 'Intensive training programs and industry certifications',
                'duration': '3-12 months',
                'pros': ['Focused learning', 'Practical skills', 'Faster entry'],
                'cons': ['Intensive pace', 'Limited depth', 'Requires self-discipline']
            })
        
        # Self-directed learning
        options.append({
            'type': 'Self-Directed Learning',
            'description': 'Online courses, tutorials, and personal projects',
            'duration': '6-18 months',
            'pros': ['Flexible schedule', 'Cost-effective', 'Learn at your pace'],
            'cons': ['Requires discipline', 'No formal credentials', 'Limited networking']
        })
        
        # Apprenticeship/Internship
        if career.get('apprenticeships_common', False):
            options.append({
                'type': 'Apprenticeship/Internship',
                'description': 'Learn while working under experienced professionals',
                'duration': '6-24 months',
                'pros': ['Paid learning', 'Real experience', 'Mentorship'],
                'cons': ['Competitive entry', 'Lower initial pay', 'Limited positions']
            })
        
        return options
    
    def _get_related_resources(self, careers: List[Dict]) -> Dict[str, List[Dict]]:
        """Get learning resources related to careers"""
        resources = {
            'courses': [],
            'books': [],
            'websites': [],
            'communities': []
        }
        
        # Aggregate unique skills from all careers
        all_skills = set()
        for career in careers:
            all_skills.update(career.get('required_skills', []))
        
        # Get resources for top skills (this would normally query a resources database)
        # For now, return curated recommendations
        resources['courses'] = [
            {
                'title': 'Introduction to Data Science',
                'platform': 'Coursera',
                'duration': '4 months',
                'level': 'Beginner',
                'skills': ['Python', 'Statistics', 'Data Analysis']
            },
            {
                'title': 'Full Stack Web Development',
                'platform': 'Udemy',
                'duration': '6 months',
                'level': 'Intermediate',
                'skills': ['JavaScript', 'React', 'Node.js']
            }
        ]
        
        resources['books'] = [
            {
                'title': 'The Pragmatic Programmer',
                'author': 'David Thomas, Andrew Hunt',
                'topics': ['Software Development', 'Best Practices']
            },
            {
                'title': 'Designing Your Life',
                'author': 'Bill Burnett, Dave Evans',
                'topics': ['Career Planning', 'Life Design']
            }
        ]
        
        resources['websites'] = [
            {
                'name': 'Stack Overflow',
                'url': 'stackoverflow.com',
                'description': 'Q&A for programmers'
            },
            {
                'name': 'LinkedIn Learning',
                'url': 'linkedin.com/learning',
                'description': 'Professional skills courses'
            }
        ]
        
        resources['communities'] = [
            {
                'name': 'Reddit Career Guidance',
                'platform': 'Reddit',
                'members': '500k+',
                'focus': 'Career advice and discussions'
            },
            {
                'name': 'Dev.to',
                'platform': 'Web',
                'members': '1M+',
                'focus': 'Developer community and learning'
            }
        ]
        
        return resources
    
    def track_career_interest(self, user_id: str, career_id: str, 
                            action: str = 'view') -> None:
        """Track user's interest in a career"""
        tracking_data = {
            'user_id': user_id,
            'career_id': career_id,
            'action': action,  # view, save, apply, etc.
            'timestamp': datetime.now().isoformat()
        }
        
        # Save to user's career interests
        self.data_manager.save_career_interest(user_id, tracking_data)
    
    def get_career_insights(self, career_id: str) -> Dict[str, any]:
        """Get detailed insights about a specific career"""
        career = self.get_career_by_id(career_id)
        if not career:
            return {'error': 'Career not found'}
        
        # Get related careers
        related_careers = self.search_careers(
            '',
            filters={
                'holland_codes': career['holland_codes'],
                'categories': [career['category']]
            }
        ).head(5).to_dict('records')
        
        # Remove the current career from related
        related_careers = [c for c in related_careers if c['id'] != career_id]
        
        # Get career progression paths
        progression_paths = self._get_career_progression(career)
        
        # Get industry trends (would normally query external data)
        industry_trends = {
            'automation_risk': career.get('automation_risk', 'Medium'),
            'remote_work_compatibility': career.get('remote_friendly', 'Moderate'),
            'emerging_skills': career.get('emerging_skills', []),
            'industry_growth': career.get('industry_growth', 'Stable')
        }
        
        return {
            'career': career,
            'related_careers': related_careers[:4],
            'progression_paths': progression_paths,
            'industry_trends': industry_trends,
            'salary_progression': self._get_salary_progression(career),
            'work_life_balance': career.get('work_life_balance', 'Moderate'),
            'job_satisfaction': career.get('job_satisfaction', 'High')
        }
    
    def _get_career_progression(self, career: Dict) -> List[Dict]:
        """Get potential career progression paths"""
        current_level = career.get('seniority_level', 'mid')
        
        progression = []
        
        if current_level == 'entry':
            progression = [
                {
                    'years': '0-2',
                    'title': career['title'],
                    'focus': 'Learn fundamentals and gain experience'
                },
                {
                    'years': '2-5',
                    'title': f'Senior {career["title"]}',
                    'focus': 'Develop expertise and leadership skills'
                },
                {
                    'years': '5-10',
                    'title': f'{career["title"]} Manager',
                    'focus': 'Lead teams and strategic initiatives'
                }
            ]
        elif current_level == 'mid':
            progression = [
                {
                    'years': '0-3',
                    'title': career['title'],
                    'focus': 'Deepen expertise and expand skills'
                },
                {
                    'years': '3-7',
                    'title': f'Senior {career["title"]}',
                    'focus': 'Mentor others and lead projects'
                },
                {
                    'years': '7-12',
                    'title': f'{career["category"]} Director',
                    'focus': 'Strategic leadership and vision'
                }
            ]
        
        return progression
    
    def _get_salary_progression(self, career: Dict) -> Dict[str, int]:
        """Get salary progression estimates"""
        base_min = career.get('salary_range_min', 50000)
        base_max = career.get('salary_range_max', 80000)
        
        return {
            'entry_level': int(base_min * 0.8),
            'mid_level': int((base_min + base_max) / 2),
            'senior_level': int(base_max * 1.2),
            'leadership_level': int(base_max * 1.5)
        }
    
    def export_career_plan(self, user_id: str, format: str = 'pdf') -> any:
        """Export user's career plan in specified format"""
        recommendations = self.get_career_recommendations(user_id, include_ai=True)
        
        if format == 'json':
            return json.dumps(recommendations, indent=2)
        elif format == 'summary':
            return self._format_career_plan_summary(recommendations)
        else:
            # PDF export would be implemented here
            return recommendations
    
    def _format_career_plan_summary(self, recommendations: Dict) -> str:
        """Format career plan as readable summary"""
        summary = f"""
Career Development Plan
======================
Generated: {datetime.now().strftime('%Y-%m-%d')}
Holland Code: {recommendations['assessment_summary']['holland_code']}
Primary Type: {recommendations['assessment_summary']['primary_type']}

Top Career Matches:
------------------
"""
        for i, career in enumerate(recommendations['matched_careers'][:5], 1):
            summary += f"{i}. {career['title']} (Match: {career['match_score']:.0f}%)\n"
            summary += f"   - {career['description'][:100]}...\n"
            summary += f"   - Salary: ${career['salary_range_min']:,} - ${career['salary_range_max']:,}\n\n"
        
        if recommendations.get('development_paths'):
            summary += "\nRecommended Development Path:\n"
            summary += "-----------------------------\n"
            path = recommendations['development_paths'][0]
            summary += f"Target: {path['career']}\n"
            summary += f"Duration: {path['total_duration']}\n\n"
            
            for phase in path['phases']:
                summary += f"Phase {phase['phase']}: {phase['title']}\n"
                summary += f"Duration: {phase['duration']}\n"
                summary += "Skills to develop:\n"
                for skill in phase['skills'][:3]:
                    summary += f"  - {skill['skill']}\n"
                summary += "\n"
        
        return summary

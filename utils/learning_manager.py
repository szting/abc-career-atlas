import json
import os
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import streamlit as st
import pandas as pd
from .data_manager import DataManager
from .ai_manager import AIManager
from .career_manager import CareerManager

class LearningManager:
    """Manages learning resources, recommendations, and progress tracking"""
    
    def __init__(self):
        self.data_manager = DataManager()
        self.ai_manager = AIManager()
        self.career_manager = CareerManager()
        self.resources_data = self._load_resources_data()
        self.courses_data = self._load_courses_data()
        
    def _load_resources_data(self) -> pd.DataFrame:
        """Load learning resources database"""
        resources_path = os.path.join('data', 'resources', 'learning_resources.json')
        try:
            with open(resources_path, 'r') as f:
                data = json.load(f)
                return pd.DataFrame(data.get('resources', []))
        except Exception as e:
            st.error(f"Error loading resources data: {str(e)}")
            return pd.DataFrame()
    
    def _load_courses_data(self) -> pd.DataFrame:
        """Load courses database"""
        courses_path = os.path.join('data', 'resources', 'courses_database.json')
        try:
            with open(courses_path, 'r') as f:
                data = json.load(f)
                return pd.DataFrame(data.get('courses', []))
        except Exception as e:
            st.error(f"Error loading courses data: {str(e)}")
            return pd.DataFrame()
    
    def get_resource_by_id(self, resource_id: str) -> Optional[Dict]:
        """Get resource details by ID"""
        if self.resources_data.empty:
            return None
        
        resource = self.resources_data[self.resources_data['id'] == resource_id]
        if not resource.empty:
            return resource.iloc[0].to_dict()
        return None
    
    def get_course_by_id(self, course_id: str) -> Optional[Dict]:
        """Get course details by ID"""
        if self.courses_data.empty:
            return None
        
        course = self.courses_data[self.courses_data['id'] == course_id]
        if not course.empty:
            return course.iloc[0].to_dict()
        return None
    
    def search_resources(self, query: str = '', filters: Dict = None) -> pd.DataFrame:
        """
        Search learning resources with filters
        
        Args:
            query: Search query string
            filters: Dict with optional filters:
                - resource_type: List of types (course, book, video, article, etc.)
                - skill_level: List of levels (beginner, intermediate, advanced)
                - skills: List of skills covered
                - format: List of formats (online, offline, hybrid)
                - price_range: Tuple of (min, max) price
                - duration_range: Tuple of (min, max) duration in hours
        """
        if self.resources_data.empty:
            return pd.DataFrame()
        
        results = self.resources_data.copy()
        
        # Text search
        if query:
            query_lower = query.lower()
            mask = (
                results['title'].str.lower().str.contains(query_lower, na=False) |
                results['description'].str.lower().str.contains(query_lower, na=False) |
                results['skills'].apply(lambda x: any(query_lower in s.lower() for s in x))
            )
            results = results[mask]
        
        # Apply filters
        if filters:
            # Resource type filter
            if filters.get('resource_type'):
                results = results[results['type'].isin(filters['resource_type'])]
            
            # Skill level filter
            if filters.get('skill_level'):
                results = results[results['level'].isin(filters['skill_level'])]
            
            # Skills filter
            if filters.get('skills'):
                mask = results['skills'].apply(
                    lambda x: any(skill in x for skill in filters['skills'])
                )
                results = results[mask]
            
            # Format filter
            if filters.get('format'):
                results = results[results['format'].isin(filters['format'])]
            
            # Price range filter
            if filters.get('price_range'):
                min_price, max_price = filters['price_range']
                results = results[
                    (results['price'] >= min_price) & 
                    (results['price'] <= max_price)
                ]
            
            # Duration filter
            if filters.get('duration_range'):
                min_dur, max_dur = filters['duration_range']
                results = results[
                    (results['duration_hours'] >= min_dur) & 
                    (results['duration_hours'] <= max_dur)
                ]
        
        return results
    
    def get_learning_recommendations(self, user_id: str, 
                                   career_goals: List[str] = None,
                                   include_ai: bool = True) -> Dict[str, any]:
        """
        Get personalized learning recommendations
        
        Args:
            user_id: User identifier
            career_goals: List of target career IDs
            include_ai: Whether to include AI-generated insights
            
        Returns:
            Dict with recommended resources, learning paths, and insights
        """
        # Get user profile and assessment
        user_profile = self.data_manager.load_user_profile(user_id)
        assessments = self.data_manager.load_user_assessments(user_id)
        
        # Get skill gaps if career goals provided
        skill_gaps = []
        if career_goals:
            for career_id in career_goals:
                career = self.career_manager.get_career_by_id(career_id)
                if career:
                    gaps = self._analyze_skill_gaps_for_career(
                        user_profile.get('skills', []),
                        career.get('required_skills', [])
                    )
                    skill_gaps.extend(gaps)
        
        # Get recommended resources
        recommended_resources = self._get_recommended_resources(
            user_profile.get('skills', []),
            skill_gaps,
            user_profile.get('learning_style', 'visual'),
            user_profile.get('time_availability', 'moderate')
        )
        
        # Create learning paths
        learning_paths = self._create_learning_paths(
            skill_gaps,
            recommended_resources,
            user_profile.get('time_availability', 'moderate')
        )
        
        # Get AI insights if enabled
        ai_insights = None
        if include_ai and assessments:
            ai_insights = self.ai_manager.get_learning_recommendations(
                assessments[0] if assessments else {},
                skill_gaps[:5],  # Top 5 skill gaps
                user_profile.get('learning_style', 'visual')
            )
        
        # Track learning interests
        self._track_learning_interests(user_id, recommended_resources[:10])
        
        return {
            'recommended_resources': recommended_resources,
            'learning_paths': learning_paths,
            'skill_gaps': skill_gaps,
            'ai_insights': ai_insights,
            'estimated_completion': self._estimate_completion_time(learning_paths),
            'learning_style_match': self._match_learning_style(
                recommended_resources,
                user_profile.get('learning_style', 'visual')
            )
        }
    
    def _analyze_skill_gaps_for_career(self, user_skills: List[str], 
                                     required_skills: List[str]) -> List[Dict]:
        """Analyze skill gaps for a specific career"""
        user_skills_set = set(user_skills)
        gaps = []
        
        for skill in required_skills:
            if skill not in user_skills_set:
                skill_info = self._get_skill_details(skill)
                gaps.append({
                    'skill': skill,
                    'category': skill_info.get('category', 'General'),
                    'difficulty': skill_info.get('difficulty', 'Medium'),
                    'importance': skill_info.get('importance', 'High'),
                    'prerequisites': skill_info.get('prerequisites', [])
                })
        
        return gaps
    
    def _get_skill_details(self, skill_name: str) -> Dict:
        """Get detailed information about a skill"""
        # This would normally query a skills database
        # For now, return structured data
        skill_categories = {
            'Python': {'category': 'Programming', 'difficulty': 'Medium'},
            'Machine Learning': {'category': 'Data Science', 'difficulty': 'Hard'},
            'React': {'category': 'Web Development', 'difficulty': 'Medium'},
            'Leadership': {'category': 'Soft Skills', 'difficulty': 'Hard'},
            'Communication': {'category': 'Soft Skills', 'difficulty': 'Medium'},
            'Data Analysis': {'category': 'Analytics', 'difficulty': 'Medium'},
            'Project Management': {'category': 'Management', 'difficulty': 'Medium'}
        }
        
        return skill_categories.get(skill_name, {
            'category': 'General',
            'difficulty': 'Medium',
            'importance': 'Medium',
            'prerequisites': []
        })
    
    def _get_recommended_resources(self, current_skills: List[str],
                                 skill_gaps: List[Dict],
                                 learning_style: str,
                                 time_availability: str) -> List[Dict]:
        """Get resources matching user's needs and preferences"""
        recommendations = []
        
        # Prioritize resources for skill gaps
        for gap in skill_gaps[:10]:  # Top 10 gaps
            # Search for resources teaching this skill
            resources = self.search_resources(
                gap['skill'],
                filters={
                    'skills': [gap['skill']],
                    'skill_level': self._get_appropriate_level(gap['difficulty'])
                }
            )
            
            # Score and rank resources
            for _, resource in resources.iterrows():
                resource_dict = resource.to_dict()
                score = self._score_resource(
                    resource_dict,
                    learning_style,
                    time_availability,
                    gap['importance']
                )
                resource_dict['relevance_score'] = score
                resource_dict['target_skill'] = gap['skill']
                recommendations.append(resource_dict)
        
        # Sort by relevance score
        recommendations.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        # Remove duplicates
        seen = set()
        unique_recommendations = []
        for rec in recommendations:
            if rec['id'] not in seen:
                seen.add(rec['id'])
                unique_recommendations.append(rec)
        
        return unique_recommendations[:20]  # Top 20 recommendations
    
    def _get_appropriate_level(self, difficulty: str) -> List[str]:
        """Map difficulty to appropriate learning levels"""
        mapping = {
            'Easy': ['beginner'],
            'Medium': ['beginner', 'intermediate'],
            'Hard': ['intermediate', 'advanced']
        }
        return mapping.get(difficulty, ['beginner', 'intermediate'])
    
    def _score_resource(self, resource: Dict, learning_style: str,
                       time_availability: str, importance: str) -> float:
        """Score a resource based on user preferences and needs"""
        score = 50.0  # Base score
        
        # Learning style match
        style_formats = {
            'visual': ['video', 'infographic', 'interactive'],
            'auditory': ['podcast', 'audiobook', 'lecture'],
            'reading': ['book', 'article', 'documentation'],
            'kinesthetic': ['hands-on', 'project', 'workshop']
        }
        
        if resource.get('format') in style_formats.get(learning_style, []):
            score += 20
        
        # Time availability match
        time_duration = {
            'limited': (0, 10),
            'moderate': (5, 50),
            'flexible': (0, 200)
        }
        
        min_hours, max_hours = time_duration.get(time_availability, (0, 50))
        resource_hours = resource.get('duration_hours', 10)
        if min_hours <= resource_hours <= max_hours:
            score += 15
        
        # Importance weighting
        if importance == 'High':
            score += 10
        elif importance == 'Medium':
            score += 5
        
        # Quality indicators
        if resource.get('rating', 0) >= 4.5:
            score += 10
        elif resource.get('rating', 0) >= 4.0:
            score += 5
        
        # Recency bonus
        if resource.get('updated_date'):
            try:
                updated = datetime.fromisoformat(resource['updated_date'])
                if (datetime.now() - updated).days < 180:
                    score += 5
            except:
                pass
        
        # Price consideration
        if resource.get('price', 0) == 0:
            score += 5  # Free resource bonus
        
        return min(100, score)
    
    def _create_learning_paths(self, skill_gaps: List[Dict],
                             resources: List[Dict],
                             time_availability: str) -> List[Dict]:
        """Create structured learning paths"""
        # Group skills by category and prerequisites
        skill_graph = self._build_skill_dependency_graph(skill_gaps)
        
        # Create paths based on dependencies
        paths = []
        
        # Path 1: Foundation Path (prerequisites first)
        foundation_skills = [s for s in skill_gaps if not s.get('prerequisites', [])]
        if foundation_skills:
            foundation_resources = [
                r for r in resources 
                if r.get('target_skill') in [s['skill'] for s in foundation_skills]
            ]
            
            paths.append({
                'name': 'Foundation Skills Path',
                'description': 'Build essential skills with no prerequisites',
                'duration_weeks': self._estimate_duration_weeks(
                    foundation_resources, time_availability
                ),
                'skills': [s['skill'] for s in foundation_skills[:5]],
                'resources': foundation_resources[:10],
                'difficulty': 'Beginner-friendly',
                'outcomes': [
                    'Solid foundation in core concepts',
                    'Preparation for advanced topics',
                    'Immediate practical application'
                ]
            })
        
        # Path 2: Specialized Path (build on foundations)
        specialized_skills = [
            s for s in skill_gaps 
            if s.get('prerequisites', []) and s['importance'] == 'High'
        ]
        if specialized_skills:
            specialized_resources = [
                r for r in resources 
                if r.get('target_skill') in [s['skill'] for s in specialized_skills]
            ]
            
            paths.append({
                'name': 'Specialization Path',
                'description': 'Advanced skills for career specialization',
                'duration_weeks': self._estimate_duration_weeks(
                    specialized_resources, time_availability
                ),
                'skills': [s['skill'] for s in specialized_skills[:5]],
                'resources': specialized_resources[:10],
                'difficulty': 'Intermediate to Advanced',
                'prerequisites': foundation_skills[:3] if foundation_skills else [],
                'outcomes': [
                    'Deep expertise in specialized areas',
                    'Competitive advantage in job market',
                    'Leadership potential in field'
                ]
            })
        
        # Path 3: Quick Wins Path (easy, high-impact skills)
        quick_wins = [
            s for s in skill_gaps 
            if s['difficulty'] == 'Easy' and s['importance'] in ['High', 'Medium']
        ]
        if quick_wins:
            quick_resources = [
                r for r in resources 
                if r.get('target_skill') in [s['skill'] for s in quick_wins]
                and r.get('duration_hours', 0) <= 20
            ]
            
            paths.append({
                'name': 'Quick Wins Path',
                'description': 'High-impact skills you can learn quickly',
                'duration_weeks': 4,
                'skills': [s['skill'] for s in quick_wins[:5]],
                'resources': quick_resources[:8],
                'difficulty': 'Easy',
                'outcomes': [
                    'Immediate resume enhancement',
                    'Quick confidence boost',
                    'Rapid skill acquisition'
                ]
            })
        
        return paths
    
    def _build_skill_dependency_graph(self, skill_gaps: List[Dict]) -> Dict:
        """Build a graph of skill dependencies"""
        graph = {}
        
        for skill in skill_gaps:
            skill_name = skill['skill']
            prerequisites = skill.get('prerequisites', [])
            
            graph[skill_name] = {
                'prerequisites': prerequisites,
                'difficulty': skill['difficulty'],
                'importance': skill['importance']
            }
        
        return graph
    
    def _estimate_duration_weeks(self, resources: List[Dict], 
                               time_availability: str) -> int:
        """Estimate weeks to complete resources based on time availability"""
        total_hours = sum(r.get('duration_hours', 10) for r in resources)
        
        # Hours per week based on availability
        hours_per_week = {
            'limited': 5,
            'moderate': 10,
            'flexible': 20
        }
        
        weekly_hours = hours_per_week.get(time_availability, 10)
        weeks = int(total_hours / weekly_hours)
        
        return max(1, weeks)
    
    def _estimate_completion_time(self, learning_paths: List[Dict]) -> Dict:
        """Estimate overall completion time for all paths"""
        if not learning_paths:
            return {'weeks': 0, 'months': 0}
        
        # Assume paths can be partially parallelized
        total_weeks = sum(p.get('duration_weeks', 0) for p in learning_paths)
        parallel_factor = 0.7  # 30% time savings from parallelization
        
        adjusted_weeks = int(total_weeks * parallel_factor)
        
        return {
            'weeks': adjusted_weeks,
            'months': round(adjusted_weeks / 4.33, 1),
            'dedication_required': self._get_dedication_level(adjusted_weeks)
        }
    
    def _get_dedication_level(self, weeks: int) -> str:
        """Determine dedication level required"""
        if weeks <= 12:
            return 'Moderate - achievable with consistent effort'
        elif weeks <= 26:
            return 'Significant - requires strong commitment'
        else:
            return 'Intensive - long-term dedication needed'
    
    def _match_learning_style(self, resources: List[Dict], 
                            learning_style: str) -> Dict:
        """Analyze how well resources match learning style"""
        style_formats = {
            'visual': ['video', 'infographic', 'interactive'],
            'auditory': ['podcast', 'audiobook', 'lecture'],
            'reading': ['book', 'article', 'documentation'],
            'kinesthetic': ['hands-on', 'project', 'workshop']
        }
        
        preferred_formats = style_formats.get(learning_style, [])
        
        matching_count = sum(
            1 for r in resources 
            if r.get('format') in preferred_formats
        )
        
        match_percentage = (matching_count / len(resources) * 100) if resources else 0
        
        return {
            'style': learning_style,
            'match_percentage': round(match_percentage, 1),
            'matching_resources': matching_count,
            'total_resources': len(resources),
            'recommendation': self._get_style_recommendation(match_percentage)
        }
    
    def _get_style_recommendation(self, match_percentage: float) -> str:
        """Get recommendation based on learning style match"""
        if match_percentage >= 70:
            return 'Excellent match - resources align well with your learning style'
        elif match_percentage >= 50:
            return 'Good match - mix of preferred and alternative formats'
        elif match_percentage >= 30:
            return 'Moderate match - consider supplementing with preferred formats'
        else:
            return 'Low match - actively seek resources in your preferred format'
    
    def track_learning_progress(self, user_id: str, resource_id: str,
                              progress: Dict) -> None:
        """
        Track user's progress on a learning resource
        
        Args:
            user_id: User identifier
            resource_id: Resource identifier
            progress: Dict with progress details:
                - status: started, in_progress, completed
                - percentage: 0-100
                - time_spent_hours: float
                - notes: str
        """
        progress_data = {
            'user_id': user_id,
            'resource_id': resource_id,
            'status': progress.get('status', 'started'),
            'percentage': progress.get('percentage', 0),
            'time_spent_hours': progress.get('time_spent_hours', 0),
            'notes': progress.get('notes', ''),
            'last_updated': datetime.now().isoformat(),
            'started_date': progress.get('started_date', datetime.now().isoformat())
        }
        
        # Calculate completion date if completed
        if progress_data['status'] == 'completed':
            progress_data['completed_date'] = datetime.now().isoformat()
        
        # Save progress
        self.data_manager.save_learning_progress(user_id, progress_data)
        
        # Update user's skill profile if completed
        if progress_data['status'] == 'completed':
            resource = self.get_resource_by_id(resource_id)
            if resource:
                self._update_user_skills(user_id, resource.get('skills', []))
    
    def _update_user_skills(self, user_id: str, new_skills: List[str]) -> None:
        """Update user's skill profile with newly acquired skills"""
        user_profile = self.data_manager.load_user_profile(user_id)
        current_skills = set(user_profile.get('skills', []))
        
        # Add new skills
        updated_skills = list(current_skills.union(set(new_skills)))
        
        # Update profile
        user_profile['skills'] = updated_skills
        user_profile['last_skill_update'] = datetime.now().isoformat()
        
        self.data_manager.save_user_profile(user_id, user_profile)
    
    def get_learning_dashboard(self, user_id: str) -> Dict:
        """Get comprehensive learning dashboard data"""
        # Load user's learning history
        learning_history = self.data_manager.load_learning_history(user_id)
        
        # Calculate statistics
        stats = self._calculate_learning_stats(learning_history)
        
        # Get current learning paths
        current_paths = [
            item for item in learning_history 
            if item.get('status') in ['started', 'in_progress']
        ]
        
        # Get completed resources
        completed = [
            item for item in learning_history 
            if item.get('status') == 'completed'
        ]
        
        # Get recommendations
        recommendations = self.get_learning_recommendations(
            user_id, 
            include_ai=False
        )
        
        return {
            'statistics': stats,
            'current_learning': current_paths[:5],
            'completed_resources': completed[:10],
            'recommended_next': recommendations['recommended_resources'][:5],
            'learning_streak': self._calculate_learning_streak(learning_history),
            'skills_acquired': self._get_acquired_skills(completed),
            'time_investment': self._calculate_time_investment(learning_history)
        }
    
    def _calculate_learning_stats(self, history: List[Dict]) -> Dict:
        """Calculate learning statistics"""
        total_resources = len(history)
        completed = len([h for h in history if h.get('status') == 'completed'])
        in_progress = len([h for h in history if h.get('status') == 'in_progress'])
        
        total_hours = sum(h.get('time_spent_hours', 0) for h in history)
        
        # Calculate completion rate
        completion_rate = (completed / total_resources * 100) if total_resources > 0 else 0
        
        return {
            'total_resources_started': total_resources,
            'completed_resources': completed,
            'in_progress_resources': in_progress,
            'completion_rate': round(completion_rate, 1),
            'total_learning_hours': round(total_hours, 1),
            'average_hours_per_resource': round(total_hours / completed, 1) if completed > 0 else 0
        }
    
    def _calculate_learning_streak(self, history: List[Dict]) -> Dict:
        """Calculate current learning streak"""
        if not history:
            return {'current_streak': 0, 'longest_streak': 0}
        
        # Sort by date
        sorted_history = sorted(
            history,
            key=lambda x: x.get('last_updated', ''),
            reverse=True
        )
        
        # Calculate current streak
        current_streak = 0
        today = datetime.now().date()
        
        for item in sorted_history:
            try:
                item_date = datetime.fromisoformat(
                    item.get('last_updated', '')
                ).date()
                
                if (today - item_date).days <= current_streak + 1:
                    current_streak = (today - item_date).days
                else:
                    break
            except:
                continue
        
        return {
            'current_streak': current_streak,
            'longest_streak': current_streak,  # Would need more logic for historical
            'last_activity': sorted_history[0].get('last_updated') if sorted_history else None
        }
    
    def _get_acquired_skills(self, completed_resources: List[Dict]) -> List[str]:
        """Get list of skills acquired from completed resources"""
        skills = set()
        
        for item in completed_resources:
            resource = self.get_resource_by_id(item.get('resource_id'))
            if resource:
                skills.update(resource.get('skills', []))
        
        return list(skills)
    
    def _calculate_time_investment(self, history: List[Dict]) -> Dict:
        """Calculate time investment analysis"""
        total_hours = sum(h.get('time_spent_hours', 0) for h in history)
        
        # Group by month
        monthly_hours = {}
        for item in history:
            try:
                date = datetime.fromisoformat(item.get('last_updated', ''))
                month_key = date.strftime('%Y-%m')
                monthly_hours[month_key] = monthly_hours.get(month_key, 0) + \
                                         item.get('time_spent_hours', 0)
            except:
                continue
        
        # Calculate average
        avg_monthly = sum(monthly_hours.values()) / len(monthly_hours) if monthly_hours else 0
        
        return {
            'total_hours': round(total_hours, 1),
            'monthly_average': round(avg_monthly, 1),
            'weekly_average': round(avg_monthly / 4.33, 1),
            'daily_average': round(avg_monthly / 30, 1)
        }
    
    def _track_learning_interests(self, user_id: str, resources: List[Dict]) -> None:
        """Track user's learning interests for better recommendations"""
        interests = {
            'user_id': user_id,
            'timestamp': datetime.now().isoformat(),
            'interested_skills': list(set(
                skill for r in resources 
                for skill in r.get('skills', [])
            )),
            'preferred_formats': list(set(
                r.get('format') for r in resources 
                if r.get('format')
            )),
            'average_duration': sum(
                r.get('duration_hours', 0) for r in resources
            ) / len(resources) if resources else 0
        }
        
        self.data_manager.save_learning_interests(user_id, interests)
    
    def export_learning_plan(self, user_id: str, format: str = 'pdf') -> any:
        """Export user's learning plan"""
        dashboard = self.get_learning_dashboard(user_id)
        recommendations = self.get_learning_recommendations(user_id)
        
        if format == 'json':
            return json.dumps({
                'dashboard': dashboard,
                'recommendations': recommendations
            }, indent=2)
        elif format == 'summary':
            return self._format_learning_plan_summary(dashboard, recommendations)
        else:
            # PDF export would be implemented here
            return {'dashboard': dashboard, 'recommendations': recommendations}
    
    def _format_learning_plan_summary(self, dashboard: Dict, 
                                    recommendations: Dict) -> str:
        """Format learning plan as readable summary"""
        summary = f"""
Personal Learning Plan
=====================
Generated: {datetime.now().strftime('%Y-%m-%d')}

Learning Statistics:
-------------------
Total Resources Started: {dashboard['statistics']['total_resources_started']}
Completed: {dashboard['statistics']['completed_resources']}
Completion Rate: {dashboard['statistics']['completion_rate']}%
Total Learning Hours: {dashboard['statistics']['total_learning_hours']}

Current Progress:
----------------
"""
        
        for item in dashboard['current_learning'][:3]:
            summary += f"- {item.get('resource_id', 'Unknown')} ({item.get('percentage', 0)}%)\n"
        
        summary += "\nRecommended Learning Paths:\n"
        summary += "---------------------------\n"
        
        for path in recommendations.get('learning_paths', [])[:2]:
            summary += f"\n{path['name']}\n"
            summary += f"Duration: {path['duration_weeks']} weeks\n"
            summary += f"Skills: {', '.join(path['skills'][:3])}\n"
            summary += f"Difficulty: {path['difficulty']}\n"
        
        return summary

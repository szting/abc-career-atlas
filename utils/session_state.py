"""
Session State Manager for Career Atlas

This module manages the application's session state, providing a centralized
way to handle user data, navigation, and temporary state across pages.
"""

import streamlit as st
from typing import Any, Dict, Optional, List
from datetime import datetime
import json


class SessionStateManager:
    """Manages Streamlit session state for the Career Atlas application"""
    
    # Define default values for session state
    DEFAULTS = {
        # Authentication
        'authenticated': False,
        'user_id': None,
        'username': None,
        'role': None,
        'name': None,
        
        # Navigation
        'current_page': 'welcome',
        'previous_page': None,
        'persona': None,  # 'individual', 'coach', 'manager'
        
        # Assessment state
        'assessment_in_progress': False,
        'current_assessment': None,  # 'riasec', 'skills', 'values'
        'assessment_responses': {},
        'assessment_start_time': None,
        'assessment_progress': 0,
        
        # Results
        'assessment_complete': False,
        'riasec_scores': None,
        'skills_scores': None,
        'values_rankings': None,
        'career_recommendations': None,
        'learning_recommendations': None,
        
        # Temporary data
        'selected_career': None,
        'selected_resource': None,
        'search_query': '',
        'filter_settings': {},
        'view_mode': 'grid',  # 'grid' or 'list'
        
        # User preferences
        'theme': 'light',
        'notifications_enabled': True,
        'auto_save': True,
        
        # Cache flags
        'data_loaded': False,
        'recommendations_cached': False,
        'last_sync': None
    }
    
    @classmethod
    def initialize(cls) -> None:
        """Initialize session state with default values"""
        for key, default_value in cls.DEFAULTS.items():
            if key not in st.session_state:
                st.session_state[key] = default_value
    
    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        """
        Get a value from session state
        
        Args:
            key: The key to retrieve
            default: Default value if key doesn't exist
            
        Returns:
            The value from session state or default
        """
        return st.session_state.get(key, default)
    
    @classmethod
    def set(cls, key: str, value: Any) -> None:
        """
        Set a value in session state
        
        Args:
            key: The key to set
            value: The value to store
        """
        st.session_state[key] = value
    
    @classmethod
    def update(cls, updates: Dict[str, Any]) -> None:
        """
        Update multiple values in session state
        
        Args:
            updates: Dictionary of key-value pairs to update
        """
        for key, value in updates.items():
            st.session_state[key] = value
    
    @classmethod
    def clear(cls, keys: Optional[List[str]] = None) -> None:
        """
        Clear specific keys or all session state
        
        Args:
            keys: List of keys to clear. If None, clears all except auth
        """
        if keys:
            for key in keys:
                if key in st.session_state:
                    del st.session_state[key]
        else:
            # Clear all except authentication
            auth_keys = ['authenticated', 'user_id', 'username', 'role', 'name']
            keys_to_clear = [k for k in st.session_state.keys() if k not in auth_keys]
            for key in keys_to_clear:
                del st.session_state[key]
    
    @classmethod
    def reset_assessment(cls) -> None:
        """Reset all assessment-related state"""
        assessment_keys = [
            'assessment_in_progress',
            'current_assessment',
            'assessment_responses',
            'assessment_start_time',
            'assessment_progress',
            'assessment_complete',
            'riasec_scores',
            'skills_scores',
            'values_rankings'
        ]
        cls.clear(assessment_keys)
        cls.set('assessment_responses', {})
    
    @classmethod
    def navigate_to(cls, page: str) -> None:
        """
        Navigate to a specific page
        
        Args:
            page: The page to navigate to
        """
        cls.set('previous_page', cls.get('current_page'))
        cls.set('current_page', page)
        st.rerun()
    
    @classmethod
    def go_back(cls) -> None:
        """Navigate to the previous page"""
        previous = cls.get('previous_page')
        if previous:
            cls.navigate_to(previous)
    
    @classmethod
    def is_authenticated(cls) -> bool:
        """Check if user is authenticated"""
        return cls.get('authenticated', False)
    
    @classmethod
    def is_admin(cls) -> bool:
        """Check if user has admin role"""
        return cls.get('role') == 'admin'
    
    @classmethod
    def get_user_info(cls) -> Dict[str, Any]:
        """Get current user information"""
        return {
            'user_id': cls.get('user_id'),
            'username': cls.get('username'),
            'name': cls.get('name'),
            'role': cls.get('role')
        }
    
    @classmethod
    def set_user_info(cls, user_info: Dict[str, Any]) -> None:
        """Set user information after login"""
        cls.update({
            'authenticated': True,
            'user_id': user_info.get('user_id'),
            'username': user_info.get('username'),
            'name': user_info.get('name'),
            'role': user_info.get('role')
        })
    
    @classmethod
    def logout(cls) -> None:
        """Clear session state on logout"""
        # Clear everything
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        # Re-initialize with defaults
        cls.initialize()
    
    @classmethod
    def save_assessment_response(cls, assessment_type: str, question_id: str, response: Any) -> None:
        """
        Save a response to an assessment question
        
        Args:
            assessment_type: Type of assessment ('riasec', 'skills', 'values')
            question_id: Unique identifier for the question
            response: The user's response
        """
        responses = cls.get('assessment_responses', {})
        if assessment_type not in responses:
            responses[assessment_type] = {}
        responses[assessment_type][question_id] = response
        cls.set('assessment_responses', responses)
    
    @classmethod
    def get_assessment_responses(cls, assessment_type: str) -> Dict[str, Any]:
        """
        Get all responses for a specific assessment
        
        Args:
            assessment_type: Type of assessment
            
        Returns:
            Dictionary of responses
        """
        responses = cls.get('assessment_responses', {})
        return responses.get(assessment_type, {})
    
    @classmethod
    def calculate_assessment_progress(cls, assessment_type: str, total_questions: int) -> float:
        """
        Calculate progress for an assessment
        
        Args:
            assessment_type: Type of assessment
            total_questions: Total number of questions
            
        Returns:
            Progress percentage (0-100)
        """
        responses = cls.get_assessment_responses(assessment_type)
        answered = len(responses)
        return (answered / total_questions * 100) if total_questions > 0 else 0
    
    @classmethod
    def cache_recommendations(cls, career_recs: List[Dict], learning_recs: List[Dict]) -> None:
        """Cache recommendations to avoid repeated API calls"""
        cls.set('career_recommendations', career_recs)
        cls.set('learning_recommendations', learning_recs)
        cls.set('recommendations_cached', True)
        cls.set('last_sync', datetime.now().isoformat())
    
    @classmethod
    def get_cached_recommendations(cls) -> Optional[Dict[str, List[Dict]]]:
        """Get cached recommendations if available"""
        if cls.get('recommendations_cached', False):
            return {
                'careers': cls.get('career_recommendations', []),
                'learning': cls.get('learning_recommendations', [])
            }
        return None
    
    @classmethod
    def set_filter(cls, filter_type: str, value: Any) -> None:
        """Set a filter value"""
        filters = cls.get('filter_settings', {})
        filters[filter_type] = value
        cls.set('filter_settings', filters)
    
    @classmethod
    def get_filter(cls, filter_type: str, default: Any = None) -> Any:
        """Get a filter value"""
        filters = cls.get('filter_settings', {})
        return filters.get(filter_type, default)
    
    @classmethod
    def clear_filters(cls) -> None:
        """Clear all filters"""
        cls.set('filter_settings', {})
    
    @classmethod
    def export_state(cls) -> Dict[str, Any]:
        """
        Export current session state (excluding sensitive data)
        
        Returns:
            Dictionary of session state
        """
        exclude_keys = ['authenticated', 'password']
        state = {}
        for key, value in st.session_state.items():
            if key not in exclude_keys:
                # Convert non-serializable objects to strings
                try:
                    json.dumps(value)
                    state[key] = value
                except:
                    state[key] = str(value)
        return state
    
    @classmethod
    def import_state(cls, state: Dict[str, Any]) -> None:
        """
        Import session state from a dictionary
        
        Args:
            state: Dictionary of state to import
        """
        # Don't import authentication-related keys
        exclude_keys = ['authenticated', 'user_id', 'username', 'role']
        for key, value in state.items():
            if key not in exclude_keys:
                st.session_state[key] = value
    
    @classmethod
    def debug_state(cls) -> None:
        """Display current session state for debugging"""
        st.write("### Current Session State")
        state_dict = {}
        for key, value in sorted(st.session_state.items()):
            # Truncate long values for display
            if isinstance(value, (dict, list)) and len(str(value)) > 100:
                state_dict[key] = f"{type(value).__name__} (length: {len(value)})"
            else:
                state_dict[key] = value
        st.json(state_dict)


# Convenience functions for common operations
def init_session_state():
    """Initialize session state"""
    SessionStateManager.initialize()


def get_state(key: str, default: Any = None) -> Any:
    """Get a value from session state"""
    return SessionStateManager.get(key, default)


def set_state(key: str, value: Any) -> None:
    """Set a value in session state"""
    SessionStateManager.set(key, value)


def update_state(updates: Dict[str, Any]) -> None:
    """Update multiple values in session state"""
    SessionStateManager.update(updates)


def navigate_to(page: str) -> None:
    """Navigate to a page"""
    SessionStateManager.navigate_to(page)


def is_authenticated() -> bool:
    """Check if user is authenticated"""
    return SessionStateManager.is_authenticated()


def is_admin() -> bool:
    """Check if user is admin"""
    return SessionStateManager.is_admin()

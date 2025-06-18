# Simple hardcoded authentication manager
import streamlit as st

class AuthManager:
    """Simple authentication with hardcoded credentials"""
    
    # Hardcoded credentials - change these in production!
    USERS = {
        'admin': {
            'password': 'admin123',
            'name': 'Admin User',
            'role': 'admin',
            'email': 'admin@careeratllas.com'
        },
        'demo': {
            'password': 'demo123',
            'name': 'Demo User',
            'role': 'user',
            'email': 'demo@careeratllas.com'
        }
    }
    
    @staticmethod
    def login(username: str, password: str) -> dict:
        """Authenticate user and return user info if successful"""
        if username in AuthManager.USERS:
            user = AuthManager.USERS[username]
            if user['password'] == password:
                return {
                    'username': username,
                    'name': user['name'],
                    'role': user['role'],
                    'email': user['email'],
                    'authenticated': True
                }
        return {'authenticated': False}
    
    @staticmethod
    def logout():
        """Clear authentication from session state"""
        keys_to_clear = ['authenticated', 'username', 'name', 'role', 'email']
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
    
    @staticmethod
    def is_authenticated() -> bool:
        """Check if user is authenticated"""
        return st.session_state.get('authenticated', False)
    
    @staticmethod
    def is_admin() -> bool:
        """Check if current user is admin"""
        return (st.session_state.get('authenticated', False) and 
                st.session_state.get('role') == 'admin')
    
    @staticmethod
    def get_current_user() -> dict:
        """Get current user info"""
        if AuthManager.is_authenticated():
            return {
                'username': st.session_state.get('username'),
                'name': st.session_state.get('name'),
                'role': st.session_state.get('role'),
                'email': st.session_state.get('email')
            }
        return None
    
    @staticmethod
    def require_auth():
        """Decorator to require authentication for a page"""
        if not AuthManager.is_authenticated():
            st.error("Please login to access this page")
            st.stop()
    
    @staticmethod
    def require_admin():
        """Decorator to require admin role for a page"""
        if not AuthManager.is_admin():
            st.error("Admin access required")
            st.stop()

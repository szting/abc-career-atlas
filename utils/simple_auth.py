# This file now redirects to the new auth_manager
# Kept for backward compatibility with existing pages

from utils.auth_manager import AuthManager

def check_password():
    """Legacy function - redirects to AuthManager"""
    return AuthManager.is_authenticated()

def login(username, password):
    """Legacy function - redirects to AuthManager"""
    return AuthManager.login(username, password)

def logout():
    """Legacy function - redirects to AuthManager"""
    return AuthManager.logout()

def get_user_info():
    """Legacy function - redirects to AuthManager"""
    return AuthManager.get_current_user()

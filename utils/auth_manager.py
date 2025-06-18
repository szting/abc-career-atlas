import streamlit as st
import bcrypt
import json
import os
from datetime import datetime
from pathlib import Path

class AuthManager:
    def __init__(self):
        self.users_file = Path("data/users.json")
        self.ensure_data_directory()
        self.load_users()
    
    def ensure_data_directory(self):
        """Ensure data directory exists"""
        self.users_file.parent.mkdir(exist_ok=True)
        
        # Create default admin user if no users exist
        if not self.users_file.exists():
            default_users = {
                "admin": {
                    "name": "Administrator",
                    "email": "admin@careeratllas.com",
                    "password": self.hash_password("admin123"),
                    "created_at": datetime.now().isoformat(),
                    "role": "admin"
                }
            }
            self.save_users(default_users)
    
    def load_users(self):
        """Load users from file"""
        if self.users_file.exists():
            with open(self.users_file, 'r') as f:
                self.users = json.load(f)
        else:
            self.users = {}
    
    def save_users(self, users=None):
        """Save users to file"""
        if users is None:
            users = self.users
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=2)
    
    def hash_password(self, password):
        """Hash password using bcrypt"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def verify_password(self, password, hashed):
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    def authenticate(self, username, password):
        """Authenticate user"""
        if username in self.users:
            return self.verify_password(password, self.users[username]['password'])
        return False
    
    def register_user(self, username, password, name, email):
        """Register new user"""
        if username in self.users:
            return False
        
        self.users[username] = {
            "name": name,
            "email": email,
            "password": self.hash_password(password),
            "created_at": datetime.now().isoformat(),
            "role": "user"
        }
        self.save_users()
        return True
    
    def get_user_name(self, username):
        """Get user's display name"""
        return self.users.get(username, {}).get('name', username)
    
    def logout(self):
        """Logout user"""
        st.session_state.authentication_status = None
        st.session_state.username = None
        st.session_state.name = None

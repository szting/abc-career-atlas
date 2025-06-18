import streamlit as st
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import bcrypt

class AuthManager:
    def __init__(self, config_file='config.yaml'):
        self.config_file = config_file
        self.load_config()
    
    def load_config(self):
        """Load authentication configuration from YAML file"""
        try:
            with open(self.config_file) as file:
                self.config = yaml.load(file, Loader=SafeLoader)
        except FileNotFoundError:
            # Create default config if not exists
            self.create_default_config()
    
    def create_default_config(self):
        """Create a default configuration file"""
        default_config = {
            'credentials': {
                'usernames': {
                    'admin': {
                        'email': 'admin@example.com',
                        'name': 'Admin User',
                        'password': self.hash_password('admin123')
                    },
                    'demo': {
                        'email': 'demo@example.com',
                        'name': 'Demo User',
                        'password': self.hash_password('demo123')
                    }
                }
            },
            'cookie': {
                'name': 'career_atlas_cookie',
                'key': 'random_signature_key',
                'expiry_days': 30
            },
            'preauthorized': {
                'emails': []
            }
        }
        
        with open(self.config_file, 'w') as file:
            yaml.dump(default_config, file)
        
        self.config = default_config
    
    def hash_password(self, password):
        """Hash a password using bcrypt"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def add_user(self, username, name, email, password):
        """Add a new user to the configuration"""
        hashed_password = self.hash_password(password)
        
        self.config['credentials']['usernames'][username] = {
            'email': email,
            'name': name,
            'password': hashed_password
        }
        
        self.save_config()
    
    def remove_user(self, username):
        """Remove a user from the configuration"""
        if username in self.config['credentials']['usernames']:
            del self.config['credentials']['usernames'][username]
            self.save_config()
            return True
        return False
    
    def update_user(self, username, **kwargs):
        """Update user information"""
        if username in self.config['credentials']['usernames']:
            for key, value in kwargs.items():
                if key == 'password':
                    value = self.hash_password(value)
                self.config['credentials']['usernames'][username][key] = value
            self.save_config()
            return True
        return False
    
    def save_config(self):
        """Save configuration to YAML file"""
        with open(self.config_file, 'w') as file:
            yaml.dump(self.config, file)
    
    def get_authenticator(self):
        """Get configured authenticator instance"""
        return stauth.Authenticate(
            self.config['credentials'],
            self.config['cookie']['name'],
            self.config['cookie']['key'],
            self.config['cookie']['expiry_days'],
            self.config['preauthorized']
        )
    
    def verify_user(self, username, password):
        """Verify user credentials"""
        if username in self.config['credentials']['usernames']:
            stored_password = self.config['credentials']['usernames'][username]['password']
            return bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8'))
        return False
    
    def get_user_info(self, username):
        """Get user information"""
        if username in self.config['credentials']['usernames']:
            return self.config['credentials']['usernames'][username]
        return None
    
    def list_users(self):
        """List all registered users"""
        return list(self.config['credentials']['usernames'].keys())

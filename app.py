import streamlit as st
import streamlit_authenticator as stauth
from datetime import datetime
import yaml
from yaml.loader import SafeLoader
import os
from dotenv import load_dotenv
import json
from pathlib import Path

# Import custom modules
from utils.auth_manager import AuthManager
from utils.google_drive import GoogleDriveManager
from utils.llm_manager import LLMManager
from utils.data_manager import DataManager
from pages.welcome import show_welcome_page
from pages.assessment import show_assessment_page
from pages.results import show_results_page
from pages.coaching import show_coaching_page
from pages.analytics import show_analytics_page
from pages.settings import show_settings_page
from pages.admin import show_admin_page

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Career Atlas - AI-Powered Career Assessment",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/yourusername/career-atlas',
        'Report a bug': "https://github.com/yourusername/career-atlas/issues",
        'About': "Career Atlas - Your AI-powered career guidance companion"
    }
)

# Initialize session state
def init_session_state():
    if 'authentication_status' not in st.session_state:
        st.session_state.authentication_status = None
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'name' not in st.session_state:
        st.session_state.name = None
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {}
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'welcome'
    if 'selected_persona' not in st.session_state:
        st.session_state.selected_persona = None
    if 'assessment_data' not in st.session_state:
        st.session_state.assessment_data = {}
    if 'llm_provider' not in st.session_state:
        st.session_state.llm_provider = 'openai'
    if 'custom_frameworks' not in st.session_state:
        st.session_state.custom_frameworks = {}

# Custom CSS for better mobile responsiveness and PWA
def load_custom_css():
    st.markdown("""
    <style>
    /* PWA-ready responsive design */
    @media (max-width: 768px) {
        .stSidebar {
            margin-left: -21rem;
        }
        .block-container {
            padding: 1rem;
        }
    }
    
    /* Custom theme colors */
    :root {
        --primary-color: #4F46E5;
        --secondary-color: #7C3AED;
        --success-color: #10B981;
        --warning-color: #F59E0B;
        --error-color: #EF4444;
    }
    
    /* Improved button styling */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 0.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    /* Card styling */
    .assessment-card {
        background: white;
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    
    .assessment-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 20px rgba(0,0,0,0.15);
    }
    
    /* Progress bar */
    .progress-bar {
        height: 8px;
        background: #E5E7EB;
        border-radius: 4px;
        overflow: hidden;
        margin: 1rem 0;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        transition: width 0.5s ease;
    }
    </style>
    """, unsafe_allow_html=True)

# PWA manifest injection
def inject_pwa_manifest():
    st.markdown("""
    <link rel="manifest" href="/manifest.json">
    <meta name="theme-color" content="#4F46E5">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black">
    <meta name="apple-mobile-web-app-title" content="Career Atlas">
    <link rel="apple-touch-icon" href="/icon-192.png">
    """, unsafe_allow_html=True)

# Main app logic
def main():
    init_session_state()
    load_custom_css()
    inject_pwa_manifest()
    
    # Initialize managers
    auth_manager = AuthManager()
    drive_manager = GoogleDriveManager()
    llm_manager = LLMManager()
    data_manager = DataManager(drive_manager)
    
    # Authentication
    if st.session_state.authentication_status is None:
        show_login_page(auth_manager)
    elif st.session_state.authentication_status == False:
        st.error('Username/password is incorrect')
        show_login_page(auth_manager)
    elif st.session_state.authentication_status == True:
        show_authenticated_app(auth_manager, drive_manager, llm_manager, data_manager)

def show_login_page(auth_manager):
    st.title("🧭 Career Atlas")
    st.subheader("Your AI-Powered Career Guidance Companion")
    
    tab1, tab2, tab3 = st.tabs(["Login", "Register", "Google Sign-In"])
    
    with tab1:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")
            
            if submit:
                if auth_manager.authenticate(username, password):
                    st.session_state.authentication_status = True
                    st.session_state.username = username
                    st.session_state.name = auth_manager.get_user_name(username)
                    st.rerun()
                else:
                    st.error("Invalid username or password")
    
    with tab2:
        with st.form("register_form"):
            new_name = st.text_input("Full Name")
            new_username = st.text_input("Username")
            new_email = st.text_input("Email")
            new_password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            register = st.form_submit_button("Register")
            
            if register:
                if new_password != confirm_password:
                    st.error("Passwords do not match")
                elif auth_manager.register_user(new_username, new_password, new_name, new_email):
                    st.success("Registration successful! Please login.")
                else:
                    st.error("Username already exists")
    
    with tab3:
        st.info("Google Sign-In coming soon!")
        if st.button("Sign in with Google", disabled=True):
            # TODO: Implement Google OAuth
            pass

def show_authenticated_app(auth_manager, drive_manager, llm_manager, data_manager):
    # Sidebar navigation
    with st.sidebar:
        st.title(f"Welcome, {st.session_state.name}!")
        
        # Navigation menu
        st.subheader("Navigation")
        pages = {
            "🏠 Home": "welcome",
            "📋 Assessment": "assessment",
            "📊 Results": "results",
            "🤝 Coaching": "coaching",
            "📈 Analytics": "analytics",
            "⚙️ Settings": "settings"
        }
        
        # Add admin page for admin users
        if st.session_state.username == "admin":
            pages["🔧 Admin Panel"] = "admin"
        
        for page_name, page_key in pages.items():
            if st.button(page_name, key=f"nav_{page_key}"):
                st.session_state.current_page = page_key
        
        st.divider()
        
        # Persona selection
        st.subheader("Select Persona")
        persona = st.radio(
            "Choose your role:",
            ["Individual", "Coach", "Manager"],
            key="persona_selector"
        )
        st.session_state.selected_persona = persona
        
        st.divider()
        
        # Logout button
        if st.button("🚪 Logout"):
            auth_manager.logout()
            for key in st.session_state.keys():
                del st.session_state[key]
            st.rerun()
    
    # Main content area
    if st.session_state.current_page == "welcome":
        show_welcome_page()
    elif st.session_state.current_page == "assessment":
        show_assessment_page(data_manager)
    elif st.session_state.current_page == "results":
        show_results_page(data_manager)
    elif st.session_state.current_page == "coaching":
        show_coaching_page(llm_manager, data_manager)
    elif st.session_state.current_page == "analytics":
        show_analytics_page(data_manager)
    elif st.session_state.current_page == "settings":
        show_settings_page(llm_manager)
    elif st.session_state.current_page == "admin":
        show_admin_page(data_manager)

if __name__ == "__main__":
    main()

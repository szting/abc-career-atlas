"""
Career Atlas - AI-Powered Career Guidance Platform
Main application entry point
"""

import streamlit as st
from utils.session_state import SessionStateManager
from utils.auth_manager import AuthManager
import os
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Career Atlas - AI Career Guidance",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
SessionStateManager.initialize()

# Custom CSS for better styling
st.markdown("""
<style>
    /* Main container styling */
    .main {
        padding: 0rem 1rem;
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        height: 3rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    /* Card styling */
    .card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
    }
    
    /* Header styling */
    h1 {
        color: #1e3a8a;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    h2 {
        color: #3730a3;
        font-weight: 600;
    }
    
    h3 {
        color: #4c1d95;
        font-weight: 500;
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div > div {
        background-color: #3b82f6;
    }
    
    /* Info box styling */
    .stInfo {
        background-color: #eff6ff;
        border: 1px solid #3b82f6;
    }
    
    /* Success box styling */
    .stSuccess {
        background-color: #f0fdf4;
        border: 1px solid #22c55e;
    }
    
    /* Warning box styling */
    .stWarning {
        background-color: #fffbeb;
        border: 1px solid #f59e0b;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

def show_login_page():
    """Display the login page"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<h1 style='text-align: center;'>🧭 Career Atlas</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #6b7280; font-size: 1.1rem;'>Your AI-Powered Career Guidance Platform</p>", unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Login form
        with st.form("login_form"):
            st.markdown("### Sign In")
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            col1, col2 = st.columns(2)
            with col1:
                login_button = st.form_submit_button("Sign In", use_container_width=True, type="primary")
            with col2:
                demo_button = st.form_submit_button("Try Demo", use_container_width=True)
            
            if login_button:
                if username and password:
                    if AuthManager.login(username, password):
                        st.success("Login successful! Redirecting...")
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
                else:
                    st.warning("Please enter both username and password")
            
            if demo_button:
                if AuthManager.login("demo", "demo123"):
                    st.success("Logged in as demo user! Redirecting...")
                    st.rerun()
        
        # Info box
        st.markdown("<br>", unsafe_allow_html=True)
        st.info("""
        **Demo Credentials:**
        - Username: `demo` | Password: `demo123`
        - Username: `admin` | Password: `admin123`
        """)
        
        # Features section
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 🌟 Key Features")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class='card'>
                <h4>🎯 RIASEC Assessment</h4>
                <p>Discover your Holland Code through our comprehensive personality assessment</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class='card'>
                <h4>💼 Career Matching</h4>
                <p>Get AI-powered career recommendations tailored to your unique profile</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class='card'>
                <h4>📚 Learning Paths</h4>
                <p>Receive personalized learning recommendations to achieve your career goals</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class='card'>
                <h4>📊 Progress Tracking</h4>
                <p>Monitor your development journey with detailed analytics and insights</p>
            </div>
            """, unsafe_allow_html=True)

def show_main_app():
    """Display the main application based on current page"""
    current_page = SessionStateManager.get('current_page', 'welcome')
    
    # Create a header with user info and logout
    col1, col2, col3 = st.columns([6, 2, 1])
    with col1:
        user_info = SessionStateManager.get_user_info()
        st.markdown(f"### Welcome, {user_info.get('name', user_info.get('username', 'User'))}! 👋")
    
    with col3:
        if st.button("Logout", type="secondary"):
            AuthManager.logout()
            st.rerun()
    
    st.markdown("---")
    
    # Dynamic page loading
    try:
        if current_page == 'welcome':
            from pages.welcome import show_welcome
            show_welcome()
        elif current_page == 'persona_selection':
            from pages.persona_selection import show_persona_selection
            show_persona_selection()
        elif current_page == 'riasec_assessment':
            from pages.riasec_assessment import show_riasec_assessment
            show_riasec_assessment()
        elif current_page == 'skills_assessment':
            from pages.skills_assessment import show_skills_assessment
            show_skills_assessment()
        elif current_page == 'values_assessment':
            from pages.values_assessment import show_values_assessment
            show_values_assessment()
        elif current_page == 'results':
            from pages.results import show_results
            show_results()
        elif current_page == 'coaching_dashboard':
            from pages.coaching_dashboard import show_coaching_dashboard
            show_coaching_dashboard()
        elif current_page == 'manager_dashboard':
            from pages.manager_dashboard import show_manager_dashboard
            show_manager_dashboard()
        elif current_page == 'admin_panel':
            from pages.admin_panel import show_admin_panel
            show_admin_panel()
        else:
            st.error(f"Page '{current_page}' not found")
            if st.button("Go to Welcome"):
                SessionStateManager.navigate_to('welcome')
    except ImportError as e:
        st.error(f"Page module not found: {e}")
        st.info("This page is under development. Please check back later.")
        if st.button("Go to Welcome"):
            SessionStateManager.navigate_to('welcome')
    except Exception as e:
        st.error(f"An error occurred: {e}")
        if st.button("Go to Welcome"):
            SessionStateManager.navigate_to('welcome')

def main():
    """Main application entry point"""
    # Check authentication
    if not SessionStateManager.is_authenticated():
        show_login_page()
    else:
        show_main_app()

if __name__ == "__main__":
    # Ensure data directories exist
    data_dirs = [
        "data/users/profiles",
        "data/users/assessments", 
        "data/users/progress"
    ]
    
    for dir_path in data_dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    # Run the app
    main()

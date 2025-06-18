import streamlit as st
from utils.session_state import SessionStateManager
from utils.auth_manager import AuthManager

def show_welcome():
    """Display the welcome page after login"""
    # Get user info
    user_info = SessionStateManager.get_user_info()
    
    # Welcome header
    st.markdown(f"# Welcome to Career Atlas, {user_info.get('name', 'Explorer')}! 🧭")
    st.markdown("Your personalized AI-powered career guidance journey starts here.")
    
    # Quick stats if user has previous assessments
    if SessionStateManager.get('assessment_complete', False):
        st.markdown("### 📊 Your Progress")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Assessments Completed", "1", "RIASEC")
        with col2:
            holland_code = st.session_state.get('holland_code', 'N/A')
            st.metric("Holland Code", holland_code)
        with col3:
            st.metric("Career Matches", "10+", "Personalized")
        with col4:
            st.metric("Profile Strength", "85%", "+15%")
    
    # Main navigation options
    st.markdown("### 🚀 What would you like to do today?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎯 Career Discovery")
        if st.button("Start RIASEC Assessment", use_container_width=True, type="primary"):
            SessionStateManager.navigate_to('riasec_assessment')
        
        if st.button("Explore Careers", use_container_width=True):
            st.info("Career exploration coming soon!")
        
        if st.button("Skills Assessment", use_container_width=True):
            SessionStateManager.navigate_to('skills_assessment')
        
        if st.button("Values Assessment", use_container_width=True):
            SessionStateManager.navigate_to('values_assessment')
    
    with col2:
        st.markdown("#### 📈 Your Journey")
        if SessionStateManager.get('assessment_complete', False):
            if st.button("View Results", use_container_width=True, type="primary"):
                SessionStateManager.navigate_to('results')
            
            if st.button("Compare RIASEC vs Skills", use_container_width=True):
                SessionStateManager.navigate_to('comparison_view')
        else:
            st.info("Complete assessments to unlock results")
        
        if st.button("Learning Resources", use_container_width=True):
            st.info("Learning resources coming soon!")
        
        if st.button("Career Coaching", use_container_width=True):
            SessionStateManager.set('persona', 'coach')
            SessionStateManager.navigate_to('coaching_dashboard')
    
    # Role-based options
    if SessionStateManager.is_admin():
        st.markdown("### 🔧 Admin Tools")
        if st.button("Admin Panel", use_container_width=True):
            SessionStateManager.navigate_to('admin_panel')
    
    # Quick tips
    st.markdown("### 💡 Quick Tips")
    tips = [
        "Complete the RIASEC assessment to discover careers that match your personality",
        "Regular skills assessments help track your professional growth",
        "Use the comparison view to identify skill gaps and opportunities",
        "Career coaching provides personalized guidance for your journey"
    ]
    
    tip_index = hash(user_info.get('username', '')) % len(tips)
    st.info(tips[tip_index])
    
    # Recent activity (if any)
    if SessionStateManager.get('last_activity'):
        st.markdown("### 📅 Recent Activity")
        st.write(f"Last active: {SessionStateManager.get('last_activity')}")

"""
Persona Selection Page for Career Atlas
Allows users to choose their role: Individual, Coach, or Manager
"""

import streamlit as st
from utils.session_state import SessionStateManager
from utils.data_manager import DataManager
from datetime import datetime

def show_persona_selection():
    """Display the persona selection page"""
    
    # Header
    st.markdown("# 🎭 Choose Your Path")
    st.markdown("Select how you'd like to use Career Atlas today")
    
    st.markdown("---")
    
    # Create three columns for the personas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Individual Path
        st.markdown("""
        <div style='background-color: #e0f2fe; padding: 2rem; border-radius: 12px; height: 100%; text-align: center;'>
            <h2 style='color: #0369a1; margin-bottom: 1rem;'>👤 Individual</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### For Career Seekers")
        
        st.markdown("""
        Perfect if you want to:
        - Discover your RIASEC personality type
        - Explore career matches
        - Get personalized learning paths
        - Track your development progress
        """)
        
        with st.expander("What You'll Do"):
            st.markdown("""
            1. **Take Assessments** - Complete RIASEC, skills, and values assessments
            2. **Get Insights** - Receive your personality profile and career matches
            3. **Plan Development** - Access personalized learning recommendations
            4. **Track Progress** - Monitor your skill growth over time
            """)
        
        if st.button("🚀 Start Individual Journey", use_container_width=True, type="primary"):
            SessionStateManager.set('persona', 'individual')
            SessionStateManager.set('assessment_in_progress', True)
            SessionStateManager.navigate_to('riasec_assessment')
    
    with col2:
        # Coach Path
        st.markdown("""
        <div style='background-color: #fef3c7; padding: 2rem; border-radius: 12px; height: 100%; text-align: center;'>
            <h2 style='color: #d97706; margin-bottom: 1rem;'>👥 Career Coach</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### For Career Professionals")
        
        st.markdown("""
        Perfect if you want to:
        - Access coaching conversation guides
        - View client assessment insights
        - Get RIASEC-based coaching tips
        - Track client progress
        """)
        
        with st.expander("What You'll Access"):
            st.markdown("""
            1. **Coaching Questions** - RIASEC-specific conversation starters
            2. **Client Insights** - Understanding personality types
            3. **Development Guides** - Career path recommendations
            4. **Progress Tracking** - Monitor client journeys
            """)
        
        if st.button("📋 Access Coach Dashboard", use_container_width=True):
            SessionStateManager.set('persona', 'coach')
            SessionStateManager.navigate_to('coaching_dashboard')
    
    with col3:
        # Manager Path
        st.markdown("""
        <div style='background-color: #ede9fe; padding: 2rem; border-radius: 12px; height: 100%; text-align: center;'>
            <h2 style='color: #7c3aed; margin-bottom: 1rem;'>💼 Manager</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### For Team Leaders")
        
        st.markdown("""
        Perfect if you want to:
        - Understand team dynamics
        - Plan development initiatives
        - Support career conversations
        - Build stronger teams
        """)
        
        with st.expander("What You'll Discover"):
            st.markdown("""
            1. **Team Insights** - Collective strengths and interests
            2. **Development Planning** - Targeted skill building
            3. **1-on-1 Guides** - Career conversation starters
            4. **Succession Planning** - Internal talent matching
            """)
        
        if st.button("👔 Open Manager Dashboard", use_container_width=True):
            SessionStateManager.set('persona', 'manager')
            SessionStateManager.navigate_to('manager_dashboard')
    
    st.markdown("---")
    
    # Additional information section
    st.markdown("## 💡 Not Sure Which Path to Choose?")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Quick Guide:
        
        - **Choose Individual** if you're exploring your own career path, looking for a job change, 
          or wanting to understand your professional identity better.
        
        - **Choose Career Coach** if you're a professional helping others with career decisions, 
          whether as a counselor, HR professional, or mentor.
        
        - **Choose Manager** if you lead a team and want to better understand and develop your 
          team members' careers.
        """)
        
        st.info("""
        💡 **Tip**: You can always return to this page later to explore different paths. 
        Your progress in one area won't affect the others.
        """)
    
    with col2:
        st.markdown("### 🔄 Switch Anytime")
        st.markdown("""
        You're not locked into one path! Feel free to:
        - Complete individual assessments first
        - Then explore coaching resources
        - Or check manager insights
        
        Each path offers unique value.
        """)
    
    # Quick stats if user has previous data
    user_info = SessionStateManager.get_user_info()
    username = user_info.get('username')
    
    if username:
        data_manager = DataManager()
        profile = data_manager.load_user_profile(username)
        
        if profile:
            st.markdown("---")
            st.markdown("### 📊 Your Activity Summary")
            
            col1, col2, col3, col4 = st.columns(4)
            
            # Load various data
            assessments = data_manager.load_user_assessments(username)
            learning_history = data_manager.load_learning_history(username)
            
            with col1:
                assessment_count = len(assessments) if assessments else 0
                st.metric("Assessments", assessment_count)
            
            with col2:
                learning_count = len(learning_history) if learning_history else 0
                st.metric("Learning Activities", learning_count)
            
            with col3:
                # Calculate days since joining
                created_at = profile.get('created_at')
                if created_at:
                    created_date = datetime.fromisoformat(created_at)
                    days_active = (datetime.now() - created_date).days
                    st.metric("Days Active", days_active)
            
            with col4:
                # Show primary RIASEC type if available
                if assessments:
                    latest_assessment = assessments[0]
                    scores = latest_assessment.get('riasec_scores', {})
                    if scores:
                        top_type = max(scores.items(), key=lambda x: x[1])[0]
                        st.metric("Primary Type", top_type[0])  # First letter only
    
    # Footer navigation
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("← Back to Welcome", use_container_width=True):
            SessionStateManager.navigate_to('welcome')
    
    with col3:
        # Admin quick access
        if SessionStateManager.is_admin():
            if st.button("🔧 Admin Panel →", use_container_width=True):
                SessionStateManager.navigate_to('admin_panel')
    
    # Save persona selection timestamp
    if 'persona_selected_at' not in st.session_state:
        st.session_state.persona_selected_at = datetime.now().isoformat()

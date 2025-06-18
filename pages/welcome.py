import streamlit as st
from datetime import datetime

def show_welcome_page():
    """Display the welcome/home page"""
    
    # Hero section
    st.markdown("""
    <div style='text-align: center; padding: 2rem 0;'>
        <h1 style='font-size: 3rem; background: linear-gradient(135deg, #4F46E5, #7C3AED); 
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
            🧭 Career Atlas
        </h1>
        <p style='font-size: 1.5rem; color: #6B7280; margin-top: 1rem;'>
            Your AI-Powered Career Guidance Companion
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Active Persona", st.session_state.get('selected_persona', 'Individual'))
    
    with col2:
        assessments_completed = len(st.session_state.get('assessment_data', {}))
        st.metric("Assessments Completed", f"{assessments_completed}/3")
    
    with col3:
        last_login = st.session_state.get('last_login', datetime.now())
        st.metric("Last Activity", "Today")
    
    st.divider()
    
    # Persona-specific content
    persona = st.session_state.get('selected_persona', 'Individual')
    
    if persona == 'Individual':
        show_individual_welcome()
    elif persona == 'Coach':
        show_coach_welcome()
    elif persona == 'Manager':
        show_manager_welcome()

def show_individual_welcome():
    """Welcome content for Individual persona"""
    st.header("🎯 Your Career Journey Starts Here")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📋 Complete Your Assessments
        
        Discover your career personality, skills, and values through our comprehensive assessments:
        
        - **RIASEC Assessment**: Uncover your Holland Code
        - **Skills Confidence**: Evaluate your strengths
        - **Work Values**: Identify what matters most
        """)
        
        if st.button("Start Assessment", key="start_assessment_home"):
            st.session_state.current_page = "assessment"
            st.rerun()
    
    with col2:
        st.markdown("""
        ### 🎨 Your Career Profile
        
        Build a comprehensive understanding of:
        
        - Your personality type
        - Natural strengths and interests
        - Ideal work environments
        - Career paths that align with you
        """)
        
        if st.button("View Results", key="view_results_home"):
            st.session_state.current_page = "results"
            st.rerun()
    
    # Progress tracker
    st.subheader("📊 Your Progress")
    progress_data = {
        "RIASEC Assessment": st.session_state.get('assessment_data', {}).get('riasec', {}).get('completed', False),
        "Skills Assessment": st.session_state.get('assessment_data', {}).get('skills', {}).get('completed', False),
        "Values Assessment": st.session_state.get('assessment_data', {}).get('values', {}).get('completed', False)
    }
    
    for assessment, completed in progress_data.items():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(assessment)
        with col2:
            if completed:
                st.success("✅ Complete")
            else:
                st.info("⏳ Pending")

def show_coach_welcome():
    """Welcome content for Coach persona"""
    st.header("🤝 Coach Dashboard")
    
    st.markdown("""
    ### Welcome to Your Coaching Toolkit
    
    As a career coach, you have access to:
    
    - **AI-Powered Insights**: Get intelligent coaching suggestions
    - **Client Assessments**: Review and interpret results
    - **Coaching Questions**: Access our curated question bank
    - **Progress Tracking**: Monitor client development
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("**Active Clients**\n\n12")
    
    with col2:
        st.success("**Sessions Today**\n\n3")
    
    with col3:
        st.warning("**Pending Reviews**\n\n5")
    
    if st.button("Go to Coaching Hub", key="coaching_hub"):
        st.session_state.current_page = "coaching"
        st.rerun()

def show_manager_welcome():
    """Welcome content for Manager persona"""
    st.header("👔 Manager Dashboard")
    
    st.markdown("""
    ### Team Development Overview
    
    As a manager, leverage Career Atlas to:
    
    - **Team Analytics**: Understand team strengths and gaps
    - **Succession Planning**: Identify high-potential employees
    - **Development Plans**: Create targeted growth paths
    - **Team Composition**: Build balanced, effective teams
    """)
    
    # Team overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Team Members", "24")
    
    with col2:
        st.metric("Assessments Complete", "18/24")
    
    with col3:
        st.metric("Avg Team Score", "78%")
    
    with col4:
        st.metric("Development Plans", "12")
    
    if st.button("View Team Analytics", key="team_analytics"):
        st.session_state.current_page = "analytics"
        st.rerun()

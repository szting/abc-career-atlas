"""
Welcome Page for Career Atlas
First page users see after login
"""

import streamlit as st
from utils.session_state import SessionStateManager
from utils.data_manager import DataManager
from datetime import datetime

def show_welcome():
    """Display the welcome page"""
    
    # Get user info
    user_info = SessionStateManager.get_user_info()
    username = user_info.get('username', 'User')
    
    # Initialize data manager
    data_manager = DataManager()
    
    # Load user profile to check if returning user
    profile = data_manager.load_user_profile(username)
    is_returning_user = profile is not None
    
    # Header
    st.markdown("# 🧭 Welcome to Career Atlas")
    
    if is_returning_user:
        st.markdown(f"### Great to see you again, {user_info.get('name', username)}!")
        
        # Show progress summary if they have assessments
        assessments = data_manager.load_user_assessments(username)
        if assessments:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Assessments Completed", len(assessments))
            with col2:
                # Get latest assessment date
                latest_date = max(a.get('timestamp', '') for a in assessments)
                if latest_date:
                    date_obj = datetime.fromisoformat(latest_date)
                    days_ago = (datetime.now() - date_obj).days
                    st.metric("Last Assessment", f"{days_ago} days ago")
            with col3:
                # Check learning progress
                progress = data_manager.load_learning_history(username)
                st.metric("Learning Activities", len(progress) if progress else 0)
    else:
        st.markdown(f"### Welcome aboard, {user_info.get('name', username)}!")
        st.markdown("Let's begin your career discovery journey.")
    
    st.markdown("---")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("## 🎯 Your Career Journey Starts Here")
        
        st.markdown("""
        Career Atlas uses scientifically-proven assessments and AI technology to help you:
        
        - **Discover** your unique personality profile through the RIASEC assessment
        - **Explore** careers that match your interests, skills, and values
        - **Learn** with personalized recommendations tailored to your goals
        - **Grow** by tracking your progress and skill development
        """)
        
        # Call to action based on user status
        st.markdown("### 🚀 Ready to Get Started?")
        
        if is_returning_user and assessments:
            st.info("📊 You have completed assessments. You can view your results or retake assessments to track changes.")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("View My Results", type="primary", use_container_width=True):
                    SessionStateManager.navigate_to('results')
            with col2:
                if st.button("Retake Assessments", use_container_width=True):
                    SessionStateManager.navigate_to('persona_selection')
            with col3:
                if st.button("Explore Careers", use_container_width=True):
                    SessionStateManager.set('explore_mode', True)
                    SessionStateManager.navigate_to('results')
        else:
            st.success("🎉 Let's discover your ideal career path! Choose how you'd like to proceed:")
            
            if st.button("Start My Journey", type="primary", use_container_width=True):
                SessionStateManager.navigate_to('persona_selection')
    
    with col2:
        # Quick tips sidebar
        st.markdown("### 💡 Quick Tips")
        
        with st.container():
            st.markdown("""
            <div style='background-color: #f0f2f6; padding: 1rem; border-radius: 8px;'>
            
            **For Best Results:**
            
            🎯 **Be Honest**  
            Answer based on your true preferences, not what you think is "right"
            
            ⏱️ **Take Your Time**  
            Most users complete all assessments in 20-30 minutes
            
            🔄 **Stay Open**  
            You might discover careers you haven't considered before
            
            📈 **Track Progress**  
            Return regularly to update your skills and explore new paths
            
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Feature highlights
    st.markdown("## 🌟 What Makes Career Atlas Special")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🧬 Scientific Foundation
        Based on the RIASEC model developed by Dr. John Holland, used by career counselors worldwide.
        """)
    
    with col2:
        st.markdown("""
        ### 🤖 AI-Powered Insights
        Advanced AI analyzes your profile to provide personalized career and learning recommendations.
        """)
    
    with col3:
        st.markdown("""
        ### 📊 Comprehensive Analysis
        Goes beyond simple matching to consider skills, values, and market trends.
        """)
    
    # Different paths section
    st.markdown("---")
    st.markdown("## 🛤️ Choose Your Path")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 👤 Individual
        - Take comprehensive assessments
        - Get personalized career matches
        - Receive learning recommendations
        - Track your progress
        """)
        if st.button("Individual Path", use_container_width=True):
            SessionStateManager.set('persona', 'individual')
            SessionStateManager.navigate_to('riasec_assessment')
    
    with col2:
        st.markdown("""
        ### 👥 Career Coach
        - Access coaching resources
        - View client insights
        - Get conversation starters
        - Track client progress
        """)
        if st.button("Coach Dashboard", use_container_width=True):
            SessionStateManager.set('persona', 'coach')
            SessionStateManager.navigate_to('coaching_dashboard')
    
    with col3:
        st.markdown("""
        ### 💼 Manager
        - Understand team dynamics
        - Identify development needs
        - Plan succession strategies
        - Support team growth
        """)
        if st.button("Manager Dashboard", use_container_width=True):
            SessionStateManager.set('persona', 'manager')
            SessionStateManager.navigate_to('manager_dashboard')
    
    # Admin panel access for admin users
    if SessionStateManager.is_admin():
        st.markdown("---")
        st.markdown("### 🔧 Administrator Access")
        if st.button("Open Admin Panel", use_container_width=True):
            SessionStateManager.navigate_to('admin_panel')
    
    # Footer with helpful information
    st.markdown("---")
    
    with st.expander("❓ Frequently Asked Questions"):
        st.markdown("""
        **Q: How long does the assessment take?**  
        A: The complete assessment process takes about 20-30 minutes. You can save and continue later.
        
        **Q: Can I retake the assessments?**  
        A: Yes! We recommend retaking assessments every 6-12 months to track your growth.
        
        **Q: Is my data private?**  
        A: Absolutely. Your assessment data is stored securely and never shared without permission.
        
        **Q: How accurate are the career recommendations?**  
        A: Our recommendations are based on validated psychological models and continuously improved through AI.
        
        **Q: Can I use this for my team/clients?**  
        A: Yes! Check out our Coach and Manager dashboards for team and client management features.
        """)
    
    with st.expander("📚 Learn More About RIASEC"):
        st.markdown("""
        The RIASEC model categorizes both people and work environments into six types:
        
        - **Realistic (R)**: Practical, hands-on, physical activities
        - **Investigative (I)**: Analytical, intellectual, scientific thinking
        - **Artistic (A)**: Creative, expressive, imaginative work
        - **Social (S)**: Helping, teaching, interpersonal interaction
        - **Enterprising (E)**: Leading, persuading, business-oriented
        - **Conventional (C)**: Organizing, detail-oriented, structured tasks
        
        Most people have characteristics of multiple types, creating unique profiles like RIA or SEC.
        """)
    
    # Save that user has visited welcome page
    if not is_returning_user:
        # Create initial profile
        profile_data = {
            'username': username,
            'name': user_info.get('name', username),
            'created_at': datetime.now().isoformat(),
            'last_login': datetime.now().isoformat(),
            'onboarding_completed': False
        }
        data_manager.save_user_profile(username, profile_data)

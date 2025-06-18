import streamlit as st

def show_welcome():
    st.title("🧭 Welcome to Career Atlas")
    
    st.markdown("""
    ### Your AI-Powered Career Navigation System
    
    Career Atlas helps you discover your ideal career path through:
    
    - **RIASEC Assessment**: Understand your personality type and interests
    - **AI-Powered Analysis**: Get personalized career recommendations
    - **Career Coaching**: Receive guidance tailored to your unique profile
    
    #### How It Works
    
    1. **Take the Assessment**: Complete our comprehensive RIASEC questionnaire
    2. **Get Your Results**: Receive your personality profile and career matches
    3. **Explore Opportunities**: Discover careers aligned with your interests
    4. **Plan Your Path**: Get actionable steps to achieve your career goals
    
    Ready to begin your journey? Click on **Assessment** in the sidebar to start!
    """)
    
    # Add some visual elements
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Assessment Time", "15-20 min", help="Average time to complete")
    
    with col2:
        st.metric("Career Matches", "10+", help="Personalized recommendations")
    
    with col3:
        st.metric("Success Rate", "94%", help="User satisfaction score")
    
    st.divider()
    
    st.subheader("About RIASEC")
    
    st.markdown("""
    The RIASEC model categorizes interests into six types:
    
    - **R**ealistic: Practical, hands-on activities
    - **I**nvestigative: Analytical, intellectual pursuits
    - **A**rtistic: Creative, expressive endeavors
    - **S**ocial: Helping and teaching others
    - **E**nterprising: Leading and persuading
    - **C**onventional: Organizing and processing data
    
    Your unique combination of these types helps identify careers where you'll thrive!
    """)


import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Any
import pandas as pd

def show_results_page(data_manager):
    """Display assessment results and career recommendations"""
    st.header("📊 Your Career Assessment Results")
    
    # Check if assessments are complete
    if not has_completed_assessments():
        st.warning("Please complete all assessments to view your full results.")
        if st.button("Go to Assessments"):
            st.session_state.current_page = "assessment"
            st.rerun()
        return
    
    # Load user profile
    user_profile = data_manager.load_user_profile(st.session_state.username)
    
    # Display results based on persona
    persona = st.session_state.get('selected_persona', 'Individual')
    
    if persona == 'Individual':
        show_individual_results(user_profile, data_manager)
    elif persona == 'Coach':
        show_coach_results(user_profile, data_manager)
    elif persona == 'Manager':
        show_manager_results(user_profile, data_manager)

def has_completed_assessments():
    """Check if user has completed required assessments"""
    assessment_data = st.session_state.get('assessment_data', {})
    return (
        assessment_data.get('riasec', {}).get('completed', False) and
        assessment_data.get('skills', {}).get('completed', False) and
        assessment_data.get('values', {}).get('completed', False)
    )

def show_individual_results(user_profile: Dict[str, Any], data_manager):
    """Show results for individual users"""
    
    # RIASEC Profile
    st.subheader("🎯 Your RIASEC Profile")
    
    riasec_scores = user_profile['assessments']['riasec']['data']['scores']
    
    # Create radar chart
    fig = create_riasec_radar_chart(riasec_scores)
    st.plotly_chart(fig, use_container_width=True)
    
    # Top 3 RIASEC types
    top_types = sorted(riasec_scores.items(), key=lambda x: x[1], reverse=True)[:3]
    
    col1, col2, col3 = st.columns(3)
    for i, (riasec_type, score) in enumerate(top_types):
        with [col1, col2, col3][i]:
            st.metric(
                f"#{i+1} {riasec_type.capitalize()}",
                f"{score:.0f}%",
                help=get_riasec_description(riasec_type)
            )
    
    st.divider()
    
    # Skills Profile
    st.subheader("💪 Your Skills Profile")
    
    skills_data = user_profile['assessments']['skills']['data']['responses']
    skills_df = create_skills_dataframe(skills_data)
    
    # Skills bar chart
    fig = px.bar(
        skills_df,
        x='confidence_score',
        y='skill',
        orientation='h',
        color='category',
        title="Skills Confidence Levels"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Career Recommendations
    st.subheader("🎯 Recommended Career Paths")
    
    # Get career recommendations
    careers = data_manager.get_top_careers(riasec_scores, num_careers=10)
    
    # Display top careers
    for i, career in enumerate(careers[:5]):
        with st.expander(f"#{i+1} {career['title']} - {career['match_score']:.0f}% Match"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write("**Description:**")
                st.write(career.get('description', 'Career description coming soon...'))
                
                st.write("**Key Responsibilities:**")
                for resp in career.get('responsibilities', ['Details coming soon']):
                    st.write(f"• {resp}")
            
            with col2:
                st.write("**Required Skills:**")
                for skill in career.get('required_skills', ['Skills analysis pending']):
                    st.write(f"• {skill}")
                
                st.write("**Education:**")
                st.write(career.get('education', 'Varies by employer'))
                
                st.write("**Salary Range:**")
                st.write(career.get('salary_range', 'Competitive'))
    
    # Export results
    st.divider()
    if st.button("📥 Download Full Report"):
        export_data = data_manager.export_user_data(st.session_state.username)
        st.download_button(
            label="Download JSON Report",
            data=json.dumps(export_data, indent=2),
            file_name=f"career_assessment_{st.session_state.username}.json",
            mime="application/json"
        )

def show_coach_results(user_profile: Dict[str, Any], data_manager):
    """Show results view for coaches"""
    st.info("Coach View: Analyzing client assessment results")
    
    # Client overview
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Client Profile Overview")
        
        # RIASEC summary
        riasec_scores = user_profile['assessments']['riasec']['data']['scores']
        top_types = sorted(riasec_scores.items(), key=lambda x: x[1], reverse=True)[:3]
        
        st.write("**Primary RIASEC Types:**")
        for riasec_type, score in top_types:
            st.write(f"• {riasec_type.capitalize()}: {score:.0f}%")
        
        # Values summary
        values = user_profile['assessments']['values']['data']['selected_values']
        st.write("\n**Top Work Values:**")
        for value in values[:5]:
            st.write(f"• {value}")
    
    with col2:
        # Coaching insights
        st.subheader("AI Coaching Insights")
        
        if st.button("Generate Coaching Insights"):
            with st.spinner("Analyzing profile..."):
                # This would call the LLM to generate insights
                st.success("Insights generated!")
                st.write("""
                **Key Observations:**
                - Strong investigative and artistic tendencies
                - Values creativity and autonomy
                - May thrive in research or design roles
                
                **Suggested Discussion Topics:**
                - Exploring creative technical roles
                - Building a portfolio
                - Networking strategies
                """)
    
    # Coaching questions bank
    st.divider()
    st.subheader("🤔 Coaching Questions")
    
    question_categories = {
        "Self-Discovery": [
            "What activities make you lose track of time?",
            "When do you feel most energized at work?",
            "What accomplishments are you most proud of?"
        ],
        "Career Exploration": [
            "What aspects of your ideal job are non-negotiable?",
            "How do you define career success?",
            "What industries intrigue you and why?"
        ],
        "Action Planning": [
            "What's one step you can take this week toward your career goals?",
            "Who in your network could provide valuable insights?",
            "What skills would you like to develop next?"
        ]
    }
    
    for category, questions in question_categories.items():
        with st.expander(category):
            for question in questions:
                st.write(f"• {question}")

def show_manager_results(user_profile: Dict[str, Any], data_manager):
    """Show results view for managers"""
    st.info("Manager View: Team member development insights")
    
    # Team member summary
    st.subheader("Team Member Profile")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Primary Type", "Investigative", "85%")
    
    with col2:
        st.metric("Top Skill", "Data Analysis", "Expert")
    
    with col3:
        st.metric("Key Value", "Innovation", "High")
    
    # Development recommendations
    st.divider()
    st.subheader("📈 Development Recommendations")
    
    recommendations = [
        {
            "area": "Technical Leadership",
            "current": "Individual Contributor",
            "target": "Technical Lead",
            "actions": ["Mentor junior developers", "Lead technical discussions", "Own system architecture decisions"]
        },
        {
            "area": "Communication Skills",
            "current": "Intermediate",
            "target": "Advanced",
            "actions": ["Present at team meetings", "Write technical documentation", "Facilitate workshops"]
        }
    ]
    
    for rec in recommendations:
        with st.expander(f"{rec['area']}: {rec['current']} → {rec['target']}"):
            st.write("**Recommended Actions:**")
            for action in rec['actions']:
                st.write(f"• {action}")
    
    # Team fit analysis
    st.divider()
    st.subheader("🤝 Team Fit Analysis")
    
    # Mock team composition data
    team_data = pd.DataFrame({
        'Member': ['Current User', 'Team Avg'],
        'Realistic': [30, 45],
        'Investigative': [85, 60],
        'Artistic': [
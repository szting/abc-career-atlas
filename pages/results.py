import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from utils.llm_manager import LLMManager
from utils.data_manager import DataManager
import pandas as pd

def show_results():
    st.title("📊 Your Career Assessment Results")
    
    # Check if assessment is complete
    if 'assessment_complete' not in st.session_state or not st.session_state.assessment_complete:
        st.warning("Please complete the assessment first to see your results.")
        return
    
    # Initialize managers
    llm_manager = LLMManager()
    data_manager = DataManager()
    
    # Get assessment data
    scores = st.session_state.assessment_scores
    assessment_data = st.session_state.assessment_data
    
    # Display RIASEC Profile
    st.subheader("Your RIASEC Profile")
    
    # Create radar chart
    categories = list(scores.keys())
    values = list(scores.values())
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Your Profile'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5]
            )),
        showlegend=False,
        title="RIASEC Interest Profile"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Display top 3 types
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top_types = sorted_scores[:3]
    
    st.subheader("Your Top Interest Areas")
    
    col1, col2, col3 = st.columns(3)
    
    for i, (type_name, score) in enumerate(top_types):
        with [col1, col2, col3][i]:
            st.metric(
                label=f"#{i+1} {type_name}",
                value=f"{score:.1f}/5.0",
                delta=f"{(score/5)*100:.0f}%"
            )
    
    # Generate career recommendations
    st.subheader("🎯 Recommended Careers")
    
    with st.spinner("Generating personalized career recommendations..."):
        # Get AI-powered recommendations
        career_recommendations = llm_manager.generate_career_recommendations(
            scores=scores,
            additional_info=assessment_data['additional_info']
        )
        
        if career_recommendations:
            # Display recommendations in expandable sections
            for i, career in enumerate(career_recommendations[:5]):
                with st.expander(f"{i+1}. {career['title']}", expanded=(i==0)):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.write("**Description:**")
                        st.write(career.get('description', 'No description available'))
                        
                        st.write("**Why it matches your profile:**")
                        st.write(career.get('match_reason', 'Based on your RIASEC scores'))
                        
                        st.write("**Required Skills:**")
                        skills = career.get('skills', [])
                        if skills:
                            st.write(", ".join(skills))
                    
                    with col2:
                        st.write("**Match Score:**")
                        match_score = career.get('match_score', 85)
                        st.progress(match_score/100)
                        st.caption(f"{match_score}% match")
                        
                        st.write("**Salary Range:**")
                        st.write(career.get('salary_range', 'Varies'))
                        
                        st.write("**Growth Outlook:**")
                        st.write(career.get('growth_outlook', 'Average'))
    
    # Career Development Plan
    st.subheader("📈 Your Career Development Plan")
    
    with st.spinner("Creating your personalized development plan..."):
        development_plan = llm_manager.generate_development_plan(
            scores=scores,
            careers=career_recommendations[:3],
            additional_info=assessment_data['additional_info']
        )
        
        if development_plan:
            tabs = st.tabs(["Short-term Goals", "Skills to Develop", "Resources", "Action Steps"])
            
            with tabs[0]:
                st.write("**Goals for the next 6 months:**")
                for goal in development_plan.get('short_term_goals', []):
                    st.write(f"• {goal}")
            
            with tabs[1]:
                st.write("**Key skills to focus on:**")
                skills_df = pd.DataFrame(development_plan.get('skills_to_develop', []))
                if not skills_df.empty:
                    st.dataframe(skills_df, use_container_width=True)
            
            with tabs[2]:
                st.write("**Recommended resources:**")
                for resource in development_plan.get('resources', []):
                    st.write(f"• {resource}")
            
            with tabs[3]:
                st.write("**Your action plan:**")
                for i, step in enumerate(development_plan.get('action_steps', [])):
                    st.checkbox(step, key=f"action_{i}")
    
    # Export options
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Export Report", use_container_width=True):
            # Generate PDF report
            report_data = data_manager.generate_report(assessment_data, career_recommendations)
            st.download_button(
                label="Download PDF Report",
                data=report_data,
                file_name=f"career_assessment_{st.session_state.username}.pdf",
                mime="application/pdf"
            )
    
    with col2:
        if st.button("📧 Email Results", use_container_width=True):
            st.info("Email functionality coming soon!")
    
    with col3:
        if st.button("🔄 Retake Assessment", use_container_width=True):
            # Clear assessment data
            st.session_state.assessment_complete = False
            st.session_state.responses = {}
            st.rerun()

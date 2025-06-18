import streamlit as st
from typing import Dict, List, Any
import json
from datetime import datetime

def show_assessment_page(data_manager):
    """Display the assessment page"""
    st.header("📋 Career Assessment Suite")
    
    # Assessment progress
    progress = calculate_assessment_progress()
    st.progress(progress / 100)
    st.caption(f"Overall Progress: {progress}%")
    
    # Assessment tabs
    tab1, tab2, tab3 = st.tabs(["RIASEC Assessment", "Skills Confidence", "Work Values"])
    
    with tab1:
        show_riasec_assessment(data_manager)
    
    with tab2:
        show_skills_assessment(data_manager)
    
    with tab3:
        show_values_assessment(data_manager)

def calculate_assessment_progress():
    """Calculate overall assessment progress"""
    completed = 0
    if st.session_state.get('assessment_data', {}).get('riasec', {}).get('completed'):
        completed += 1
    if st.session_state.get('assessment_data', {}).get('skills', {}).get('completed'):
        completed += 1
    if st.session_state.get('assessment_data', {}).get('values', {}).get('completed'):
        completed += 1
    
    return int((completed / 3) * 100)

def show_riasec_assessment(data_manager):
    """Display RIASEC assessment"""
    st.subheader("🎯 RIASEC Interest Profiler")
    
    st.markdown("""
    The RIASEC assessment helps identify your Holland Code - a combination of personality types 
    that can guide you toward careers that match your interests.
    
    Rate each activity based on how much you would enjoy doing it:
    """)
    
    # Load RIASEC questions
    questions = load_riasec_questions()
    
    # Initialize responses in session state
    if 'riasec_responses' not in st.session_state:
        st.session_state.riasec_responses = {}
    
    # Display questions by category
    riasec_types = ['Realistic', 'Investigative', 'Artistic', 'Social', 'Enterprising', 'Conventional']
    
    for riasec_type in riasec_types:
        with st.expander(f"{riasec_type} Activities", expanded=True):
            type_questions = questions.get(riasec_type.lower(), [])
            
            for i, question in enumerate(type_questions[:10]):  # 10 questions per type
                key = f"{riasec_type.lower()}_{i}"
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(question)
                with col2:
                    response = st.select_slider(
                        "Interest",
                        options=[1, 2, 3, 4, 5],
                        value=st.session_state.riasec_responses.get(key, 3),
                        key=f"riasec_{key}",
                        label_visibility="collapsed"
                    )
                    st.session_state.riasec_responses[key] = response
    
    # Submit button
    if st.button("Complete RIASEC Assessment", type="primary"):
        # Calculate scores
        scores = calculate_riasec_scores(st.session_state.riasec_responses)
        
        # Save assessment
        assessment_data = {
            "completed": True,
            "timestamp": datetime.now().isoformat(),
            "responses": st.session_state.riasec_responses,
            "scores": scores
        }
        
        if 'assessment_data' not in st.session_state:
            st.session_state.assessment_data = {}
        
        st.session_state.assessment_data['riasec'] = assessment_data
        
        # Save to database
        data_manager.save_assessment(
            st.session_state.username,
            "riasec",
            assessment_data
        )
        
        st.success("✅ RIASEC Assessment completed successfully!")
        st.balloons()

def show_skills_assessment(data_manager):
    """Display skills confidence assessment"""
    st.subheader("💪 Skills Confidence Assessment")
    
    st.markdown("""
    Rate your confidence level in each skill area. This helps us understand your strengths 
    and areas for potential development.
    """)
    
    # Load skills categories
    skills_categories = load_skills_categories()
    
    if 'skills_responses' not in st.session_state:
        st.session_state.skills_responses = {}
    
    for category, skills in skills_categories.items():
        with st.expander(f"{category} Skills", expanded=True):
            for skill in skills:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(skill)
                with col2:
                    confidence = st.select_slider(
                        "Confidence",
                        options=["Beginner", "Basic", "Intermediate", "Advanced", "Expert"],
                        value=st.session_state.skills_responses.get(skill, "Intermediate"),
                        key=f"skill_{skill}",
                        label_visibility="collapsed"
                    )
                    st.session_state.skills_responses[skill] = confidence
    
    if st.button("Complete Skills Assessment", type="primary"):
        assessment_data = {
            "completed": True,
            "timestamp": datetime.now().isoformat(),
            "responses": st.session_state.skills_responses
        }
        
        if 'assessment_data' not in st.session_state:
            st.session_state.assessment_data = {}
        
        st.session_state.assessment_data['skills'] = assessment_data
        
        # Save to database
        data_manager.save_assessment(
            st.session_state.username,
            "skills",
            assessment_data
        )
        
        st.success("✅ Skills Assessment completed successfully!")

def show_values_assessment(data_manager):
    """Display work values assessment"""
    st.subheader("🌟 Work Values Assessment")
    
    st.markdown("""
    Select the work values that are most important to you. These help us understand 
    what you're looking for in your ideal career.
    """)
    
    # Load work values
    work_values = load_work_values()
    
    if 'values_responses' not in st.session_state:
        st.session_state.values_responses = []
    
    # Display values in categories
    for category, values in work_values.items():
        st.write(f"**{category}**")
        
        cols = st.columns(2)
        for i, value in enumerate(values):
            with cols[i % 2]:
                selected = st.checkbox(
                    value['name'],
                    value=value['name'] in st.session_state.values_responses,
                    help=value['description'],
                    key=f"value_{value['name']}"
                )
                
                if selected and value['name'] not in st.session_state.values_responses:
                    st.session_state.values_responses.append(value['name'])
                elif not selected and value['name'] in st.session_state.values_responses:
                    st.session_state.values_responses.remove(value['name'])
    
    st.info(f"Selected {len(st.session_state.values_responses)} values")
    
    if st.button("Complete Values Assessment", type="primary"):
        if len(st.session_state.values_responses) < 5:
            st.error("Please select at least 5 work values that are important to you.")
        else:
            assessment_data = {
                "completed": True,
                "timestamp": datetime.now().isoformat(),
                "selected_values": st.session_state.values_responses
            }
            
            if 'assessment_data' not in st.session_state:
                st.session_state.assessment_data = {}
            
            st.session_state.assessment_data['values'] = assessment_data
            
            # Save to database
            data_manager.save_assessment(
                st.session_state.username,
                "values",
                assessment_data
            )
            
            st.success("✅ Values Assessment completed successfully!")
            st.info("🎉 All assessments complete! View your results in the Results page.")

def load_riasec_questions():
    """Load RIASEC assessment questions"""
    # Default questions if file doesn't exist
    return {
        "realistic": [
            "Build things with your hands",
            "Work on cars or mechanical equipment",
            "Work outdoors",
            "Operate tools and machinery",
            "Work with animals",
            "Build or repair furniture",
            "Work in construction",
            "Grow plants or gardens",
            "Hunt or fish",
            "Play sports or exercise"
        ],
        "investigative": [
            "Solve complex problems",
            "Conduct scientific experiments",
            "Analyze data and statistics",
            "Research topics in depth",
            "Work with computers and technology",
            "Study how things work",
            "Read scientific articles",
            "Develop new theories",
            "Work in a laboratory",
            "Solve mathematical problems"
        ],
        "artistic": [
            "Create art or music",
            "Write stories or poetry",
            "Design graphics or websites",
            "Perform in front of others",
            "Take photographs",
            "Act in plays or movies",
            "Play musical instruments",
            "Design clothing or interiors",
            "Work in creative fields",
            "Express yourself creatively"
        ],
        "social": [
            "Help people solve problems",
            "Teach or train others",
            "Work with children",
            "Provide counseling or therapy",
            "Work in healthcare",
            "Volunteer for causes",
            "Lead group discussions",
            "Work in customer service",
            "Help people in need",
            "Work in community service"
        ],
        "enterprising": [
            "Lead teams or projects",
            "Start your own business",
            "Sell products or services",
            "Manage people or operations",
            "Make important decisions",
            "Negotiate deals",
            "Give presentations",
            "Influence others",
            "Take financial risks",
            "Work in competitive environments"
        ],
        "conventional": [
            "Organize files and records",
            "Follow established procedures",
            "Work with numbers and data",
            "Maintain accurate records",
            "Work in structured environments",
            "Handle administrative tasks",
            "Create systems and processes",
            "Work with spreadsheets",
            "Manage schedules and calendars",
            "Ensure quality and accuracy"
        ]
    }

def load_skills_categories():
    """Load skills categories"""
    return {
        "Technical": [
            "Programming/Coding",
            "Data Analysis",
            "Digital Marketing",
            "Graphic Design",
            "Project Management",
            "Database Management",
            "Cloud Computing",
            "Cybersecurity"
        ],
        "Communication": [
            "Public Speaking",
            "Written Communication",
            "Active Listening",
            "Presentation Skills",
            "Negotiation",
            "Conflict Resolution",
            "Cross-cultural Communication",
            "Storytelling"
        ],
        "Leadership": [
            "Team Management",
            "Strategic Planning",
            "Decision Making",
            "Delegation",
            "Mentoring/Coaching",
            "Change Management",
            "Vision Setting",
            "Performance Management"
        ],
        "Analytical": [
            "Problem Solving",
            "Critical Thinking",
            "Research Skills",
            "Data Interpretation",
            "Financial Analysis",
            "Risk Assessment",
            "Process Improvement",
            "Quality Assurance"
        ]
    }

def load_work_values():
    """Load work values categories"""
    return {
        "Achievement": [
            {"name": "Recognition", "description": "Being acknowledged for your contributions"},
            {"name": "Advancement", "description": "Opportunities for career growth"},
            {"name": "Challenge", "description": "Work that tests your abilities"},
            {"name": "Results", "description": "Seeing tangible outcomes from your work"}
        ],
        "Independence": [
            {"name": "Autonomy", "description": "Freedom to make your own decisions"},
            {"name": "Creativity", "description": "Ability to express original ideas"},
            {"name": "Flexibility", "description": "Control over your schedule and work style"},
            {"name": "Variety", "description": "Diverse tasks and responsibilities"}
        ],
        "Relationships": [
            {"name": "Teamwork", "description": "Collaborating with others"},
            {"name": "Service", "description": "Helping others and making a difference"},
            {"name": "Leadership", "description": "Guiding and influencing others"},
            {"name": "Mentorship", "description": "Teaching and developing others"}
        ],
        "Working Conditions": [
            {"name": "Security", "description": "Stable employment and benefits"},
            {"name": "Compensation", "description": "Fair pay and financial rewards"},
            {"name": "Work-Life Balance", "description": "Time for personal life and interests"},
            {"name": "Environment", "description": "Pleasant and comfortable workplace"}
        ]
    }

def calculate_riasec_scores(responses: Dict[str, int]) -> Dict[str, float]:
    """Calculate RIASEC scores from responses"""
    riasec_types = ['realistic', 'investigative', 'artistic', 'social', 'enterprising', 'conventional']
    scores = {}
    
    for riasec_type in riasec_types:
        type_responses = [v for k, v in responses.items() if k.startswith(riasec_type)]
        if type_responses:
            # Calculate average and scale to 0-100
            scores[riasec_type] = (sum(type_responses) / len(type_responses)) * 20
        else:
            scores[riasec_type] = 0
    
    return scores

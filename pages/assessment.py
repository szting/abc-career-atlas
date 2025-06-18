import streamlit as st
from utils.data_manager import DataManager
from utils.llm_manager import LLMManager
import json
from datetime import datetime

def show_assessment():
    st.title("🎯 RIASEC Career Assessment")
    
    # Initialize managers
    data_manager = DataManager()
    llm_manager = LLMManager()
    
    # Assessment questions organized by RIASEC category
    questions = {
        "Realistic": [
            "I enjoy working with tools and machines",
            "I like to build or fix things with my hands",
            "I prefer outdoor activities over indoor ones",
            "I enjoy physical activities and sports",
            "I like working with plants or animals"
        ],
        "Investigative": [
            "I enjoy solving complex problems",
            "I like to understand how things work",
            "I enjoy conducting research and experiments",
            "I prefer working with ideas rather than people",
            "I like analyzing data and information"
        ],
        "Artistic": [
            "I enjoy creative activities like art, music, or writing",
            "I like to express myself through various mediums",
            "I prefer unstructured, flexible environments",
            "I enjoy coming up with new ideas",
            "I like to think outside the box"
        ],
        "Social": [
            "I enjoy helping and teaching others",
            "I like working in teams",
            "I prefer jobs that involve interacting with people",
            "I enjoy volunteering and community service",
            "I like to mentor or coach others"
        ],
        "Enterprising": [
            "I enjoy leading and influencing others",
            "I like to take on challenges and risks",
            "I enjoy selling ideas or products",
            "I prefer competitive environments",
            "I like to start new projects or businesses"
        ],
        "Conventional": [
            "I enjoy organizing and structuring information",
            "I like following established procedures",
            "I prefer working with numbers and data",
            "I enjoy administrative tasks",
            "I like maintaining order and accuracy"
        ]
    }
    
    # Initialize session state for responses
    if 'responses' not in st.session_state:
        st.session_state.responses = {}
    
    # Progress tracking
    total_questions = sum(len(q) for q in questions.values())
    answered = len(st.session_state.responses)
    
    st.progress(answered / total_questions)
    st.caption(f"Progress: {answered}/{total_questions} questions answered")
    
    # Display questions by category
    for category, category_questions in questions.items():
        st.subheader(f"{category} Interests")
        
        for i, question in enumerate(category_questions):
            question_key = f"{category}_{i}"
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(question)
            
            with col2:
                response = st.select_slider(
                    "Rate",
                    options=[1, 2, 3, 4, 5],
                    value=st.session_state.responses.get(question_key, 3),
                    key=question_key,
                    label_visibility="collapsed",
                    help="1 = Strongly Disagree, 5 = Strongly Agree"
                )
                st.session_state.responses[question_key] = response
        
        st.divider()
    
    # Additional information section
    st.subheader("Additional Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        education = st.selectbox(
            "Highest Education Level",
            ["High School", "Some College", "Bachelor's Degree", "Master's Degree", "Doctorate"],
            key="education"
        )
        
        experience = st.number_input(
            "Years of Work Experience",
            min_value=0,
            max_value=50,
            value=0,
            key="experience"
        )
    
    with col2:
        interests = st.text_area(
            "Other interests or hobbies",
            placeholder="Tell us about your other interests...",
            key="interests"
        )
        
        goals = st.text_area(
            "Career goals",
            placeholder="What are your career aspirations?",
            key="goals"
        )
    
    # Submit button
    if st.button("Submit Assessment", type="primary", use_container_width=True):
        if len(st.session_state.responses) < total_questions:
            st.error("Please answer all questions before submitting.")
        else:
            with st.spinner("Analyzing your responses..."):
                # Calculate RIASEC scores
                scores = calculate_riasec_scores(st.session_state.responses, questions)
                
                # Prepare assessment data
                assessment_data = {
                    "username": st.session_state.username,
                    "timestamp": datetime.now().isoformat(),
                    "responses": st.session_state.responses,
                    "scores": scores,
                    "additional_info": {
                        "education": education,
                        "experience": experience,
                        "interests": interests,
                        "goals": goals
                    }
                }
                
                # Save assessment data
                data_manager.save_assessment(assessment_data)
                
                # Store in session state for results page
                st.session_state.assessment_complete = True
                st.session_state.assessment_scores = scores
                st.session_state.assessment_data = assessment_data
                
                st.success("Assessment completed! Go to Results to see your career profile.")

def calculate_riasec_scores(responses, questions):
    """Calculate RIASEC scores from responses"""
    scores = {}
    
    for category in questions.keys():
        category_scores = []
        for i in range(len(questions[category])):
            question_key = f"{category}_{i}"
            if question_key in responses:
                category_scores.append(responses[question_key])
        
        # Calculate average score for category
        if category_scores:
            scores[category] = sum(category_scores) / len(category_scores)
        else:
            scores[category] = 0
    
    return scores

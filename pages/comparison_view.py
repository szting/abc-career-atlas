"""
Comparison View - RIASEC vs Skills Spider Diagram
Compares user's RIASEC scores with their skills confidence based on job skills data
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from utils.session_state import SessionStateManager
from utils.data_manager import DataManager
from utils.career_manager import CareerManager
import json
import os
from typing import Dict, List, Tuple

def show_comparison_view():
    """Display comparison between RIASEC scores and Skills confidence"""
    st.title("📊 RIASEC vs Skills Comparison")
    st.markdown("Compare your personality profile with your skills confidence based on job requirements")
    
    # Check if user has completed assessments
    if not SessionStateManager.get('assessment_complete', False):
        st.warning("Please complete the RIASEC assessment first to see comparisons.")
        if st.button("Go to Assessment"):
            SessionStateManager.navigate_to('riasec_assessment')
        return
    
    # Get RIASEC scores
    riasec_scores = SessionStateManager.get('assessment_scores', {})
    if not riasec_scores:
        st.error("No RIASEC scores found. Please complete the assessment.")
        return
    
    # Get skills assessment data
    skills_responses = SessionStateManager.get('skills_assessment_responses', {})
    
    # Initialize managers
    data_manager = DataManager()
    career_manager = CareerManager()
    
    # Load job skills data
    job_skills_data = load_job_skills_data()
    
    if not job_skills_data:
        st.info("No job skills data uploaded yet. Using default skill mappings.")
        job_skills_data = get_default_job_skills_mapping()
    
    # Calculate skills confidence by RIASEC type
    skills_by_riasec = map_skills_to_riasec(skills_responses, job_skills_data)
    
    # Create comparison visualization
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Create spider diagram
        fig = create_comparison_spider_diagram(riasec_scores, skills_by_riasec)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Display legend and insights
        st.markdown("### 📍 Legend")
        st.markdown("🔵 **RIASEC Scores**: Your personality assessment results")
        st.markdown("🟢 **Skills Confidence**: Your self-rated skills mapped to RIASEC types")
        
        st.markdown("### 💡 Insights")
        insights = generate_comparison_insights(riasec_scores, skills_by_riasec)
        for insight in insights:
            st.info(insight)
    
    # Detailed comparison table
    st.markdown("### 📋 Detailed Comparison")
    comparison_df = create_comparison_dataframe(riasec_scores, skills_by_riasec)
    
    # Style the dataframe
    styled_df = comparison_df.style.background_gradient(subset=['RIASEC Score', 'Skills Confidence'], cmap='RdYlGn')
    st.dataframe(styled_df, use_container_width=True)
    
    # Gap analysis
    st.markdown("### 🎯 Gap Analysis")
    gaps = analyze_gaps(riasec_scores, skills_by_riasec)
    
    if gaps['aligned']:
        st.success("✅ Your skills align well with your interests!")
        for item in gaps['aligned']:
            st.write(f"• **{item['type']}**: Both interest and skills are strong")
    
    if gaps['opportunities']:
        st.warning("📈 Development Opportunities")
        for item in gaps['opportunities']:
            st.write(f"• **{item['type']}**: High interest ({item['interest']:.1f}) but lower skills ({item['skills']:.1f})")
            with st.expander(f"Recommended skills to develop for {item['type']}"):
                for skill in item['recommended_skills']:
                    st.write(f"  - {skill}")
    
    if gaps['underutilized']:
        st.info("💼 Underutilized Strengths")
        for item in gaps['underutilized']:
            st.write(f"• **{item['type']}**: Strong skills ({item['skills']:.1f}) but lower interest ({item['interest']:.1f})")
    
    # Career recommendations based on alignment
    st.markdown("### 🚀 Career Recommendations Based on Alignment")
    
    # Get careers that match both RIASEC and skills profile
    aligned_careers = get_aligned_career_recommendations(riasec_scores, skills_by_riasec, career_manager)
    
    if aligned_careers:
        for i, career in enumerate(aligned_careers[:5]):
            with st.expander(f"{i+1}. {career['title']} - {career['alignment_score']:.0f}% alignment"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write("**Why this career fits:**")
                    st.write(career['alignment_reason'])
                    
                    st.write("**Required skills you have:**")
                    matching_skills = career.get('matching_skills', [])
                    if matching_skills:
                        st.write(", ".join(matching_skills[:5]))
                    
                    st.write("**Skills to develop:**")
                    missing_skills = career.get('skills_to_develop', [])
                    if missing_skills:
                        st.write(", ".join(missing_skills[:3]))
                
                with col2:
                    st.metric("Interest Match", f"{career['interest_match']:.0f}%")
                    st.metric("Skills Match", f"{career['skills_match']:.0f}%")
                    st.metric("Overall Alignment", f"{career['alignment_score']:.0f}%")
    
    # Export options
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Export Comparison Report", use_container_width=True):
            report_data = generate_comparison_report(riasec_scores, skills_by_riasec, gaps, aligned_careers)
            st.download_button(
                label="Download Report",
                data=report_data,
                file_name=f"riasec_skills_comparison_{SessionStateManager.get('username')}.json",
                mime="application/json"
            )
    
    with col2:
        if st.button("🔄 Update Skills Assessment", use_container_width=True):
            SessionStateManager.navigate_to('skills_assessment')
    
    with col3:
        if st.button("📊 View Full Results", use_container_width=True):
            SessionStateManager.navigate_to('results')

def load_job_skills_data() -> Dict:
    """Load uploaded job skills data from the correct directory"""
    try:
        # Check multiple possible locations for job skills data
        possible_paths = [
            os.path.join('data', 'jobskills', 'job_skills_mapping.json'),
            os.path.join('data', 'jobskills', 'skills_mapping.json'),
            os.path.join('data', 'jobskills', 'skills.json'),
            # Also check for CSV files
            os.path.join('data', 'jobskills', 'skills.csv'),
            os.path.join('data', 'jobskills', 'job_skills.csv')
        ]
        
        # Try JSON files first
        for path in possible_paths:
            if path.endswith('.json') and os.path.exists(path):
                with open(path, 'r') as f:
                    return json.load(f)
        
        # Try CSV files if no JSON found
        for path in possible_paths:
            if path.endswith('.csv') and os.path.exists(path):
                # Convert CSV to expected format
                df = pd.read_csv(path)
                return convert_csv_to_skills_mapping(df)
        
        # Check if there are any files in the jobskills directory
        jobskills_dir = os.path.join('data', 'jobskills')
        if os.path.exists(jobskills_dir):
            files = os.listdir(jobskills_dir)
            if files:
                st.info(f"Found files in jobskills directory: {', '.join(files)}")
                # Try to load the first JSON or CSV file found
                for file in files:
                    file_path = os.path.join(jobskills_dir, file)
                    if file.endswith('.json'):
                        with open(file_path, 'r') as f:
                            return json.load(f)
                    elif file.endswith('.csv'):
                        df = pd.read_csv(file_path)
                        return convert_csv_to_skills_mapping(df)
        
    except Exception as e:
        st.error(f"Error loading job skills data: {str(e)}")
    
    return None

def convert_csv_to_skills_mapping(df: pd.DataFrame) -> Dict:
    """Convert CSV data to expected skills mapping format"""
    skill_mapping = {}
    
    # Try to identify columns that might contain skill names and RIASEC types
    skill_columns = ['skill', 'skill_name', 'name', 'skills']
    riasec_columns = ['riasec', 'riasec_type', 'type', 'category']
    
    skill_col = None
    riasec_col = None
    
    # Find the appropriate columns
    for col in df.columns:
        if col.lower() in skill_columns:
            skill_col = col
        elif col.lower() in riasec_columns:
            riasec_col = col
    
    # If we found both columns, create the mapping
    if skill_col and riasec_col:
        for _, row in df.iterrows():
            skill = row[skill_col]
            riasec = row[riasec_col]
            if pd.notna(skill) and pd.notna(riasec):
                skill_mapping[str(skill)] = str(riasec)
    
    return {"skill_riasec_mapping": skill_mapping}

def get_default_job_skills_mapping() -> Dict:
    """Provide default mapping of skills to RIASEC types"""
    return {
        "skill_riasec_mapping": {
            # Realistic skills
            "Equipment Operation": "Realistic",
            "Mechanical Skills": "Realistic",
            "Physical Coordination": "Realistic",
            "Tool Usage": "Realistic",
            "Construction": "Realistic",
            "Repair & Maintenance": "Realistic",
            "Technical Drawing": "Realistic",
            "Safety Procedures": "Realistic",
            "Quality Control": "Realistic",
            "Manufacturing": "Realistic",
            
            # Investigative skills
            "Data Analysis": "Investigative",
            "Research": "Investigative",
            "Problem Solving": "Investigative",
            "Critical Thinking": "Investigative",
            "Scientific Method": "Investigative",
            "Statistical Analysis": "Investigative",
            "Laboratory Skills": "Investigative",
            "Hypothesis Testing": "Investigative",
            "Technical Writing": "Investigative",
            "Systems Analysis": "Investigative",
            
            # Artistic skills
            "Creative Design": "Artistic",
            "Writing": "Artistic",
            "Visual Arts": "Artistic",
            "Music/Performance": "Artistic",
            "Innovation": "Artistic",
            "Storytelling": "Artistic",
            "Photography": "Artistic",
            "Video Production": "Artistic",
            "Graphic Design": "Artistic",
            "User Experience Design": "Artistic",
            
            # Social skills
            "Communication": "Social",
            "Teaching": "Social",
            "Counseling": "Social",
            "Team Collaboration": "Social",
            "Customer Service": "Social",
            "Empathy": "Social",
            "Active Listening": "Social",
            "Conflict Resolution": "Social",
            "Mentoring": "Social",
            "Public Relations": "Social",
            
            # Enterprising skills
            "Leadership": "Enterprising",
            "Sales": "Enterprising",
            "Negotiation": "Enterprising",
            "Strategic Planning": "Enterprising",
            "Public Speaking": "Enterprising",
            "Business Development": "Enterprising",
            "Marketing": "Enterprising",
            "Project Management": "Enterprising",
            "Entrepreneurship": "Enterprising",
            "Risk Management": "Enterprising",
            
            # Conventional skills
            "Organization": "Conventional",
            "Data Entry": "Conventional",
            "Record Keeping": "Conventional",
            "Quality Control": "Conventional",
            "Process Management": "Conventional",
            "Compliance": "Conventional",
            "Accounting": "Conventional",
            "Documentation": "Conventional",
            "Scheduling": "Conventional",
            "Database Management": "Conventional"
        }
    }

def map_skills_to_riasec(skills_responses: Dict, job_skills_data: Dict) -> Dict[str, float]:
    """Map user's skills confidence to RIASEC types based on job skills data"""
    riasec_types = ['Realistic', 'Investigative', 'Artistic', 'Social', 'Enterprising', 'Conventional']
    riasec_skills_scores = {riasec: [] for riasec in riasec_types}
    
    # Get skill to RIASEC mapping
    skill_mapping = job_skills_data.get('skill_riasec_mapping', {})
    
    # Map each skill response to its RIASEC type
    for skill_name, confidence_level in skills_responses.items():
        # Convert confidence level to numeric score (1-4 scale to 0-5 scale for consistency)
        confidence_map = {
            'Beginner': 1.25,
            'Intermediate': 2.5,
            'Advanced': 3.75,
            'Expert': 5.0,
            1: 1.25,
            2: 2.5,
            3: 3.75,
            4: 5.0
        }
        
        numeric_confidence = confidence_map.get(confidence_level, 2.5)
        
        # Find which RIASEC type this skill belongs to
        riasec_type = skill_mapping.get(skill_name)
        
        if not riasec_type:
            # Try to match by partial name or category
            for mapped_skill, mapped_type in skill_mapping.items():
                if mapped_skill.lower() in skill_name.lower() or skill_name.lower() in mapped_skill.lower():
                    riasec_type = mapped_type
                    break
        
        if riasec_type and riasec_type in riasec_skills_scores:
            riasec_skills_scores[riasec_type].append(numeric_confidence)
    
    # Calculate average confidence for each RIASEC type
    riasec_confidence = {}
    for riasec_type in riasec_types:
        scores = riasec_skills_scores[riasec_type]
        if scores:
            riasec_confidence[riasec_type] = sum(scores) / len(scores)
        else:
            riasec_confidence[riasec_type] = 0.0
    
    return riasec_confidence

def create_comparison_spider_diagram(riasec_scores: Dict[str, float], 
                                   skills_confidence: Dict[str, float]) -> go.Figure:
    """Create spider diagram comparing RIASEC scores with skills confidence"""
    categories = list(riasec_scores.keys())
    
    # Normalize RIASEC scores to 0-5 scale (assuming they come as 0-100)
    riasec_values = [score / 20 for score in riasec_scores.values()]
    skills_values = [skills_confidence.get(cat, 0) for cat in categories]
    
    fig = go.Figure()
    
    # Add RIASEC scores trace
    fig.add_trace(go.Scatterpolar(
        r=riasec_values,
        theta=categories,
        fill='toself',
        name='RIASEC Interests',
        line=dict(color='#3b82f6', width=2),
        fillcolor='rgba(59, 130, 246, 0.2)'
    ))
    
    # Add Skills confidence trace
    fig.add_trace(go.Scatterpolar(
        r=skills_values,
        theta=categories,
        fill='toself',
        name='Skills Confidence',
        line=dict(color='#10b981', width=2),
        fillcolor='rgba(16, 185, 129, 0.2)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5],
                tickmode='linear',
                tick0=0,
                dtick=1
            )),
        showlegend=True,
        title={
            'text': "RIASEC Interests vs Skills Confidence",
            'x': 0.5,
            'xanchor': 'center'
        },
        height=500
    )
    
    return fig

def create_comparison_dataframe(riasec_scores: Dict[str, float], 
                               skills_confidence: Dict[str, float]) -> pd.DataFrame:
    """Create detailed comparison dataframe"""
    data = []
    
    for riasec_type in riasec_scores.keys():
        riasec_score = riasec_scores[riasec_type] / 20  # Normalize to 0-5
        skills_score = skills_confidence.get(riasec_type, 0)
        gap = riasec_score - skills_score
        
        data.append({
            'RIASEC Type': riasec_type,
            'RIASEC Score': round(riasec_score, 2),
            'Skills Confidence': round(skills_score, 2),
            'Gap': round(gap, 2),
            'Alignment': get_alignment_label(gap)
        })
    
    df = pd.DataFrame(data)
    return df

def get_alignment_label(gap: float) -> str:
    """Get alignment label based on gap value"""
    if abs(gap) < 0.5:
        return "✅ Well Aligned"
    elif gap > 0:
        return "📈 Skills Development Needed"
    else:
        return "💼 Underutilized Skills"

def generate_comparison_insights(riasec_scores: Dict[str, float], 
                               skills_confidence: Dict[str, float]) -> List[str]:
    """Generate insights from the comparison"""
    insights = []
    
    # Normalize RIASEC scores
    normalized_riasec = {k: v/20 for k, v in riasec_scores.items()}
    
    # Find biggest gaps
    gaps = {k: normalized_riasec[k] - skills_confidence.get(k, 0) for k in normalized_riasec}
    
    # Overall alignment
    avg_gap = sum(abs(g) for g in gaps.values()) / len(gaps)
    if avg_gap < 0.5:
        insights.append("Your skills align well with your interests overall!")
    elif avg_gap < 1.0:
        insights.append("Moderate alignment between interests and skills")
    else:
        insights.append("Significant gaps between interests and skills")
    
    # Specific insights
    max_positive_gap = max(gaps.items(), key=lambda x: x[1])
    if max_positive_gap[1] > 0.5:
        insights.append(f"Biggest opportunity: Develop {max_positive_gap[0]} skills")
    
    max_negative_gap = min(gaps.items(), key=lambda x: x[1])
    if max_negative_gap[1] < -0.5:
        insights.append(f"Hidden strength: Strong {max_negative_gap[0]} skills")
    
    return insights

def analyze_gaps(riasec_scores: Dict[str, float], 
                skills_confidence: Dict[str, float]) -> Dict[str, List[Dict]]:
    """Analyze gaps between interests and skills"""
    normalized_riasec = {k: v/20 for k, v in riasec_scores.items()}
    
    aligned = []
    opportunities = []
    underutilized = []
    
    # Skills recommendations for each RIASEC type
    skill_recommendations = {
        'Realistic': ['Equipment Operation', 'Technical Drawing', 'Quality Control', 'Safety Procedures'],
        'Investigative': ['Data Analysis', 'Research Methods', 'Statistical Software', 'Scientific Writing'],
        'Artistic': ['Design Software', 'Creative Writing', 'Visual Communication', 'Digital Media'],
        'Social': ['Active Listening', 'Conflict Resolution', 'Group Facilitation', 'Emotional Intelligence'],
        'Enterprising': ['Project Management', 'Financial Analysis', 'Marketing Strategy', 'Negotiation'],
        'Conventional': ['Database Management', 'Spreadsheet Expertise', 'Documentation', 'Compliance']
    }
    
    for riasec_type in normalized_riasec:
        interest_score = normalized_riasec[riasec_type]
        skills_score = skills_confidence.get(riasec_type, 0)
        gap = interest_score - skills_score
        
        if abs(gap) < 0.5 and interest_score > 3.0:
            aligned.append({
                'type': riasec_type,
                'interest': interest_score,
                'skills': skills_score
            })
        elif gap > 1.0:
            opportunities.append({
                'type': riasec_type,
                'interest': interest_score,
                'skills': skills_score,
                'gap': gap,
                'recommended_skills': skill_recommendations.get(riasec_type, [])
            })
        elif gap < -1.0:
            underutilized.append({
                'type': riasec_type,
                'interest': interest_score,
                'skills': skills_score,
                'gap': abs(gap)
            })
    
    return {
        'aligned': aligned,
        'opportunities': opportunities,
        'underutilized': underutilized
    }

def get_aligned_career_recommendations(riasec_scores: Dict[str, float], 
                                     skills_confidence: Dict[str, float],
                                     career_manager: CareerManager) -> List[Dict]:
    """Get career recommendations based on alignment between interests and skills"""
    # Get top RIASEC types where both interest and skills are strong
    normalized_riasec = {k: v/20 for k, v in riasec_scores.items()}
    
    # Calculate alignment scores
    alignment_scores = {}
    for riasec_type in normalized_riasec:
        interest = normalized_riasec[riasec_type]
        skills = skills_confidence.get(riasec_type, 0)
        
        # High alignment when both are high and close together
        if interest > 2.5 and skills > 2.5:
            alignment_scores[riasec_type] = (interest + skills) / 2 - abs(interest - skills)
        else:
            alignment_scores[riasec_type] = 0
    
    # Get top 3 aligned types
    top_aligned = sorted(alignment_scores.items(), key=lambda x: x[1], reverse=True)[:3]
    
    # Mock career recommendations (in real implementation, would query career database)
    career_recommendations = [
        {
            'title': 'Data Scientist',
            'alignment_score': 85,
            'interest_match': 90,
            'skills_match': 80,
            'alignment_reason': 'Strong alignment between Investigative interests and analytical skills',
            'matching_skills': ['Data Analysis', 'Statistical Analysis', 'Problem Solving', 'Research'],
            'skills_to_develop': ['Machine Learning', 'Big Data Tools', 'Data Visualization']
        },
        {
            'title': 'UX Designer',
            'alignment_score': 82,
            'interest_match': 85,
            'skills_match': 79,
            'alignment_reason': 'Good match between Artistic interests and creative skills',
            'matching_skills': ['Creative Design', 'Visual Communication', 'Problem Solving'],
            'skills_to_develop': ['User Research', 'Prototyping Tools', 'Interaction Design']
        },
        {
            'title': 'Project Manager',
            'alignment_score': 78,
            'interest_match': 80,
            'skills_match': 76,
            'alignment_reason': 'Balance of Enterprising and Conventional traits with leadership skills',
            'matching_skills': ['Leadership', 'Organization', 'Communication', 'Strategic Planning'],
            'skills_to_develop': ['Agile Methodologies', 'Risk Management', 'Stakeholder Management']
        }
    ]
    
    return career_recommendations

def generate_comparison_report(riasec_scores: Dict[str, float], 
                             skills_confidence: Dict[str, float],
                             gaps: Dict, careers: List[Dict]) -> str:
    """Generate JSON report of the comparison analysis"""
    report = {
        'timestamp': pd.Timestamp.now().isoformat(),
        'user': SessionStateManager.get('username'),
        'riasec_scores': {k: v/20 for k, v in riasec_scores.items()},
        'skills_confidence': skills_confidence,
        'gap_analysis': gaps,
        'career_recommendations': careers[:3],
        'summary': {
            'overall_alignment': calculate_overall_alignment(riasec_scores, skills_confidence),
            'strongest_alignment': get_strongest_alignment(riasec_scores, skills_confidence),
            'biggest_gap': get_biggest_gap(riasec_scores, skills_confidence)
        }
    }
    
    return json.dumps(report, indent=2)

def calculate_overall_alignment(riasec_scores: Dict[str, float], 
                              skills_confidence: Dict[str, float]) -> float:
    """Calculate overall alignment percentage"""
    normalized_riasec = {k: v/20 for k, v in riasec_scores.items()}
    
    total_gap = 0
    for riasec_type in normalized_riasec:
        interest = normalized_riasec[riasec_type]
        skills = skills_confidence.get(riasec_type, 0)
        total_gap += abs(interest - skills)
    
    # Convert to alignment percentage (inverse of average gap)
    avg_gap = total_gap / len(normalized_riasec)
    alignment = max(0, 100 - (avg_gap * 20))
    
    return round(alignment, 1)

def get_strongest_alignment(riasec_scores: Dict[str, float], 
                          skills_confidence: Dict[str, float]) -> Dict:
    """Find the RIASEC type with strongest alignment"""
    normalized_riasec = {k: v/20 for k, v in riasec_scores.items()}
    
    best_alignment = None
    min_gap = float('inf')
    
    for riasec_type in normalized_riasec:
        interest = normalized_riasec[riasec_type]
        skills = skills_confidence.get(riasec_type, 0)
        gap = abs(interest - skills)
        
        if gap < min_gap and interest > 2.5 and skills > 2.5:
            min_gap = gap
            best_alignment = {
                'type': riasec_type,
                'interest_score': interest,
                'skills_score': skills,
                'gap': gap
            }
    
    return best_alignment

def get_biggest_gap(riasec_scores: Dict[str, float], 
                   skills_confidence: Dict[str, float]) -> Dict:
    """Find the RIASEC type with biggest gap"""
    normalized_riasec = {k: v/20 for k, v in riasec_scores.items()}
    
    biggest_gap = None
    max_gap = 0
    
    for riasec_type in normalized_riasec:
        interest = normalized_riasec[riasec_type]
        skills = skills_confidence.get(riasec_type, 0)
        gap = interest - skills  # Positive means interest > skills
        
        if abs(gap) > abs(max_gap):
            max_gap = gap
            biggest_gap = {
                'type': riasec_type,
                'interest_score': interest,
                'skills_score': skills,
                'gap': gap,
                'direction': 'skills_needed' if gap > 0 else 'underutilized_skills'
            }
    
    return biggest_gap

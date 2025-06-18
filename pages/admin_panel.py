"""
Admin Panel for Career Atlas
Provides administrative functions including CSV data upload
"""

import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import io
from utils.session_state import SessionStateManager
from utils.csv_validator import CSVValidator
from utils.csv_templates import CSVTemplateGenerator

def show_admin_panel():
    """Display the admin panel"""
    st.title("🔧 Admin Panel")
    
    # Check admin access
    if SessionStateManager.get('role') != 'admin':
        st.error("⚠️ Access Denied: Admin privileges required")
        if st.button("← Back to Dashboard"):
            SessionStateManager.navigate_to('welcome')
        return
    
    # Create tabs for different admin functions
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Dashboard", 
        "📤 CSV Upload", 
        "👥 User Management", 
        "⚙️ System Settings"
    ])
    
    with tab1:
        show_admin_dashboard()
    
    with tab2:
        show_csv_upload()
    
    with tab3:
        show_user_management()
    
    with tab4:
        show_system_settings()

def show_admin_dashboard():
    """Display admin dashboard with statistics"""
    st.header("System Overview")
    
    # Display key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Users", "2", "Active")
        
    with col2:
        st.metric("Assessments", "0", "Completed")
        
    with col3:
        st.metric("Job Roles", count_job_roles(), "Available")
        
    with col4:
        st.metric("Skills", count_skills(), "Defined")
    
    # Recent activity
    st.subheader("Recent Activity")
    st.info("No recent activity to display")

def show_csv_upload():
    """Display CSV upload interface"""
    st.header("CSV Data Upload")
    
    st.markdown("""
    Upload CSV files to update the system's job roles, skills, and competency data.
    All existing data will be replaced with the uploaded content.
    """)
    
    # File type selection
    file_types = {
        "Job Role Description": "job_roles",
        "Job Role-Critical Work Function-Key Tasks": "job_tasks",
        "Job Role-Skills": "job_skills",
        "TSC_CCS_Key (Skills Master)": "skills_master",
        "TSC_CCS_K&A (Knowledge & Abilities)": "skills_ka"
    }
    
    selected_type = st.selectbox(
        "Select file type to upload:",
        options=list(file_types.keys()),
        help="Choose the type of data you want to upload"
    )
    
    # Show expected columns for selected type
    show_expected_columns(selected_type)
    
    # Template download section
    col1, col2 = st.columns([3, 1])
    with col1:
        st.info("💡 Download a template file to see the expected format")
    with col2:
        if st.button("📥 Download Template", type="secondary"):
            download_template(selected_type)
    
    # File upload
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=['csv'],
        help="Select a CSV file matching the expected format"
    )
    
    if uploaded_file is not None:
        # Read and validate the file
        try:
            df = pd.read_csv(uploaded_file)
            
            # Show preview
            st.subheader("📋 Data Preview")
            st.write(f"**Rows:** {len(df)} | **Columns:** {len(df.columns)}")
            
            # Display first 5 rows
            st.dataframe(df.head(), use_container_width=True)
            
            # Validate the data
            validator = CSVValidator()
            validation_result = validator.validate(selected_type, df)
            
            if validation_result['valid']:
                st.success("✅ Validation passed! Data is ready to upload.")
                
                # Show validation summary
                with st.expander("Validation Summary"):
                    st.json(validation_result['summary'])
                
                # Upload confirmation
                st.warning("⚠️ **Warning:** Uploading will replace all existing data for this type!")
                
                col1, col2, col3 = st.columns([1, 1, 3])
                with col1:
                    if st.button("📤 Confirm Upload", type="primary"):
                        if process_csv_upload(selected_type, df):
                            st.success("✅ Data uploaded successfully!")
                            st.balloons()
                            st.rerun()
                
                with col2:
                    if st.button("❌ Cancel"):
                        st.rerun()
            else:
                st.error("❌ Validation failed! Please fix the following issues:")
                
                # Show validation errors
                for error in validation_result['errors']:
                    st.error(f"• {error}")
                
                # Show detailed error report if available
                if 'details' in validation_result:
                    with st.expander("Detailed Error Report"):
                        for detail in validation_result['details']:
                            st.write(f"**Row {detail['row']}:** {detail['message']}")
                            
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")
            st.info("Please ensure the file is a valid CSV with UTF-8 encoding")

def show_expected_columns(file_type: str):
    """Display expected columns for each file type"""
    expected_columns = {
        "Job Role Description": [
            "Sector", "Track", "Job Role", "Job Role Description"
        ],
        "Job Role-Critical Work Function-Key Tasks": [
            "Sector", "Track", "Job Role", "Critical Work Function", "Key Tasks"
        ],
        "Job Role-Skills": [
            "Sector", "Track", "Job Role", "TSC_CCS Title", "TSC_CCS Type", "Proficiency Level"
        ],
        "TSC_CCS_Key (Skills Master)": [
            "TSC Code", "Sector", "TSC_CCS Category", "TSC_CCS Title", 
            "TSC_CCS Description", "TSC_CCS Type"
        ],
        "TSC_CCS_K&A (Knowledge & Abilities)": [
            "Sector", "TSC_CCS Category", "TSC_CCS Title", "TSC_CCS Description",
            "Proficiency Level", "Proficiency Description", 
            "Knowledge-Ability Classification", "Knowledge-Ability Items"
        ]
    }
    
    with st.expander("📋 Expected Columns"):
        columns = expected_columns.get(file_type, [])
        st.write("Your CSV file must contain these columns (in any order):")
        for i, col in enumerate(columns, 1):
            st.write(f"{i}. **{col}**")

def download_template(file_type: str):
    """Generate and download a template CSV file"""
    generator = CSVTemplateGenerator()
    template_df = generator.generate_template(file_type)
    
    if template_df is not None:
        csv = template_df.to_csv(index=False)
        filename = f"{file_type.lower().replace(' ', '_').replace('-', '_')}_template.csv"
        
        st.download_button(
            label="📥 Download Template",
            data=csv,
            file_name=filename,
            mime="text/csv"
        )

def process_csv_upload(file_type: str, df: pd.DataFrame) -> bool:
    """Process the uploaded CSV and save to appropriate location"""
    try:
        # Map file types to storage locations
        storage_map = {
            "Job Role Description": "data/careers/job_roles.json",
            "Job Role-Critical Work Function-Key Tasks": "data/careers/job_tasks.json",
            "Job Role-Skills": "data/careers/job_skills.json",
            "TSC_CCS_Key (Skills Master)": "data/skills/skills_master.json",
            "TSC_CCS_K&A (Knowledge & Abilities)": "data/skills/skills_ka.json"
        }
        
        # Convert DataFrame to appropriate JSON structure
        if file_type == "Job Role Description":
            data = convert_job_roles_to_json(df)
        elif file_type == "Job Role-Critical Work Function-Key Tasks":
            data = convert_job_tasks_to_json(df)
        elif file_type == "Job Role-Skills":
            data = convert_job_skills_to_json(df)
        elif file_type == "TSC_CCS_Key (Skills Master)":
            data = convert_skills_master_to_json(df)
        elif file_type == "TSC_CCS_K&A (Knowledge & Abilities)":
            data = convert_skills_ka_to_json(df)
        else:
            return False
        
        # Save to file
        filepath = storage_map[file_type]
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        # Log the upload
        log_upload(file_type, len(df))
        
        return True
        
    except Exception as e:
        st.error(f"Error processing upload: {str(e)}")
        return False

def convert_job_roles_to_json(df: pd.DataFrame) -> Dict:
    """Convert job roles DataFrame to JSON structure"""
    data = {
        "last_updated": datetime.now().isoformat(),
        "job_roles": []
    }
    
    for _, row in df.iterrows():
        data["job_roles"].append({
            "sector": row["Sector"],
            "track": row["Track"],
            "job_role": row["Job Role"],
            "description": row["Job Role Description"]
        })
    
    return data

def convert_job_tasks_to_json(df: pd.DataFrame) -> Dict:
    """Convert job tasks DataFrame to JSON structure"""
    data = {
        "last_updated": datetime.now().isoformat(),
        "job_tasks": []
    }
    
    for _, row in df.iterrows():
        data["job_tasks"].append({
            "sector": row["Sector"],
            "track": row["Track"],
            "job_role": row["Job Role"],
            "critical_work_function": row["Critical Work Function"],
            "key_tasks": row["Key Tasks"]
        })
    
    return data

def convert_job_skills_to_json(df: pd.DataFrame) -> Dict:
    """Convert job skills DataFrame to JSON structure"""
    data = {
        "last_updated": datetime.now().isoformat(),
        "job_skills": []
    }
    
    for _, row in df.iterrows():
        data["job_skills"].append({
            "sector": row["Sector"],
            "track": row["Track"],
            "job_role": row["Job Role"],
            "skill_title": row["TSC_CCS Title"],
            "skill_type": row["TSC_CCS Type"],
            "proficiency_level": row["Proficiency Level"]
        })
    
    return data

def convert_skills_master_to_json(df: pd.DataFrame) -> Dict:
    """Convert skills master DataFrame to JSON structure"""
    data = {
        "last_updated": datetime.now().isoformat(),
        "skills": []
    }
    
    for _, row in df.iterrows():
        data["skills"].append({
            "tsc_code": row["TSC Code"],
            "sector": row["Sector"],
            "category": row["TSC_CCS Category"],
            "title": row["TSC_CCS Title"],
            "description": row["TSC_CCS Description"],
            "type": row["TSC_CCS Type"]
        })
    
    return data

def convert_skills_ka_to_json(df: pd.DataFrame) -> Dict:
    """Convert skills K&A DataFrame to JSON structure"""
    data = {
        "last_updated": datetime.now().isoformat(),
        "knowledge_abilities": []
    }
    
    for _, row in df.iterrows():
        data["knowledge_abilities"].append({
            "sector": row["Sector"],
            "category": row["TSC_CCS Category"],
            "title": row["TSC_CCS Title"],
            "description": row["TSC_CCS Description"],
            "proficiency_level": row["Proficiency Level"],
            "proficiency_description": row["Proficiency Description"],
            "classification": row["Knowledge-Ability Classification"],
            "items": row["Knowledge-Ability Items"]
        })
    
    return data

def log_upload(file_type: str, row_count: int):
    """Log CSV upload activity"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "user": SessionStateManager.get('username'),
        "action": "csv_upload",
        "file_type": file_type,
        "row_count": row_count
    }
    
    # Create logs directory if it doesn't exist
    os.makedirs("data/logs", exist_ok=True)
    
    # Append to log file
    log_file = "data/logs/admin_activity.json"
    logs = []
    
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            logs = json.load(f)
    
    logs.append(log_entry)
    
    with open(log_file, 'w') as f:
        json.dump(logs, f, indent=2)

def count_job_roles() -> int:
    """Count total job roles in the system"""
    try:
        if os.path.exists("data/careers/job_roles.json"):
            with open("data/careers/job_roles.json", 'r') as f:
                data = json.load(f)
                return len(data.get("job_roles", []))
    except:
        pass
    return 0

def count_skills() -> int:
    """Count total skills in the system"""
    try:
        if os.path.exists("data/skills/skills_master.json"):
            with open("data/skills/skills_master.json", 'r') as f:
                data = json.load(f)
                return len(data.get("skills", []))
    except:
        pass
    return 0

def show_user_management():
    """Display user management interface"""
    st.header("User Management")
    
    # Display current users
    st.subheader("Current Users")
    
    users_data = [
        {"Username": "admin", "Name": "Administrator", "Role": "admin", "Status": "Active"},
        {"Username": "demo", "Name": "Demo User", "Role": "user", "Status": "Active"}
    ]
    
    df = pd.DataFrame(users_data)
    st.dataframe(df, use_container_width=True)
    
    st.info("User management features are currently limited to viewing existing users.")

def show_system_settings():
    """Display system settings"""
    st.header("System Settings")
    
    st.subheader("Data Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Current Data Files:**")
        data_files = [
            "Job Roles", "Job Tasks", "Job Skills", 
            "Skills Master", "Skills K&A"
        ]
        for file in data_files:
            st.write(f"• {file}")
    
    with col2:
        st.write("**System Status:**")
        st.success("✅ All systems operational")
    
    st.subheader("Backup & Restore")
    st.info("Backup and restore features coming soon")

"""
CSV Validator for Career Atlas
Validates uploaded CSV files according to defined rules
"""

import pandas as pd
from typing import Dict, List, Tuple, Optional
import re

class CSVValidator:
    """Validates CSV files for different data types"""
    
    def __init__(self):
        self.proficiency_levels_numeric = [1, 2, 3, 4, 5]
        self.proficiency_levels_text = [
            "Basic", "Intermediate", "Advanced", "Expert", "Master",
            "Beginner", "Competent", "Proficient"
        ]
        self.skill_types = ["Technical Skills", "Core Competencies"]
        self.ka_classifications = ["Knowledge", "Ability"]
    
    def validate(self, file_type: str, df: pd.DataFrame) -> Dict:
        """
        Validate a DataFrame based on file type
        
        Returns:
            Dict with 'valid' boolean, 'errors' list, and 'summary' dict
        """
        validators = {
            "Job Role Description": self.validate_job_roles,
            "Job Role-Critical Work Function-Key Tasks": self.validate_job_tasks,
            "Job Role-Skills": self.validate_job_skills,
            "TSC_CCS_Key (Skills Master)": self.validate_skills_master,
            "TSC_CCS_K&A (Knowledge & Abilities)": self.validate_skills_ka
        }
        
        validator_func = validators.get(file_type)
        if not validator_func:
            return {
                'valid': False,
                'errors': [f"Unknown file type: {file_type}"],
                'summary': {}
            }
        
        return validator_func(df)
    
    def validate_job_roles(self, df: pd.DataFrame) -> Dict:
        """Validate Job Role Description CSV"""
        errors = []
        details = []
        
        # Check required columns
        required_columns = ["Sector", "Track", "Job Role", "Job Role Description"]
        missing_columns = self.check_required_columns(df, required_columns)
        if missing_columns:
            errors.append(f"Missing required columns: {', '.join(missing_columns)}")
            return {'valid': False, 'errors': errors, 'summary': {}}
        
        # Validate each row
        for idx, row in df.iterrows():
            row_num = idx + 2  # Account for header row
            
            # Check for empty values
            for col in required_columns:
                if pd.isna(row[col]) or str(row[col]).strip() == "":
                    details.append({
                        'row': row_num,
                        'message': f"Empty value in column '{col}'"
                    })
            
            # Check description length
            if not pd.isna(row["Job Role Description"]) and len(str(row["Job Role Description"])) < 10:
                details.append({
                    'row': row_num,
                    'message': "Job Role Description must be at least 10 characters"
                })
        
        # Check for duplicate job roles within same sector/track
        duplicates = df.groupby(['Sector', 'Track', 'Job Role']).size()
        duplicate_roles = duplicates[duplicates > 1]
        if not duplicate_roles.empty:
            for (sector, track, role), count in duplicate_roles.items():
                errors.append(f"Duplicate job role '{role}' in {sector}/{track} ({count} occurrences)")
        
        # Compile results
        if errors or details:
            return {
                'valid': False,
                'errors': errors,
                'details': details,
                'summary': {
                    'total_rows': len(df),
                    'error_count': len(errors) + len(details)
                }
            }
        
        return {
            'valid': True,
            'errors': [],
            'summary': {
                'total_rows': len(df),
                'unique_sectors': df['Sector'].nunique(),
                'unique_tracks': df['Track'].nunique(),
                'unique_roles': df['Job Role'].nunique()
            }
        }
    
    def validate_job_tasks(self, df: pd.DataFrame) -> Dict:
        """Validate Job Role-Critical Work Function-Key Tasks CSV"""
        errors = []
        details = []
        
        # Check required columns
        required_columns = ["Sector", "Track", "Job Role", "Critical Work Function", "Key Tasks"]
        missing_columns = self.check_required_columns(df, required_columns)
        if missing_columns:
            errors.append(f"Missing required columns: {', '.join(missing_columns)}")
            return {'valid': False, 'errors': errors, 'summary': {}}
        
        # Load existing job roles for validation
        existing_roles = self.load_existing_job_roles()
        
        # Validate each row
        for idx, row in df.iterrows():
            row_num = idx + 2
            
            # Check for empty values
            for col in required_columns:
                if pd.isna(row[col]) or str(row[col]).strip() == "":
                    details.append({
                        'row': row_num,
                        'message': f"Empty value in column '{col}'"
                    })
            
            # Validate job role exists
            role_key = f"{row['Sector']}|{row['Track']}|{row['Job Role']}"
            if existing_roles and role_key not in existing_roles:
                details.append({
                    'row': row_num,
                    'message': f"Job role '{row['Job Role']}' not found in {row['Sector']}/{row['Track']}"
                })
        
        # Compile results
        if errors or details:
            return {
                'valid': False,
                'errors': errors,
                'details': details,
                'summary': {
                    'total_rows': len(df),
                    'error_count': len(errors) + len(details)
                }
            }
        
        return {
            'valid': True,
            'errors': [],
            'summary': {
                'total_rows': len(df),
                'unique_functions': df['Critical Work Function'].nunique()
            }
        }
    
    def validate_job_skills(self, df: pd.DataFrame) -> Dict:
        """Validate Job Role-Skills CSV"""
        errors = []
        details = []
        
        # Check required columns
        required_columns = ["Sector", "Track", "Job Role", "TSC_CCS Title", 
                          "TSC_CCS Type", "Proficiency Level"]
        missing_columns = self.check_required_columns(df, required_columns)
        if missing_columns:
            errors.append(f"Missing required columns: {', '.join(missing_columns)}")
            return {'valid': False, 'errors': errors, 'summary': {}}
        
        # Load existing data for validation
        existing_roles = self.load_existing_job_roles()
        existing_skills = self.load_existing_skills()
        
        # Validate each row
        for idx, row in df.iterrows():
            row_num = idx + 2
            
            # Check for empty values
            for col in required_columns:
                if pd.isna(row[col]) or str(row[col]).strip() == "":
                    details.append({
                        'row': row_num,
                        'message': f"Empty value in column '{col}'"
                    })
            
            # Validate job role exists
            role_key = f"{row['Sector']}|{row['Track']}|{row['Job Role']}"
            if existing_roles and role_key not in existing_roles:
                details.append({
                    'row': row_num,
                    'message': f"Job role '{row['Job Role']}' not found"
                })
            
            # Validate skill exists
            if existing_skills and row['TSC_CCS Title'] not in existing_skills:
                details.append({
                    'row': row_num,
                    'message': f"Skill '{row['TSC_CCS Title']}' not found in skills master"
                })
            
            # Validate skill type
            if row['TSC_CCS Type'] not in self.skill_types:
                details.append({
                    'row': row_num,
                    'message': f"Invalid skill type '{row['TSC_CCS Type']}'. Must be one of: {', '.join(self.skill_types)}"
                })
            
            # Validate proficiency level
            if not self.validate_proficiency_level(row['Proficiency Level']):
                details.append({
                    'row': row_num,
                    'message': f"Invalid proficiency level '{row['Proficiency Level']}'. Must be 1-5 or Basic/Intermediate/Advanced/etc."
                })
        
        # Compile results
        if errors or details:
            return {
                'valid': False,
                'errors': errors,
                'details': details,
                'summary': {
                    'total_rows': len(df),
                    'error_count': len(errors) + len(details)
                }
            }
        
        return {
            'valid': True,
            'errors': [],
            'summary': {
                'total_rows': len(df),
                'unique_skills': df['TSC_CCS Title'].nunique()
            }
        }
    
    def validate_skills_master(self, df: pd.DataFrame) -> Dict:
        """Validate TSC_CCS_Key (Skills Master) CSV"""
        errors = []
        details = []
        
        # Check required columns
        required_columns = ["TSC Code", "Sector", "TSC_CCS Category", 
                          "TSC_CCS Title", "TSC_CCS Description", "TSC_CCS Type"]
        missing_columns = self.check_required_columns(df, required_columns)
        if missing_columns:
            errors.append(f"Missing required columns: {', '.join(missing_columns)}")
            return {'valid': False, 'errors': errors, 'summary': {}}
        
        # Check for duplicate TSC codes
        duplicate_codes = df['TSC Code'].duplicated()
        if duplicate_codes.any():
            dup_values = df[duplicate_codes]['TSC Code'].unique()
            errors.append(f"Duplicate TSC Codes found: {', '.join(dup_values)}")
        
        # Validate each row
        for idx, row in df.iterrows():
            row_num = idx + 2
            
            # Check for empty values
            for col in required_columns:
                if pd.isna(row[col]) or str(row[col]).strip() == "":
                    details.append({
                        'row': row_num,
                        'message': f"Empty value in column '{col}'"
                    })
            
            # Validate TSC code format (optional - you can define a pattern)
            if not pd.isna(row['TSC Code']) and not self.validate_tsc_code(row['TSC Code']):
                details.append({
                    'row': row_num,
                    'message': f"Invalid TSC Code format: '{row['TSC Code']}'"
                })
            
            # Validate skill type
            if row['TSC_CCS Type'] not in self.skill_types:
                details.append({
                    'row': row_num,
                    'message': f"Invalid skill type '{row['TSC_CCS Type']}'"
                })
        
        # Check for duplicate skill titles within sector
        duplicates = df.groupby(['Sector', 'TSC_CCS Title']).size()
        duplicate_skills = duplicates[duplicates > 1]
        if not duplicate_skills.empty:
            for (sector, title), count in duplicate_skills.items():
                errors.append(f"Duplicate skill '{title}' in sector '{sector}' ({count} occurrences)")
        
        # Compile results
        if errors or details:
            return {
                'valid': False,
                'errors': errors,
                'details': details,
                'summary': {
                    'total_rows': len(df),
                    'error_count': len(errors) + len(details)
                }
            }
        
        return {
            'valid': True,
            'errors': [],
            'summary': {
                'total_rows': len(df),
                'unique_codes': df['TSC Code'].nunique(),
                'unique_categories': df['TSC_CCS Category'].nunique()
            }
        }
    
    def validate_skills_ka(self, df: pd.DataFrame) -> Dict:
        """Validate TSC_CCS_K&A (Knowledge & Abilities) CSV"""
        errors = []
        details = []
        
        # Check required columns
        required_columns = ["Sector", "TSC_CCS Category", "TSC_CCS Title", 
                          "TSC_CCS Description", "Proficiency Level", 
                          "Proficiency Description", "Knowledge-Ability Classification", 
                          "Knowledge-Ability Items"]
        missing_columns = self.check_required_columns(df, required_columns)
        if missing_columns:
            errors.append(f"Missing required columns: {', '.join(missing_columns)}")
            return {'valid': False, 'errors': errors, 'summary': {}}
        
        # Load existing skills for validation
        existing_skills = self.load_existing_skills()
        
        # Validate each row
        for idx, row in df.iterrows():
            row_num = idx + 2
            
            # Check for empty values
            for col in required_columns:
                if pd.isna(row[col]) or str(row[col]).strip() == "":
                    details.append({
                        'row': row_num,
                        'message': f"Empty value in column '{col}'"
                    })
            
            # Validate skill exists
            if existing_skills and row['TSC_CCS Title'] not in existing_skills:
                details.append({
                    'row': row_num,
                    'message': f"Skill '{row['TSC_CCS Title']}' not found in skills master"
                })
            
            # Validate proficiency level
            if not self.validate_proficiency_level(row['Proficiency Level']):
                details.append({
                    'row': row_num,
                    'message': f"Invalid proficiency level '{row['Proficiency Level']}'"
                })
            
            # Validate K-A classification
            if row['Knowledge-Ability Classification'] not in self.ka_classifications:
                details.append({
                    'row': row_num,
                    'message': f"Invalid classification '{row['Knowledge-Ability Classification']}'. Must be Knowledge or Ability"
                })
        
        # Compile results
        if errors or details:
            return {
                'valid': False,
                'errors': errors,
                'details': details,
                'summary': {
                    'total_rows': len(df),
                    'error_count': len(errors) + len(details)
                }
            }
        
        return {
            'valid': True,
            'errors': [],
            'summary': {
                'total_rows': len(df),
                'knowledge_items': len(df[df['Knowledge-Ability Classification'] == 'Knowledge']),
                'ability_items': len(df[df['Knowledge-Ability Classification'] == 'Ability'])
            }
        }
    
    def check_required_columns(self, df: pd.DataFrame, required: List[str]) -> List[str]:
        """Check if all required columns are present"""
        missing = []
        for col in required:
            if col not in df.columns:
                missing.append(col)
        return missing
    
    def validate_proficiency_level(self, value) -> bool:
        """Validate proficiency level (numeric or text)"""
        if pd.isna(value):
            return False
        
        # Check numeric
        try:
            num_val = int(value)
            return num_val in self.proficiency_levels_numeric
        except:
            pass
        
        # Check text
        return str(value).strip() in self.proficiency_levels_text
    
    def validate_tsc_code(self, code: str) -> bool:
        """Validate TSC code format"""
        # Example pattern: TS001, CC001, etc.
        pattern = r'^[A-Z]{2}\d{3}$'
        return bool(re.match(pattern, str(code).strip()))
    
    def load_existing_job_roles(self) -> set:
        """Load existing job roles for validation"""
        try:
            import json
            import os
            
            if os.path.exists("data/careers/job_roles.json"):
                with open("data/careers/job_roles.json", 'r') as f:
                    data = json.load(f)
                    roles = set()
                    for role in data.get("job_roles", []):
                        key = f"{role['sector']}|{role['track']}|{role['job_role']}"
                        roles.add(key)
                    return roles
        except:
            pass
        return set()
    
    def load_existing_skills(self) -> set:
        """Load existing skills for validation"""
        try:
            import json
            import os
            
            if os.path.exists("data/skills/skills_master.json"):
                with open("data/skills/skills_master.json", 'r') as f:
                    data = json.load(f)
                    return {skill['title'] for skill in data.get("skills", [])}
        except:
            pass
        return set()

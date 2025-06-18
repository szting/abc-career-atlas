# Career Assessment Tool

A comprehensive career guidance application with RIASEC personality assessment, skills evaluation, work values analysis, and personalized coaching.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Recent Fixes](#recent-fixes)
- [Streamlit Implementation](#streamlit-implementation)
- [Customizing Career Frameworks](#customizing-career-frameworks)
  - [Career Paths](#career-paths)
  - [RIASEC Questions](#riasec-questions)
  - [Skills Assessment](#skills-assessment)
  - [Work Values](#work-values)
  - [Coaching Questions](#coaching-questions)
- [File Upload System](#file-upload-system)
- [API Integration](#api-integration)

## Overview

This Career Assessment Tool helps users discover suitable career paths based on their personality traits (RIASEC model), skills confidence, and work values. The application supports multiple user personas (Individual, Career Coach, Manager) and includes an admin panel for customization.

## Features

- **Multi-persona System**: Different interfaces for individuals, career coaches, and managers
- **Comprehensive Assessments**: RIASEC personality test, skills confidence evaluation, and work values prioritization
- **Career Matching Algorithm**: Matches user profiles with suitable career paths
- **Coaching Dashboard**: Provides personalized coaching questions based on RIASEC profile
- **Manager Dashboard**: Offers team development insights and reflection questions
- **Admin Panel**: Allows customization of assessment content, API keys, and data visualization
- **Data Visualization**: Spider diagrams for RIASEC profiles and skills confidence
- **Password Protection**: Simple authentication system to secure access

## Recent Fixes

### Part 1: Password Authentication Fix (Completed)

**Issue**: Password page was not displaying in Preview despite authentication code being present.

**Root Cause**: The authentication check was happening but the main app content was still rendering because Streamlit's execution flow wasn't properly stopped when authentication failed.

**Fix Implemented**:
1. Added `st.stop()` immediately after the authentication check in `app.py` to halt execution when not authenticated
2. Enhanced the logout function to clear all session state except authentication status
3. Added a unique key to the password input field to prevent caching issues
4. Ensured authentication state is initialized before any other session state variables

**Files Modified**:
- `app.py`: Added `st.stop()` after authentication check
- `utils/simple_auth.py`: Enhanced logout function and added input field key
- `utils/session_state.py`: Ensured authentication state initializes first

**Result**: The password page now displays properly and blocks access to the application until the correct password ("Cl@r1tyC2r3r") is entered.

### Part 2: RIASEC Analytics Update Fix (Completed)

**Issue**: RIASEC assessment results were not showing in the analytics panel after completing an assessment.

**Root Cause**: The analytics panel was only checking for the existence of data without verifying if the data had actual values. Empty RIASEC scores (all zeros) were being treated as valid data.

**Fix Implemented**:
1. Added proper validation to check if RIASEC scores have actual values (not just zeros)
2. Enhanced the analytics display to show:
   - Actual score values with progress bars
   - Top interest areas with descriptions
   - Detailed assessment progress indicators
   - Skills confidence summary with categorization
   - Work values display in a cleaner format
3. Added informative messages when no data is available
4. Improved data visualization with progress bars and better formatting

**Files Modified**:
- `pages/admin_panel.py`: Complete overhaul of the analytics section with:
  - Validation for actual assessment data
  - Enhanced RIASEC score display with progress bars
  - Skills categorization (technical, soft skills, other)
  - Better progress tracking
  - Clearer user information display

**Result**: The analytics panel now properly displays RIASEC results and other assessment data when available, with clear indicators of progress and helpful messages when data is not yet available.

## Streamlit Implementation

The Streamlit implementation consists of the following components:

### Core Streamlit Files

- **`app.py`**: Main application entry point that handles routing between different pages
- **`utils/session_state.py`**: Manages session state for user data persistence
- **`utils/simple_auth.py`**: Handles password authentication and session management
- **`utils/career_matcher.py`**: Algorithm for matching user profiles with career paths

### Streamlit Page Components

- **`pages/persona_selection.py`**: Initial page for selecting user persona (Individual/Coach/Manager)
- **`pages/welcome.py`**: Welcome screen with assessment overview
- **`pages/riasec_assessment.py`**: RIASEC personality assessment
- **`pages/skills_assessment.py`**: Skills confidence evaluation
- **`pages/values_assessment.py`**: Work values prioritization
- **`pages/results.py`**: Results page showing career matches and RIASEC profile
- **`pages/coaching_dashboard.py`**: Coaching interface with personalized questions
- **`pages/manager_dashboard.py`**: Manager interface with team insights
- **`pages/admin_panel.py`**: Admin interface for customization and settings

### Data Files

- **`data/careers.py`**: Career paths database
- **`data/riasec_questions.py`**: RIASEC assessment questions
- **`data/skills_list.py`**: Skills assessment categories and items
- **`data/work_values.py`**: Work values definitions and descriptions
- **`data/coaching_questions.py`**: Coaching questions framework

## Customizing Career Frameworks

### Career Paths

The career paths database is defined in `data/careers.py`. Each career entry follows this structure:

```python
{
    'id': 'unique-identifier',
    'title': 'Career Title',
    'description': 'Brief description of the career',
    'primary_type': 'primary-riasec-type',  # One of: realistic, investigative, artistic, social, enterprising, conventional
    'secondary_type': 'secondary-riasec-type',  # Optional secondary RIASEC type
    'required_skills': ['Skill1', 'Skill2', 'Skill3'],  # List of key skills
    'work_environment': ['Environment1', 'Environment2'],  # Work settings
    'salary_range': '$X - $Y',  # Typical salary range
    'growth_outlook': 'Growth projection',  # Job market outlook
    'education': 'Required education'  # Typical education requirements
}
```

To customize:
1. Add new career entries following the structure above
2. Ensure each career has a unique `id`
3. Assign appropriate RIASEC types as `primary_type` and `secondary_type`
4. List required skills that match or closely relate to skills in the skills assessment
5. Include relevant work environments that might align with work values

**Important**: The career matching algorithm in `utils/career_matcher.py` uses the RIASEC types, required skills, and work environment to calculate matches. Ensure these fields are properly populated for accurate matching.

### RIASEC Questions

RIASEC assessment questions are defined in a separate file (not shown in the provided code). The expected structure is:

```python
riasec_questions = [
    {
        'id': 'question-id',
        'text': 'Question text',
        'type': 'riasec-type'  # One of: realistic, investigative, artistic, social, enterprising, conventional
    },
    # More questions...
]
```

To customize:
1. Maintain a balanced number of questions for each RIASEC type
2. Ensure questions clearly reflect the characteristics of their assigned type
3. Keep questions concise and easy to understand
4. Avoid biased language that might favor certain demographics

### Skills Assessment

The skills assessment framework should be organized by categories:

```python
skills_categories = [
    {
        'name': 'Category Name',
        'skills': ['Skill 1', 'Skill 2', 'Skill 3']
    },
    # More categories...
]
```

To customize:
1. Group related skills into logical categories
2. Keep skill names concise and specific
3. Include skills relevant to various career paths in your database
4. Ensure a balanced representation across different fields

### Work Values

Work values are defined as a list of options with descriptions:

```python
work_values = [
    {
        'name': 'Value Name',
        'description': 'Brief description of the value'
    },
    # More values...
]
```

To customize:
1. Include a diverse range of work values
2. Provide clear, concise descriptions
3. Ensure values align with the keywords used in the career matching algorithm
4. Consider cultural and generational differences in work values

### Coaching Questions

Coaching questions are defined in `data/coaching_questions.py` with the following structure:

```python
coaching_questions = [
    {
        'id': 'question-id',
        'category': 'category-name',  # e.g., exploration, development, goal-setting, reflection
        'riasecFocus': 'riasec-type',  # The RIASEC type this question targets
        'question': 'The main coaching question',
        'purpose': 'Brief explanation of the question purpose',
        'followUp': ['Follow-up question 1', 'Follow-up question 2']  # Optional follow-up questions
    },
    # More questions...
]
```

To customize:
1. Create questions for each RIASEC type and category
2. Ensure questions are open-ended and thought-provoking
3. Include a clear purpose for each question
4. Add relevant follow-up questions to deepen the conversation
5. Use language appropriate for coaching conversations

## File Upload System

The admin panel includes a file upload system for updating the career frameworks. When uploading files:

1. Files must be in the correct format (JSON or Python)
2. The system validates the structure of uploaded files
3. Templates are available for download to ensure correct formatting
4. Uploaded files replace the existing frameworks after validation

File upload templates follow the structures outlined in the customization sections above.

## API Integration

The application can integrate with OpenAI's API for enhanced coaching responses. To configure:

1. Access the Admin Panel
2. Navigate to the API Settings section
3. Enter your OpenAI API key
4. Test the connection before saving
5. Configure fallback responses for when the API is unavailable

The API integration enhances the coaching experience by generating personalized follow-up questions and insights based on the user's RIASEC profile and responses.

---

## Development Notes

### Adding New Career Paths

When adding new career paths, ensure they include:

1. Accurate RIASEC type classifications
2. Skills that match or closely relate to the skills assessment options
3. Work environment descriptions that contain keywords related to work values
4. Comprehensive metadata (salary, education, growth outlook)

The career matching algorithm weighs RIASEC alignment at 40%, skills matching at 35%, and work values alignment at 25%.

### Extending the Assessment

To add new assessment types:

1. Create a new page module in the `pages` directory
2. Define the assessment questions/items in the `data` directory
3. Update the session state initialization in `utils/session_state.py`
4. Add the new step to the navigation flow in `app.py`
5. Update the career matching algorithm if needed

# Career Atlas - AI-Powered Career Guidance Platform

A comprehensive career assessment and guidance application built with Streamlit, featuring RIASEC personality assessment, skills evaluation, work values analysis, and AI-powered personalized coaching. Now available as a Progressive Web App (PWA) with offline support!

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [How It Works](#how-it-works)
- [Technical Architecture](#technical-architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [User Guide](#user-guide)
- [Code Structure](#code-structure)
- [Implementation Status](#implementation-status)
- [API Documentation](#api-documentation)
- [Customization Guide](#customization-guide)
- [Troubleshooting](#troubleshooting)

## Overview

Career Atlas is an intelligent career guidance system that helps users discover their ideal career paths through scientifically-backed assessments and AI-powered recommendations. Think of it as having a personal career counselor available 24/7, now accessible as a mobile app!

### What Makes Career Atlas Special?

- **Science-Based**: Uses the proven RIASEC (Holland Code) model for personality assessment
- **AI-Enhanced**: Leverages multiple AI providers (OpenAI, Anthropic, Google) with automatic fallback
- **Multi-User Support**: Different interfaces for individuals, coaches, and managers
- **Comprehensive**: Covers personality, skills, values, career matching, and learning paths
- **Smart Learning**: Personalized learning recommendations with progress tracking
- **Data-Driven**: Advanced analytics and insights for career development
- **CSV Data Management**: Bulk upload capability for job roles, skills, and competencies
- **Progressive Web App**: Install as a native app on any device with offline support
- **Visual Comparisons**: Spider diagram visualization comparing RIASEC scores with skills confidence

## Features

### For Individuals
- **RIASEC Personality Assessment**: Discover your Holland Code through interactive questions
- **Skills Confidence Evaluation**: Rate your confidence across various skill categories
- **Work Values Prioritization**: Identify what matters most in your ideal workplace
- **AI-Powered Career Matching**: Get personalized career recommendations based on your profile
- **Smart Learning Paths**: Receive customized learning recommendations and track progress
- **Development Planning**: Get actionable steps to reach your career goals
- **Visual Analytics**: See your results through interactive charts and graphs
- **Progress Tracking**: Monitor your learning journey with streaks and statistics
- **RIASEC vs Skills Comparison**: NEW! Visual spider diagram comparing personality interests with skills confidence
- **Gap Analysis**: Identify alignment between interests and skills for better career planning

### For Career Coaches
- **Client Dashboard**: Access coaching questions tailored to each client's RIASEC profile
- **Guided Conversations**: Use AI-generated prompts to facilitate meaningful discussions
- **Progress Tracking**: Monitor client assessment completion and results
- **Resource Library**: Access coaching materials organized by personality type

### For Managers
- **Team Insights**: Understand your team's collective strengths and interests
- **Development Questions**: Get conversation starters for one-on-ones
- **Skills Gap Analysis**: Identify areas for team development
- **Succession Planning**: Match internal talent with role requirements

### For Administrators
- **Content Management**: Customize assessment questions and career databases
- **CSV Data Upload**: Bulk import job roles, skills, and competencies with validation
- **Template Downloads**: Access pre-formatted CSV templates for easy data preparation
- **Analytics Dashboard**: View usage statistics and assessment trends
- **API Configuration**: Set up AI providers and authentication
- **Data Export**: Download assessment results for further analysis
- **Activity Logging**: Track all administrative actions and data uploads

### Progressive Web App Features (NEW!)
- **Installable**: Add to home screen on mobile devices or install on desktop
- **Offline Support**: Core features work without internet connection
- **App-like Experience**: Full-screen mode, no browser UI
- **Push Notifications**: (Coming soon) Get reminders and updates
- **Background Sync**: (Coming soon) Sync data when connection is restored
- **Responsive Design**: Optimized for all screen sizes

## How It Works

### The User Journey (In Simple Terms)

1. **Install the App**: Click install button in browser or add to home screen on mobile
2. **Login**: Users enter their credentials to access the system
3. **Welcome Hub**: Get personalized greeting and choose your path
4. **Choose Your Path**: Select whether you're an individual, coach, or manager
5. **Take Assessments** (for individuals):
   - Answer questions about your interests (RIASEC)
   - Rate your confidence in various skills
   - Rank what's important to you at work
6. **Get Results**: 
   - See your personality profile visualized
   - Review matched careers with explanations
   - Receive personalized learning paths
   - NEW! Compare your RIASEC profile with skills confidence
7. **Track Progress**:
   - Monitor learning progress
   - Update skills as you grow
   - Adjust career goals
8. **Take Action**: Export results, start learning, or schedule coaching

### The Science Behind It

**RIASEC Model**: Categorizes people into six personality types:
- **R**ealistic: Hands-on, practical, physical
- **I**nvestigative: Analytical, intellectual, scientific
- **A**rtistic: Creative, expressive, original
- **S**ocial: Helpful, teaching, interpersonal
- **E**nterprising: Persuasive, leading, influential
- **C**onventional: Organized, detailed, structured

The app matches your RIASEC profile with careers that have similar profiles, ensuring better job satisfaction and success.

## Technical Architecture

### Technology Stack
- **Frontend**: Streamlit (Python web framework)
- **Authentication**: Simple hardcoded authentication system
- **Data Visualization**: Plotly for interactive charts and spider diagrams
- **Data Processing**: Pandas for data manipulation
- **AI Integration**: OpenAI (primary), Anthropic, Google AI (fallbacks)
- **Storage**: Local file system with JSON data files
- **Session Management**: Streamlit session state with custom manager
- **Data Validation**: Custom CSV validator with comprehensive rule checking
- **PWA Support**: Service Worker for offline functionality, Web App Manifest
- **PDF Generation**: ReportLab for creating downloadable reports
- **Image Processing**: Pillow for PWA icon generation

### Key Components
1. **Multi-Page Application**: Modular page structure for different user flows
2. **Manager Classes**: Specialized managers for different functionalities
   - AuthManager: Authentication and user management
   - DataManager: Data persistence and retrieval
   - AIManager: Multi-provider AI integration with fallback
   - AssessmentManager: RIASEC assessment engine
   - CareerManager: Career matching and exploration
   - LearningManager: Learning resources and progress tracking
   - SessionStateManager: Centralized state management
3. **AI Integration Layer**: Abstracted interface for multiple AI providers
4. **Data Management**: Structured JSON storage with versioning
5. **Analytics Engine**: Processes and visualizes assessment results
6. **CSV Processing**: Validation, conversion, and storage of bulk data uploads
7. **PWA Components**: Service worker, manifest, offline caching strategy
8. **Comparison Engine**: Skills-to-RIASEC mapping and gap analysis

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (for cloning the repository)

### Step-by-Step Installation

1. **Clone the Repository**
```bash
git clone https://github.com/yourusername/career-atlas.git
cd career-atlas
```

2. **Create Virtual Environment** (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Set Up Environment Variables**
```bash
# Create .env file
cp .env.example .env
# Edit .env and add your API keys
```

5. **Run the Application**
```bash
streamlit run app.py
```

6. **Access the Application**
   - Open your browser and go to `http://localhost:8501`
   - For PWA installation, click the install button in your browser's address bar

## Configuration

### Authentication Setup

The system uses hardcoded authentication with two default users:
- **Demo User**: username: `demo`, password: `demo123`
- **Admin User**: username: `admin`, password: `admin123`

To modify users, edit the `USERS` dictionary in `utils/auth_manager.py`.

### API Configuration

Create a `.env` file with your API keys:
```env
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
GOOGLE_API_KEY=your_google_key_here
```

**Note**: The system will automatically fall back to other providers if the primary (OpenAI) is unavailable. If no API keys are configured, it will use offline fallback responses.

### PWA Configuration

The PWA functionality is automatically configured with:
- **Service Worker**: Handles offline caching and background sync
- **Web App Manifest**: Defines app metadata and appearance
- **Icons**: Auto-generated in multiple sizes for different devices

To customize PWA settings, edit:
- `static/manifest.json`: App name, colors, display mode
- `static/service-worker.js`: Caching strategies and offline behavior

### Data Files Structure

All data is stored in the `/data` directory:
```
data/
├── assessments/
│   └── riasec_questions.json    # RIASEC assessment questions
├── careers/
│   ├── careers_database.json    # Career information database
│   ├── job_roles.json          # Job role descriptions (CSV uploadable)
│   ├── job_tasks.json          # Job tasks and functions (CSV uploadable)
│   └── job_skills.json         # Job-skill mappings (CSV uploadable)
├── jobskills/                   # Job skills data directory (NEW!)
│   ├── job_skills_mapping.json # Skills to RIASEC mapping
│   ├── skills_mapping.json     # Alternative mapping format
│   └── *.csv                   # CSV uploads supported
├── skills/
│   ├── skills_database.json     # Skills taxonomy
│   ├── skills_master.json      # Skills master list (CSV uploadable)
│   └── skills_ka.json          # Knowledge & abilities (CSV uploadable)
├── resources/
│   ├── learning_resources.json  # Learning materials
│   └── courses_database.json    # Course catalog
├── coaching/
│   └── coaching_questions.json  # Coaching conversation starters
├── logs/
│   └── admin_activity.json     # Administrative action logs
└── users/                       # User data (auto-created)
    ├── profiles/               # User profiles
    ├── assessments/           # Assessment results
    └── progress/              # Learning progress
```

## User Guide

### For First-Time Users

1. **Access the App**: Open your browser and go to `http://localhost:8501`
2. **Install as PWA** (Optional): Click the install button in your browser or add to home screen
3. **Login**: Use demo/demo123 for testing or admin/admin123 for admin access
4. **Welcome Page**: Get oriented with the platform and choose your path
5. **Select Your Role**: Choose Individual, Coach, or Manager
6. **Complete Assessments**: Answer honestly - there are no right or wrong answers
7. **Explore Results**: 
   - View your RIASEC profile
   - Check career matches
   - NEW! Compare your interests vs skills in the Comparison View
8. **Start Learning**: Follow personalized learning paths
9. **Track Progress**: Monitor your development journey

### Using the Comparison View (NEW!)

The Comparison View provides powerful insights by comparing your RIASEC personality scores with your skills confidence:

1. **Access**: Navigate to "Compare RIASEC vs Skills" from the results page or welcome hub
2. **Spider Diagram**: Visual comparison showing:
   - Blue line: Your RIASEC interest scores
   - Green line: Your skills confidence mapped to RIASEC types
3. **Gap Analysis**: Identifies three key areas:
   - ✅ **Aligned**: Where interests and skills match well
   - 📈 **Development Opportunities**: High interest but lower skills
   - 💼 **Underutilized Strengths**: Strong skills but lower interest
4. **Career Recommendations**: Careers that match both your interests AND skills
5. **Export Report**: Download your comparison analysis as JSON

### For Administrators

1. **Access Admin Panel**: Login with admin credentials
2. **Dashboard View**: Monitor system metrics and recent activity
3. **CSV Upload**: 
   - Select file type from dropdown
   - Review expected column format
   - Download template for reference
   - Upload CSV file
   - Preview data and validation results
   - Confirm upload to replace existing data
4. **User Management**: View current users and their status
5. **System Settings**: Check system health and data file status

### CSV Upload Guide

The admin panel supports uploading 5 types of CSV files:

#### 1. Job Role Description
- **Columns**: Sector, Track, Job Role, Job Role Description
- **Purpose**: Define job roles and their descriptions
- **Validation**: Checks for duplicates within sector/track

#### 2. Job Role-Critical Work Function-Key Tasks
- **Columns**: Sector, Track, Job Role, Critical Work Function, Key Tasks
- **Purpose**: Map job roles to their key functions and tasks
- **Validation**: Ensures job roles exist in the system

#### 3. Job Role-Skills
- **Columns**: Sector, Track, Job Role, TSC_CCS Title, TSC_CCS Type, Proficiency Level
- **Purpose**: Define skills required for each job role
- **Validation**: Checks job role and skill existence, validates proficiency levels

#### 4. TSC_CCS_Key (Skills Master)
- **Columns**: TSC Code, Sector, TSC_CCS Category, TSC_CCS Title, TSC_CCS Description, TSC_CCS Type
- **Purpose**: Master list of all skills in the system
- **Validation**: Ensures unique TSC codes and validates skill types

#### 5. TSC_CCS_K&A (Knowledge & Abilities)
- **Columns**: Sector, TSC_CCS Category, TSC_CCS Title, TSC_CCS Description, Proficiency Level, Proficiency Description, Knowledge-Ability Classification, Knowledge-Ability Items
- **Purpose**: Detailed breakdown of knowledge and abilities for skills
- **Validation**: Checks skill existence and classification values

**Proficiency Levels**: The system accepts both numeric (1-5) and text formats:
- Numeric: 1, 2, 3, 4, 5
- Text: Basic, Intermediate, Advanced, Expert, Master, Beginner, Competent, Proficient

### Progressive Web App Usage

#### Installing the App
1. **Desktop (Chrome/Edge)**:
   - Look for install icon in address bar
   - Click "Install Career Atlas"
   - App opens in its own window

2. **Mobile (iOS)**:
   - Tap share button in Safari
   - Select "Add to Home Screen"
   - Name the app and tap "Add"

3. **Mobile (Android)**:
   - Tap menu (3 dots) in Chrome
   - Select "Add to Home Screen"
   - Confirm installation

#### Offline Features
When offline, you can:
- View previously loaded assessments
- Access cached results
- Review saved career recommendations
- Continue incomplete assessments (auto-saved)

## Code Structure

```
career-atlas/
├── app.py                    # Main application entry point (✅ Implemented)
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── .env.example           # Environment variables template
│
├── pages/                  # Streamlit pages
│   ├── __init__.py           # Pages module init (✅ Implemented)
│   ├── persona_selection.py    # Role selection
│   ├── welcome.py             # Welcome screen (✅ Implemented)
│   ├── riasec_assessment.py   # RIASEC test
│   ├── skills_assessment.py   # Skills evaluation
│   ├── values_assessment.py   # Values ranking
│   ├── results.py            # Results display
│   ├── comparison_view.py     # RIASEC vs Skills comparison (✅ NEW!)
│   ├── coaching_dashboard.py  # Coach interface
│   ├── manager_dashboard.py   # Manager interface
│   └── admin_panel.py        # Admin controls (✅ Implemented)
│
├── utils/                  # Utility modules
│   ├── auth_manager.py       # Authentication (✅ Implemented)
│   ├── data_manager.py       # Data operations (✅ Implemented)
│   ├── ai_manager.py         # AI integration (✅ Implemented)
│   ├── assessment_manager.py # Assessment engine (✅ Implemented)
│   ├── career_manager.py     # Career matching (✅ Implemented)
│   ├── learning_manager.py   # Learning system (✅ Implemented)
│   ├── session_state.py      # State management (✅ Implemented)
│   ├── csv_validator.py      # CSV validation (✅ Implemented)
│   ├── csv_templates.py      # Template generation (✅ Implemented)
│   ├── pwa_injector.py       # PWA functionality (✅ NEW!)
│   └── llm_manager.py        # Legacy AI manager
│
├── static/                 # PWA assets (✅ NEW!)
│   ├── manifest.json         # PWA manifest
│   ├── service-worker.js     # Service worker
│   ├── icon-192.png         # PWA icon
│   └── icon-512.png         # PWA icon (large)
│
└── data/                   # Data files (✅ All created)
    ├── assessments/
    ├── careers/
    ├── jobskills/           # Job skills mapping (✅ NEW!)
    ├── skills/
    ├── resources/
    ├── coaching/
    ├── logs/
    └── users/
```

## Implementation Status

### ✅ Completed Features

1. **Authentication System** (Fix #1)
   - Simple hardcoded authentication
   - User session management
   - Role-based access (admin/user)

2. **Data Files** (Fix #2)
   - Complete RIASEC questions database
   - Comprehensive careers database
   - Skills taxonomy
   - Learning resources catalog
   - Coaching questions library

3. **Navigation System** (Fix #3)
   - Button-based navigation
   - Session state management
   - Multi-page routing

4. **Data Management** (Fix #4)
   - User profile management
   - Assessment storage and retrieval
   - Learning progress tracking
   - Career interest tracking
   - Timestamp-based versioning

5. **AI Integration** (Fix #5)
   - Multi-provider support (OpenAI, Anthropic, Google)
   - Automatic fallback mechanism
   - Career recommendations
   - Development planning
   - Interview preparation
   - Skills gap analysis
   - RIASEC-tailored coaching questions

6. **Assessment Engine** (Fix #6)
   - RIASEC scoring algorithm (0-100 scale)
   - Holland Code generation
   - Score interpretation
   - Career theme identification
   - Progress tracking
   - Response validation

7. **Career Matching** (Fix #7)
   - Multi-factor matching algorithm
   - Skills gap analysis
   - Development path generation
   - Career insights and trends
   - Related career suggestions
   - Entry option analysis

8. **Learning Management** (Fix #8)
   - Personalized resource recommendations
   - Learning path creation
   - Progress tracking
   - Learning style matching
   - Skill acquisition tracking
   - Learning analytics dashboard

9. **Session State Management** (Fix #9)
   - Centralized state management
   - Navigation with history tracking
   - Authentication state helpers
   - Assessment response management
   - Recommendation caching
   - Filter persistence
   - State import/export
   - Debug utilities

10. **Main Application Entry Point** (Fix #10)
    - Complete app.py implementation
    - Professional login page with feature showcase
    - Custom CSS styling for polished UI
    - Dynamic page routing with error handling
    - User greeting and logout functionality
    - Automatic directory creation
    - Graceful handling of missing pages

11. **Welcome Page** (Fix #11)
    - Personalized greeting system (new vs returning users)
    - Progress dashboard showing assessment and learning metrics
    - Clear value proposition and feature explanations
    - Multiple navigation paths based on user status
    - Quick tips sidebar for best practices
    - Feature highlights section
    - Path selection for different user types (Individual/Coach/Manager)
    - Admin panel access for administrators
    - FAQ and RIASEC education sections
    - Automatic user profile creation

12. **Admin Panel** (Fix #12)
    - Complete admin interface with 4 tabs
    - Dashboard with system metrics
    - CSV upload functionality with validation
    - User management view
    - System settings and status

13. **CSV Upload System**
    - Support for 5 different CSV file types
    - Real-time validation with detailed error reporting
    - Data preview before upload
    - Template generation with sample data
    - Automatic JSON conversion and storage
    - Activity logging for audit trail
    - Support for both numeric and text proficiency levels
    - Referential integrity checking
    - Duplicate detection
    - UTF-8 encoding support

14. **Data Validation Framework**
    - Comprehensive CSV validation rules
    - Column presence checking
    - Data type validation
    - Referential integrity between files
    - Custom format validation (TSC codes)
    - Proficiency level validation (numeric and text)
    - Duplicate detection within contexts
    - Row-level error reporting

15. **Progressive Web App (PWA)** (NEW!)
    - Service Worker implementation with offline caching
    - Web App Manifest for installability
    - Auto-generated PWA icons in multiple sizes
    - Runtime caching strategy for API calls
    - Offline fallback pages
    - App-like experience on mobile and desktop
    - Background sync preparation
    - Cache versioning and update strategy

16. **RIASEC vs Skills Comparison View** (NEW!)
    - Interactive spider diagram using Plotly
    - Visual comparison of RIASEC scores vs skills confidence
    - Skills-to-RIASEC mapping based on uploaded job skills data
    - Support for multiple data formats (JSON/CSV)
    - Gap analysis identifying:
      - Aligned areas (interests match skills)
      - Development opportunities (high interest, low skills)
      - Underutilized strengths (high skills, low interest)
    - Career recommendations based on alignment
    - Detailed comparison metrics and insights
    - Export functionality for comparison reports
    - Integration with job skills data from CSV uploads

### 🚧 In Progress

- Auto-save functionality
- PDF export with ReportLab
- RAG-based Q&A system

### 📋 Pending Features

- Email notifications
- Advanced data visualizations
- Social features (mentorship matching)
- Push notifications for PWA
- Background sync for offline changes
- Advanced PWA features (share target, file handling)

## API Documentation

### Manager Classes

#### AuthManager
```python
# Authentication operations
AuthManager.login(username, password)
AuthManager.logout()
AuthManager.is_authenticated()
AuthManager.is_admin()
AuthManager.get_current_user()
```

#### DataManager
```python
# User operations
data_manager.save_user_profile(user_id, profile_data)
data_manager.load_user_profile(user_id)

# Assessment operations
data_manager.save_assessment(user_id, assessment_data)
data_manager.load_user_assessments(user_id)

# Learning operations
data_manager.save_learning_progress(user_id, progress_data)
data_manager.load_learning_history(user_id)
```

#### AIManager
```python
# AI-powered features
ai_manager.generate_career_recommendations(riasec_scores, additional_info)
ai_manager.generate_development_plan(riasec_scores, selected_careers, additional_info)
ai_manager.generate_interview_questions(career_title, level)
ai_manager.analyze_skills_gap(current_skills, target_career, riasec_scores)

# RIASEC-tailored coaching
ai_manager.generate_coaching_questions_for_coachee(coachee_riasec_scores, additional_context)
ai_manager.generate_manager_questions_for_team_member(team_member_riasec_scores, additional_context)
```

#### AssessmentManager
```python
# Assessment operations
assessment_manager.get_assessment_questions(category)
assessment_manager.calculate_scores(responses)
assessment_manager.interpret_scores(scores)
assessment_manager.save_assessment_result(user_id, scores, responses)
```

#### CareerManager
```python
# Career exploration
career_manager.search_careers(query, filters)
career_manager.match_careers_to_assessment(assessment_data, top_n)
career_manager.get_career_recommendations(user_id, include_ai)
career_manager.get_career_insights(career_id)
```

#### LearningManager
```python
# Learning features
learning_manager.search_resources(query, filters)
learning_manager.get_learning_recommendations(user_id, career_goals)
learning_manager.track_learning_progress(user_id, resource_id, progress)
learning_manager.get_learning_dashboard(user_id)
```

#### SessionStateManager
```python
# State management
SessionStateManager.initialize()
SessionStateManager.get(key, default)
SessionStateManager.set(key, value)
SessionStateManager.navigate_to(page)
SessionStateManager.is_authenticated()
SessionStateManager.save_assessment_response(type, question_id, response)
SessionStateManager.cache_recommendations(careers, resources)
```

#### CSVValidator
```python
# CSV validation
validator = CSVValidator()
validation_result = validator.validate(file_type, dataframe)
# Returns: {'valid': bool, 'errors': list, 'details': list, 'summary': dict}
```

#### CSVTemplateGenerator
```python
# Template generation
generator = CSVTemplateGenerator()
template_df = generator.generate_template(file_type)
# Returns: pandas DataFrame with sample data
```

## Customization Guide

### Adding New Assessment Questions

Edit `data/assessments/riasec_questions.json`:
```json
{
  "questions": [
    {
      "id": 101,
      "text": "Your new question here",
      "type": "Realistic",
      "category": "interests"
    }
  ]
}
```

### Adding New Careers

Edit `data/careers/careers_database.json`:
```json
{
  "careers": [
    {
      "id": "new-career-id",
      "title": "New Career Title",
      "holland_codes": ["RIA"],
      "required_skills": ["skill1", "skill2"],
      "salary_range_min": 50000,
      "salary_range_max": 80000
    }
  ]
}
```

### Customizing the Matching Algorithm

The career matching algorithm in `utils/career_manager.py` uses these weights:
- Primary RIASEC match: 40%
- Secondary RIASEC match: 30%
- Overall profile similarity: 30%

Adjust the weights in the `_calculate_career_match_score` method.

### Adding Learning Resources

Edit `data/resources/learning_resources.json`:
```json
{
  "resources": [
    {
      "id": "resource-001",
      "title": "New Learning Resource",
      "type": "course",
      "skills": ["Python", "Data Analysis"],
      "format": "video",
      "duration_hours": 20
    }
  ]
}
```

### Customizing Skills-to-RIASEC Mapping

Edit or upload a file to `data/jobskills/`:
```json
{
  "skill_riasec_mapping": {
    "Data Analysis": "Investigative",
    "Creative Design": "Artistic",
    "Leadership": "Enterprising"
  }
}
```

### Bulk Data Upload via CSV

1. **Prepare your CSV file** following the expected column format
2. **Download a template** from the admin panel for reference
3. **Ensure data consistency**:
   - Job roles must exist before mapping skills
   - Skills must exist in master before using in mappings
   - Use consistent naming across files
4. **Upload through admin panel**:
   - Preview data before confirming
   - Review validation results
   - Fix any errors and re-upload

### PWA Customization

1. **App Appearance** - Edit `static/manifest.json`:
```json
{
  "name": "Career Atlas",
  "short_name": "Career Atlas",
  "theme_color": "#1e3a8a",
  "background_color": "#ffffff"
}
```

2. **Caching Strategy** - Edit `static/service-worker.js`:
   - Modify cache names and versions
   - Adjust caching strategies
   - Add/remove cached resources

3. **Icons** - Replace files in `static/`:
   - `icon-192.png`: 192x192px icon
   - `icon-512.png`: 512x512px icon

## Troubleshooting

### Common Issues and Solutions

**Issue**: "Module not found" errors
- **Solution**: Ensure all dependencies are installed: `pip install -r requirements.txt`

**Issue**: AI features not working
- **Solution**: Check API keys in .env file and ensure they're valid (not placeholder values)

**Issue**: Data not saving
- **Solution**: Check that the `/data/users/` directory exists and has write permissions

**Issue**: Assessment not calculating scores
- **Solution**: Ensure all questions are answered (check for response validation errors)

**Issue**: Learning recommendations empty
- **Solution**: Complete an assessment first and ensure learning resources data file exists

**Issue**: Navigation not working
- **Solution**: Check session state initialization and ensure `SessionStateManager.initialize()` is called

**Issue**: CSV upload fails validation
- **Solution**: 
  - Check column names match exactly (case-sensitive)
  - Ensure no empty required fields
  - Verify referential integrity (job roles exist, skills exist)
  - Use UTF-8 encoding for the CSV file
  - Download and review the template for correct format

**Issue**: CSV upload succeeds but data doesn't appear
- **Solution**: 
  - Check the appropriate JSON file was created in `/data/` directory
  - Ensure the app has write permissions
  - Check admin activity logs for errors

**Issue**: PWA not installing
- **Solution**:
  - Ensure HTTPS is enabled (required for PWA)
  - Check browser compatibility
  - Clear browser cache and try again
  - Verify manifest.json is loading correctly

**Issue**: Comparison view shows no data
- **Solution**:
  - Complete both RIASEC and skills assessments first
  - Check job skills data exists in `/data/jobskills/`
  - Upload job skills mapping via admin panel if missing

**Issue**: Spider diagram not displaying
- **Solution**:
  - Ensure plotly is installed: `pip install plotly`
  - Check browser console for JavaScript errors
  - Verify assessment data is properly loaded

### Debug Mode

To enable debug logging, set in your code:
```python
import streamlit as st
st.set_option('client.showErrorDetails', True)

# For session state debugging
SessionStateManager.debug_state()

# Check CSV validation details
validation_result = validator.validate(file_type, df)
st.json(validation_result)  # Shows full validation output

# Check PWA support
from utils.pwa_injector import check_pwa_support
check_pwa_support()  # Shows PWA compatibility info
```

### Getting Help

1. Check the error messages in the terminal
2. Review the specific manager class documentation
3. Ensure all data files are properly formatted JSON
4. Verify API keys are correctly set
5. Use the session state debug view to inspect current state
6. Check admin activity logs in `/data/logs/admin_activity.json`
7. Review CSV validation error details in the upload interface
8. Check browser console for PWA-related errors
9. Verify job skills data format in `/data/jobskills/`

## Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Development Guidelines

- Follow PEP 8 style guide
- Add docstrings to all functions
- Update README for new features
- Ensure backward compatibility
- Test with both user roles
- Validate CSV processing with edge cases
- Add appropriate error handling
- Log administrative actions
- Test PWA functionality across browsers
- Ensure offline functionality works correctly

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- RIASEC model by John L. Holland
- Streamlit community for framework support
- OpenAI, Anthropic, and Google for AI capabilities
- Plotly for interactive data visualizations
- Pandas for robust data processing
- ReportLab for PDF generation capabilities
- PWA community for offline-first patterns
- All contributors and testers

---

**Note**: This is a development version. For production use, ensure proper security measures, API rate limiting, HTTPS for PWA, and data protection compliance.

## Recent Updates

### Version 2.0 (Latest)
- ✅ **Progressive Web App**: Full PWA implementation with offline support
- ✅ **Comparison View**: Spider diagram comparing RIASEC vs Skills confidence
- ✅ **Enhanced Data Management**: Support for job skills data in multiple formats
- ✅ **Improved Navigation**: Better user flow and page transitions
- 🚧 **Coming Soon**: Auto-save, PDF export, RAG-based Q&A

### Version 1.0
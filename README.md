# Career Atlas - AI-Powered Career Guidance Platform

A comprehensive career assessment and guidance application built with Streamlit, featuring RIASEC personality assessment, skills evaluation, work values analysis, and AI-powered personalized coaching.

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

Career Atlas is an intelligent career guidance system that helps users discover their ideal career paths through scientifically-backed assessments and AI-powered recommendations. Think of it as having a personal career counselor available 24/7.

### What Makes Career Atlas Special?

- **Science-Based**: Uses the proven RIASEC (Holland Code) model for personality assessment
- **AI-Enhanced**: Leverages multiple AI providers (OpenAI, Anthropic, Google) with automatic fallback
- **Multi-User Support**: Different interfaces for individuals, coaches, and managers
- **Comprehensive**: Covers personality, skills, values, career matching, and learning paths
- **Smart Learning**: Personalized learning recommendations with progress tracking
- **Data-Driven**: Advanced analytics and insights for career development

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
- **Analytics Dashboard**: View usage statistics and assessment trends
- **API Configuration**: Set up AI providers and authentication
- **Data Export**: Download assessment results for further analysis

## How It Works

### The User Journey (In Simple Terms)

1. **Login**: Users enter their credentials to access the system
2. **Choose Your Path**: Select whether you're an individual, coach, or manager
3. **Take Assessments** (for individuals):
   - Answer questions about your interests (RIASEC)
   - Rate your confidence in various skills
   - Rank what's important to you at work
4. **Get Results**: 
   - See your personality profile visualized
   - Review matched careers with explanations
   - Receive personalized learning paths
5. **Track Progress**:
   - Monitor learning progress
   - Update skills as you grow
   - Adjust career goals
6. **Take Action**: Export results, start learning, or schedule coaching

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
- **Data Visualization**: Plotly for interactive charts
- **Data Processing**: Pandas for data manipulation
- **AI Integration**: OpenAI (primary), Anthropic, Google AI (fallbacks)
- **Storage**: Local file system with JSON data files
- **Session Management**: Streamlit session state with custom manager

### Key Components
1. **Multi-Page Application**: Modular page structure for different user flows
2. **Manager Classes**: Specialized managers for different functionalities
   - AuthManager: Authentication and user management
   - DataManager: Data persistence and retrieval
   - AIManager: Multi-provider AI integration
   - AssessmentManager: RIASEC assessment engine
   - CareerManager: Career matching and exploration
   - LearningManager: Learning resources and progress tracking
   - SessionStateManager: Centralized state management
3. **AI Integration Layer**: Abstracted interface for multiple AI providers
4. **Data Management**: Structured JSON storage with versioning
5. **Analytics Engine**: Processes and visualizes assessment results

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

### Data Files Structure

All data is stored in the `/data` directory:
```
data/
├── assessments/
│   └── riasec_questions.json    # RIASEC assessment questions
├── careers/
│   └── careers_database.json    # Career information database
├── skills/
│   └── skills_database.json     # Skills taxonomy
├── resources/
│   ├── learning_resources.json  # Learning materials
│   └── courses_database.json    # Course catalog
├── coaching/
│   └── coaching_questions.json  # Coaching conversation starters
└── users/                       # User data (auto-created)
    ├── profiles/               # User profiles
    ├── assessments/           # Assessment results
    └── progress/              # Learning progress
```

## User Guide

### For First-Time Users

1. **Access the App**: Open your browser and go to `http://localhost:8501`
2. **Login**: Use demo/demo123 for testing or admin/admin123 for admin access
3. **Select Your Role**: Choose Individual, Coach, or Manager
4. **Complete Assessments**: Answer honestly - there are no right or wrong answers
5. **Explore Careers**: Review your matched careers with detailed insights
6. **Start Learning**: Follow personalized learning paths
7. **Track Progress**: Monitor your development journey

### For Administrators

1. **Access Admin Panel**: Login with admin credentials
2. **Manage Data**: Update questions, careers, and resources
3. **Configure APIs**: Set up AI providers in .env file
4. **Monitor Usage**: Check analytics and user progress

## Code Structure

```
career-atlas/
├── app.py                    # Main application entry point (✅ Implemented)
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── .env.example           # Environment variables template
│
├── pages/                  # Streamlit pages
│   ├── persona_selection.py    # Role selection
│   ├── welcome.py             # Welcome screen
│   ├── riasec_assessment.py   # RIASEC test
│   ├── skills_assessment.py   # Skills evaluation
│   ├── values_assessment.py   # Values ranking
│   ├── results.py            # Results display
│   ├── coaching_dashboard.py  # Coach interface
│   ├── manager_dashboard.py   # Manager interface
│   └── admin_panel.py        # Admin controls
│
├── utils/                  # Utility modules
│   ├── auth_manager.py       # Authentication (✅ Implemented)
│   ├── data_manager.py       # Data operations (✅ Implemented)
│   ├── ai_manager.py         # AI integration (✅ Implemented)
│   ├── assessment_manager.py # Assessment engine (✅ Implemented)
│   ├── career_manager.py     # Career matching (✅ Implemented)
│   ├── learning_manager.py   # Learning system (✅ Implemented)
│   ├── session_state.py      # State management (✅ Implemented)
│   └── llm_manager.py        # Legacy AI manager
│
└── data/                   # Data files (✅ All created)
    ├── assessments/
    ├── careers/
    ├── skills/
    ├── resources/
    ├── coaching/
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

### 🚧 In Progress

- Page implementations (welcome, assessments, results, dashboards)
- UI/UX enhancements
- Advanced analytics features

### 📋 Pending Features

- Email notifications
- PDF report generation
- Advanced data visualizations
- Social features (mentorship matching)
- Mobile responsiveness

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

### Debug Mode

To enable debug logging, set in your code:
```python
import streamlit as st
st.set_option('client.showErrorDetails', True)

# For session state debugging
SessionStateManager.debug_state()
```

### Getting Help

1. Check the error messages in the terminal
2. Review the specific manager class documentation
3. Ensure all data files are properly formatted JSON
4. Verify API keys are correctly set
5. Use the session state debug view to inspect current state

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

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- RIASEC model by John L. Holland
- Streamlit community for framework support
- OpenAI, Anthropic, and Google for AI capabilities
- All contributors and testers

---

**Note**: This is a development version. For production use, ensure proper security measures, API rate limiting, and data protection compliance.

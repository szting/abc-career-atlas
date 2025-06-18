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
- [Known Issues](#known-issues)
- [Customization Guide](#customization-guide)
- [API Integration](#api-integration)
- [Troubleshooting](#troubleshooting)

## Overview

Career Atlas is an intelligent career guidance system that helps users discover their ideal career paths through scientifically-backed assessments and AI-powered recommendations. Think of it as having a personal career counselor available 24/7.

### What Makes Career Atlas Special?

- **Science-Based**: Uses the proven RIASEC (Holland Code) model for personality assessment
- **AI-Enhanced**: Leverages artificial intelligence for personalized recommendations
- **Multi-User Support**: Different interfaces for individuals, coaches, and managers
- **Comprehensive**: Covers personality, skills, and values for holistic career matching
- **Customizable**: Administrators can tailor assessments to specific industries or organizations

## Features

### For Individuals
- **RIASEC Personality Assessment**: Discover your Holland Code through interactive questions
- **Skills Confidence Evaluation**: Rate your confidence across various skill categories
- **Work Values Prioritization**: Identify what matters most in your ideal workplace
- **AI-Powered Career Matching**: Get personalized career recommendations based on your profile
- **Development Planning**: Receive actionable steps to reach your career goals
- **Visual Analytics**: See your results through interactive charts and graphs

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
   - Receive a personalized development plan
5. **Take Action**: Export results, schedule coaching, or start learning

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
- **Authentication**: Streamlit-authenticator / Simple password system
- **Data Visualization**: Plotly for interactive charts
- **Data Processing**: Pandas for data manipulation
- **AI Integration**: OpenAI, Anthropic, or Google AI APIs
- **Storage**: Local file system / Google Drive integration

### Key Components
1. **Multi-Page Application**: Modular page structure for different user flows
2. **Session Management**: Maintains user state throughout the assessment
3. **AI Integration Layer**: Abstracted interface for multiple AI providers
4. **Data Management**: Handles assessment storage and retrieval
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

4. **Set Up Configuration**
```bash
# Create config.yaml file (see Configuration section)
cp config.example.yaml config.yaml
```

5. **Run the Application**
```bash
streamlit run app.py
```

## Configuration

### Authentication Setup

Create a `config.yaml` file:
```yaml
credentials:
  usernames:
    demo:
      email: demo@example.com
      name: Demo User
      password: $2b$12$hashed_password_here  # Use demo123
    admin:
      email: admin@example.com
      name: Admin User
      password: $2b$12$hashed_password_here  # Use admin123

cookie:
  expiry_days: 30
  key: some_signature_key
  name: some_cookie_name

preauthorized:
  emails: []
```

### API Configuration

Set up AI provider credentials in `.env`:
```env
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
GOOGLE_API_KEY=your_google_key_here
```

### Google Drive Integration (Optional)

Place your `service_account_key.json` in the project root for Google Drive storage.

## User Guide

### For First-Time Users

1. **Access the App**: Open your browser and go to `http://localhost:8501`
2. **Login**: Use demo/demo123 for testing or your assigned credentials
3. **Select Your Role**: Choose Individual, Coach, or Manager
4. **Complete Assessments**: Answer honestly - there are no right or wrong answers
5. **Review Results**: Take time to explore your matches and recommendations
6. **Export Your Report**: Download a PDF for future reference

### For Administrators

1. **Access Admin Panel**: Login with admin credentials
2. **Customize Content**: Upload new questions or career databases
3. **Configure APIs**: Set up AI providers for enhanced features
4. **Monitor Usage**: Check analytics for insights

## Code Structure

```
career-atlas/
├── app.py                    # Main application entry point
├── config.yaml              # Authentication configuration
├── requirements.txt         # Python dependencies
├── README.md               # This file
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
│   ├── simple_auth.py        # Authentication
│   ├── session_state.py      # State management
│   ├── career_matcher.py     # Matching algorithm
│   ├── auth_manager.py       # Auth utilities
│   ├── data_manager.py       # Data handling
│   └── llm_manager.py        # AI integration
│
└── data/                   # Data files
    ├── careers.py            # Career database
    ├── riasec_questions.py   # Assessment questions
    ├── skills_list.py        # Skills inventory
    ├── work_values.py        # Values definitions
    └── coaching_questions.py # Coaching prompts
```

## Known Issues

### Current Limitations

1. **Authentication Conflict**: Two authentication systems present (needs consolidation)
2. **Missing Data Files**: Core data files need to be created or imported
3. **Manager Classes**: Implementation pending for data and AI managers
4. **Navigation Flow**: Mismatch between app.py routing and actual pages
5. **API Integration**: Needs unified approach for multiple AI providers

### Planned Improvements

- [ ] Consolidate authentication system
- [ ] Implement missing manager classes
- [ ] Create comprehensive data files
- [ ] Add email notification system
- [ ] Implement PDF report generation
- [ ] Add multi-language support
- [ ] Create mobile-responsive design
- [ ] Add batch assessment capabilities

## Customization Guide

### Adding New Assessment Questions

1. **RIASEC Questions**: Edit `data/riasec_questions.py`
```python
riasec_questions = [
    {
        'id': 'q1',
        'text': 'I enjoy working with tools',
        'type': 'realistic'
    },
    # Add more questions...
]
```

2. **Skills Categories**: Modify `data/skills_list.py`
```python
skills_categories = [
    {
        'name': 'Technical Skills',
        'skills': ['Programming', 'Data Analysis', 'Design']
    },
    # Add more categories...
]
```

### Adding New Careers

Edit `data/careers.py`:
```python
careers = [
    {
        'id': 'software-engineer',
        'title': 'Software Engineer',
        'description': 'Develops software applications',
        'primary_type': 'investigative',
        'secondary_type': 'realistic',
        'required_skills': ['Programming', 'Problem Solving'],
        'salary_range': '$70,000 - $150,000',
        'growth_outlook': 'Much faster than average'
    },
    # Add more careers...
]
```

### Customizing the Matching Algorithm

The career matching algorithm in `utils/career_matcher.py` uses these weights:
- RIASEC alignment: 40%
- Skills match: 35%
- Values alignment: 25%

Adjust these weights based on your needs.

## API Integration

### Supported AI Providers

1. **OpenAI**: GPT-3.5/GPT-4 for career recommendations
2. **Anthropic**: Claude for coaching conversations
3. **Google**: Gemini for development planning

### Setting Up AI Features

1. Obtain API keys from your chosen provider
2. Add keys to `.env` file or through Admin Panel
3. Configure fallback options for reliability
4. Test integration before deployment

### API Usage Examples

```python
# Generate career recommendations
recommendations = llm_manager.generate_career_recommendations(
    riasec_scores={'realistic': 4.2, 'investigative': 3.8},
    skills=['Programming', 'Analysis'],
    values=['Work-Life Balance', 'Growth']
)

# Get coaching questions
questions = llm_manager.get_coaching_questions(
    riasec_type='social',
    context='career transition'
)
```

## Troubleshooting

### Common Issues and Solutions

**Issue**: "Module not found" errors
- **Solution**: Ensure all dependencies are installed: `pip install -r requirements.txt`

**Issue**: Authentication not working
- **Solution**: Check config.yaml format and password hashing

**Issue**: AI features not responding
- **Solution**: Verify API keys and check rate limits

**Issue**: Assessment results not saving
- **Solution**: Check file permissions in the project directory

**Issue**: Charts not displaying
- **Solution**: Update Plotly: `pip install --upgrade plotly`

### Getting Help

1. Check the [Issues](https://github.com/yourusername/career-atlas/issues) page
2. Review error logs in the terminal
3. Contact support with:
   - Error messages
   - Steps to reproduce
   - System information

## Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Development Guidelines

- Follow PEP 8 style guide
- Add docstrings to functions
- Update README for new features
- Test on multiple browsers
- Consider accessibility

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- RIASEC model by John L. Holland
- Streamlit community for framework support
- Contributors and testers

---

**Note**: This is a development version. For production use, ensure proper security measures, API rate limiting, and data protection compliance.

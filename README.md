# Career Atlas - Your Personal AI Career Guide 🧭

Think of Career Atlas as your personal career counselor that's available 24/7! It helps you discover careers that match your personality, skills, and values through fun assessments and smart AI recommendations. Plus, you can now install it like a mobile app on your phone!

## Table of Contents

- [What is Career Atlas?](#what-is-career-atlas)
- [Key Features](#key-features)
- [How It Works](#how-it-works)
- [Getting Started](#getting-started)
- [User Guide](#user-guide)
- [For Administrators](#for-administrators)
- [Technical Details](#technical-details)
- [What's New](#whats-new)
- [Troubleshooting](#troubleshooting)

## What is Career Atlas?

Career Atlas is like having a career counselor in your pocket! It uses a scientifically-proven personality test (called RIASEC) to understand what kind of work would make you happiest, then matches you with careers that fit your personality.

### Why Use Career Atlas?

- **It's Scientific**: Uses the same personality test (RIASEC/Holland Code) that real career counselors use
- **It's Smart**: AI technology gives you personalized advice, just like talking to an expert
- **It's Comprehensive**: Looks at your personality, skills, AND values - not just one thing
- **It's Convenient**: Works on your phone, tablet, or computer - even offline!
- **It's Free**: No subscription fees or hidden costs

## Key Features

### 🎯 For Job Seekers
- **Personality Test**: Answer simple questions to discover your work personality type
- **Skills Check**: Rate your confidence in different skills (from beginner to expert)
- **Values Assessment**: Identify what matters most to you in a job
- **Career Matches**: Get a list of careers that fit YOU perfectly
- **Learning Paths**: Find out exactly what skills to learn next
- **Progress Tracking**: See how far you've come on your career journey
- **Visual Comparisons**: NEW! See how your interests compare to your actual skills

### 👥 For Career Coaches
- **Smart Questions**: Get AI-generated questions tailored to each client's personality
- **Client Insights**: Understand your clients better through their assessment results
- **Conversation Starters**: Never run out of meaningful things to discuss

### 👔 For Managers
- **Team Understanding**: See your team's collective strengths and interests
- **Better 1-on-1s**: Get personalized questions for each team member
- **Development Planning**: Identify what training your team needs

### 🔧 For Administrators
- **Easy Data Management**: Upload job and skill information using simple spreadsheets
- **User Management**: See who's using the system and how
- **System Health**: Monitor that everything is working properly

### 📱 Works Like an App! (NEW!)
- **Install on Phone**: Add it to your home screen just like any other app
- **Works Offline**: Keep using it even without internet
- **Fast Loading**: Saves data on your device for quick access
- **Full Screen**: No browser bars - looks and feels like a real app

## How It Works

### The Journey (In Simple Steps)

1. **Sign In** 📝
   - Use the demo account to try it out (username: `demo`, password: `demo123`)
   - Or get your own account from your organization

2. **Choose Your Path** 🛤️
   - Individual: Take assessments and explore careers
   - Coach: Access coaching tools and client insights
   - Manager: Get team insights and development questions

3. **Take Assessments** (for individuals) 📊
   - **Personality Test**: Answer "Would you enjoy..." questions
   - **Skills Check**: Rate yourself from Beginner to Expert
   - **Values Ranking**: Pick what's most important to you at work

4. **Get Your Results** 🎉
   - See your personality type (like "Creative Problem-Solver")
   - View careers that match your profile
   - Get specific learning recommendations

5. **Compare & Analyze** (NEW!) 🔍
   - See a visual spider chart comparing your interests vs skills
   - Identify where you need to grow
   - Find careers that match BOTH your interests and current skills

6. **Take Action** 🚀
   - Start learning recommended skills
   - Track your progress
   - Update your profile as you grow

### Understanding RIASEC (Your Work Personality)

RIASEC is like a personality test, but specifically for work. It puts people into 6 types:

- **R - Realistic** 🔧: Like working with your hands, tools, or machines
- **I - Investigative** 🔬: Love solving puzzles and understanding how things work
- **A - Artistic** 🎨: Enjoy being creative and thinking outside the box
- **S - Social** 🤝: Like helping people and working in teams
- **E - Enterprising** 💼: Natural leaders who like to persuade and sell
- **C - Conventional** 📋: Prefer organized, structured work with clear rules

Most people are a mix of 2-3 types, and that's perfectly normal!

## Getting Started

### What You Need
- A computer with Python installed (version 3.8 or newer)
- Basic ability to use command line/terminal
- Internet connection (for initial setup)

### Installation Steps

1. **Download the Code**
   ```bash
   git clone https://github.com/yourusername/career-atlas.git
   cd career-atlas
   ```

2. **Set Up Python Environment** (Recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Required Packages**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up AI Keys** (Optional but recommended)
   - Copy `.env.example` to `.env`
   - Add your OpenAI/Anthropic/Google API keys
   - Don't have keys? The app still works with limited features!

5. **Start the Application**
   ```bash
   streamlit run app.py
   ```

6. **Open in Browser**
   - Go to `http://localhost:8501`
   - To install as app: Look for install button in your browser

## User Guide

### First Time Users

1. **Login Screen**
   - Use `demo`/`demo123` to try it out
   - Admins use `admin`/`admin123`

2. **Welcome Page**
   - See personalized greeting
   - Check your progress dashboard
   - Choose your path (Individual/Coach/Manager)

3. **Taking Assessments**
   - Be honest - there are no "right" answers!
   - Each assessment takes 5-10 minutes
   - You can pause and come back later

4. **Understanding Your Results**
   - **RIASEC Chart**: Shows your personality scores (higher = stronger interest)
   - **Career Matches**: Listed from best to good fit
   - **Skills Gap**: What you need to learn for each career

### Using the Comparison View (NEW!)

This exciting new feature shows you where your interests and skills align:

1. **Access It**: Click "Compare RIASEC vs Skills" from the results page
2. **The Spider Chart**: 
   - Blue line = What you're interested in
   - Green line = What you're actually good at
3. **What It Tells You**:
   - ✅ **Green Zone**: Where interests and skills match (you're on the right track!)
   - 📈 **Growth Zone**: High interest but need more skills (focus learning here!)
   - 💼 **Hidden Talents**: Strong skills you might not be using enough

### Installing as a Mobile App

**On iPhone/iPad:**
1. Open in Safari (must be Safari!)
2. Tap the share button (square with arrow)
3. Scroll down and tap "Add to Home Screen"
4. Name it and tap "Add"

**On Android:**
1. Open in Chrome
2. Tap the menu (3 dots)
3. Tap "Add to Home Screen"
4. Confirm installation

**On Computer:**
1. Look for install icon in address bar (Chrome/Edge)
2. Click "Install Career Atlas"
3. It opens in its own window!

## For Administrators

### Managing Data with Spreadsheets

You can upload data using CSV files (spreadsheets). Here's how:

1. **Go to Admin Panel** (login as admin)
2. **Click "CSV Upload" tab**
3. **Choose what to upload**:
   - Job descriptions
   - Job tasks
   - Required skills
   - Skill definitions
   - Knowledge areas

4. **Download Templates** to see the format
5. **Upload Your File**
6. **Preview** to check everything looks right
7. **Confirm** to update the system

### What Each Upload Does

- **Job Role Description**: Defines different jobs and what they involve
- **Job Tasks**: Lists what people actually do in each job
- **Job Skills**: Shows what skills each job needs
- **Skills Master**: Complete list of all skills in the system
- **Knowledge & Abilities**: Detailed breakdown of what each skill involves

### Important Admin Notes

- Always backup data before uploading new files
- CSV files completely replace existing data
- Use UTF-8 encoding (standard for most spreadsheet apps)
- Check the preview carefully before confirming

## Technical Details

### How the App is Built

- **Frontend**: Streamlit (Python web framework - makes it easy to build)
- **Charts**: Plotly (creates the interactive spider diagrams)
- **AI**: OpenAI GPT (with Anthropic Claude and Google Gemini as backups)
- **Data**: Stored as JSON files (like organized text files)
- **PWA**: Service Worker (makes it work offline)

### File Structure
```
career-atlas/
├── app.py                    # Main application file
├── pages/                    # Different screens
│   ├── welcome.py           # Home screen
│   ├── riasec_assessment.py # Personality test
│   ├── skills_assessment.py # Skills rating
│   ├── values_assessment.py # Values ranking
│   ├── results.py          # Show results
│   ├── comparison_view.py  # NEW! Spider diagram
│   └── admin_panel.py      # Admin controls
├── utils/                   # Helper code
│   ├── ai_manager.py       # AI integration
│   ├── auth_manager.py     # Login system
│   └── pwa_injector.py     # NEW! App functionality
├── data/                    # All your data
│   ├── assessments/        # Test questions
│   ├── careers/            # Job information
│   ├── jobskills/          # NEW! Skills mapping
│   └── users/              # User profiles
└── static/                  # NEW! App files
    ├── manifest.json       # App configuration
    └── service-worker.js   # Offline functionality
```

### Security & Privacy

- Passwords are checked but stored simply (not for production use)
- User data stays on your server
- AI providers only see anonymous assessment data
- No personal information is sent to AI services

## What's New

### Recent Updates

1. **📱 Progressive Web App (PWA)**
   - Install on any device like a native app
   - Works offline with cached data
   - Fast loading with saved resources
   - Full-screen app experience

2. **📊 RIASEC vs Skills Comparison**
   - Visual spider diagram showing interests vs abilities
   - Identifies skill gaps and hidden strengths
   - Recommends careers matching both interests AND skills
   - Supports multiple data formats (JSON and CSV)

3. **📤 Enhanced Admin Upload**
   - Support for 5 different CSV file types
   - Real-time validation with helpful error messages
   - Preview before confirming changes
   - Template downloads with examples

4. **🤖 Smarter AI Coaching**
   - Questions tailored to personality type
   - Separate modes for coaches and managers
   - Team dynamics analysis
   - Fallback questions when AI unavailable

5. **🎨 Better User Experience**
   - Cleaner, more modern design
   - Faster page loads
   - Better mobile responsiveness
   - Progress tracking dashboard

### Coming Soon

- **💾 Auto-Save**: Never lose your progress
- **📄 PDF Reports**: Download and print your results  
- **🤔 Smart Q&A**: Ask questions about your results
- **🔔 Notifications**: Reminders and updates

## Troubleshooting

### Common Issues

**"Can't login"**
- Check username and password (case sensitive)
- Demo: username `demo`, password `demo123`

**"No AI recommendations"**
- Check if API keys are set in `.env` file
- System works without keys but with limited features

**"Can't install as app"**
- Use Chrome, Edge, or Safari
- Must be HTTPS in production (localhost works for testing)

**"Upload failed"**
- Check CSV format matches template
- Ensure UTF-8 encoding
- Look for specific error messages

**"Offline not working"**
- Clear browser cache and reinstall
- Check if service worker is registered
- Some features need internet (AI recommendations)

### Getting Help

1. Check the error message - they're designed to be helpful
2. Try logging out and back in
3. Clear your browser cache
4. For developers: Check browser console for errors

## For Developers

### Adding New Features

The codebase is modular and easy to extend:

1. **New Assessment**: Add to `pages/` and update navigation
2. **New AI Feature**: Extend `AIManager` class
3. **New Data Type**: Add to `DataManager` and create CSV validator
4. **New Chart**: Use Plotly in new page component

### API Integration

The app supports multiple AI providers with automatic fallback:
```python
# Priority order:
1. OpenAI (GPT-3.5/4)
2. Anthropic (Claude)
3. Google (Gemini)
4. Offline fallback
```

### Contributing

1. Fork the repository
2. Create feature branch
3. Make changes with clear commits
4. Add tests if applicable
5. Submit pull request

## Final Notes

Career Atlas is designed to be helpful, not prescriptive. Use it as a guide for self-discovery and career exploration. Remember:

- Your results are a starting point, not a final destination
- Careers can change and evolve - so can you!
- The "best" career is one that makes YOU happy
- Skills can be learned - interests are harder to change

Happy career exploring! 🚀

---

*Built with ❤️ to make career guidance accessible to everyone*

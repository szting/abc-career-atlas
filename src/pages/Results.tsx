import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import Layout from '../components/Layout'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from 'recharts'
import { Download, Share2, Search } from 'lucide-react'
import './Results.css'

interface RIASECScores {
  R: number
  I: number
  A: number
  S: number
  E: number
  C: number
}

const categoryDescriptions = {
  R: { name: 'Realistic', description: 'Practical, hands-on, physical activities' },
  I: { name: 'Investigative', description: 'Thinking, researching, analyzing' },
  A: { name: 'Artistic', description: 'Creative, expressive, imaginative' },
  S: { name: 'Social', description: 'Helping, teaching, counseling' },
  E: { name: 'Enterprising', description: 'Leading, persuading, selling' },
  C: { name: 'Conventional', description: 'Organizing, structuring, processing' }
}

const careerSuggestions = {
  R: ['Engineer', 'Mechanic', 'Carpenter', 'Electrician', 'Pilot'],
  I: ['Scientist', 'Researcher', 'Doctor', 'Data Analyst', 'Software Developer'],
  A: ['Artist', 'Designer', 'Writer', 'Musician', 'Photographer'],
  S: ['Teacher', 'Counselor', 'Social Worker', 'Nurse', 'HR Manager'],
  E: ['Entrepreneur', 'Sales Manager', 'Marketing Director', 'CEO', 'Lawyer'],
  C: ['Accountant', 'Administrator', 'Project Manager', 'Auditor', 'Office Manager']
}

export default function Results() {
  const [scores, setScores] = useState<RIASECScores | null>(null)
  
  useEffect(() => {
    const savedResults = localStorage.getItem('assessmentResults')
    if (savedResults) {
      setScores(JSON.parse(savedResults))
    }
  }, [])
  
  if (!scores) {
    return (
      <Layout>
        <div className="results-empty">
          <h2>No assessment results found</h2>
          <p>Please complete the assessment first</p>
          <Link to="/assessment" className="cta-button">
            Take Assessment
          </Link>
        </div>
      </Layout>
    )
  }
  
  const chartData = Object.entries(scores).map(([key, value]) => ({
    category: categoryDescriptions[key as keyof typeof categoryDescriptions].name,
    score: value,
    fullMark: 25
  }))
  
  const topCategories = Object.entries(scores)
    .sort(([, a], [, b]) => b - a)
    .slice(0, 3)
    .map(([key]) => key as keyof typeof categoryDescriptions)
  
  return (
    <Layout>
      <div className="results">
        <div className="results-header">
          <h1>Your RIASEC Assessment Results</h1>
          <p>Based on your responses, here's your career interest profile</p>
        </div>
        
        <div className="charts-container">
          <div className="chart-card">
            <h3>Score Distribution</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="category" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="score" fill="#3498db" />
              </BarChart>
            </ResponsiveContainer>
          </div>
          
          <div className="chart-card">
            <h3>Interest Profile</h3>
            <ResponsiveContainer width="100%" height={300}>
              <RadarChart data={chartData}>
                <PolarGrid />
                <PolarAngleAxis dataKey="category" />
                <PolarRadiusAxis angle={90} domain={[0, 25]} />
                <Radar name="Score" dataKey="score" stroke="#3498db" fill="#3498db" fillOpacity={0.6} />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </div>
        
        <div className="top-interests">
          <h2>Your Top Interest Areas</h2>
          <div className="interest-cards">
            {topCategories.map((category, index) => (
              <div key={category} className="interest-card">
                <div className="rank">#{index + 1}</div>
                <h3>{categoryDescriptions[category].name}</h3>
                <p>{categoryDescriptions[category].description}</p>
                <div className="score">Score: {scores[category]}/25</div>
              </div>
            ))}
          </div>
        </div>
        
        <div className="career-suggestions">
          <h2>Suggested Career Paths</h2>
          <div className="career-grid">
            {topCategories.map(category => (
              <div key={category} className="career-category">
                <h4>{categoryDescriptions[category].name} Careers</h4>
                <ul>
                  {careerSuggestions[category].map(career => (
                    <li key={career}>{career}</li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
        
        <div className="action-buttons">
          <button className="action-button">
            <Download size={20} />
            Download Report
          </button>
          <button className="action-button">
            <Share2 size={20} />
            Share Results
          </button>
          <Link to="/career-exploration" className="action-button primary">
            <Search size={20} />
            Explore Careers
          </Link>
        </div>
      </div>
    </Layout>
  )
}

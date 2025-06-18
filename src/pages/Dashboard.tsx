import React from 'react'
import { Link } from 'react-router-dom'
import Layout from '../components/Layout'
import { FileText, Search, Brain, TrendingUp, BookOpen, Users, Award, Target } from 'lucide-react'
import './Dashboard.css'

export default function Dashboard() {
  const features = [
    {
      icon: FileText,
      title: 'Career Assessment',
      description: 'Take the RIASEC assessment to discover your career interests',
      link: '/assessment',
      color: '#3498db'
    },
    {
      icon: Search,
      title: 'Career Exploration',
      description: 'Explore careers that match your interests and skills',
      link: '/career-exploration',
      color: '#e74c3c'
    },
    {
      icon: Brain,
      title: 'AI Guidance',
      description: 'Get personalized career advice from AI counselors',
      link: '/ai-guidance',
      color: '#f39c12'
    },
    {
      icon: TrendingUp,
      title: 'Track Progress',
      description: 'Monitor your career development journey',
      link: '/progress',
      color: '#27ae60'
    },
    {
      icon: BookOpen,
      title: 'Resources',
      description: 'Access career guides, tips, and educational materials',
      link: '/resources',
      color: '#9b59b6'
    }
  ]

  const stats = [
    { icon: Users, label: 'Active Users', value: '1,234' },
    { icon: Award, label: 'Assessments Completed', value: '5,678' },
    { icon: Target, label: 'Career Matches', value: '9,012' }
  ]

  return (
    <Layout>
      <div className="dashboard">
        <div className="dashboard-header">
          <h1>Welcome to ABC Career Atlas</h1>
          <p>Your personalized career guidance platform</p>
        </div>

        <div className="stats-grid">
          {stats.map((stat, index) => {
            const Icon = stat.icon
            return (
              <div key={index} className="stat-card">
                <Icon size={32} />
                <div>
                  <h3>{stat.value}</h3>
                  <p>{stat.label}</p>
                </div>
              </div>
            )
          })}
        </div>

        <div className="features-grid">
          {features.map((feature, index) => {
            const Icon = feature.icon
            return (
              <Link key={index} to={feature.link} className="feature-card">
                <div className="feature-icon" style={{ backgroundColor: feature.color }}>
                  <Icon size={32} color="white" />
                </div>
                <h3>{feature.title}</h3>
                <p>{feature.description}</p>
              </Link>
            )
          })}
        </div>

        <div className="quick-start">
          <h2>Quick Start Guide</h2>
          <ol>
            <li>Take the RIASEC career assessment to identify your interests</li>
            <li>Explore careers that match your profile</li>
            <li>Get personalized guidance from our AI counselors</li>
            <li>Track your progress and set career goals</li>
            <li>Access resources to develop your skills</li>
          </ol>
        </div>
      </div>
    </Layout>
  )
}

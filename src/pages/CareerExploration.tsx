import React, { useState } from 'react'
import Layout from '../components/Layout'
import { Search, Filter, Briefcase, DollarSign, TrendingUp, MapPin, Clock, Users } from 'lucide-react'
import './CareerExploration.css'

const careers = [
  {
    id: 1,
    title: 'Software Developer',
    category: 'Technology',
    riasec: ['I', 'R'],
    salary: '$85,000 - $130,000',
    growth: '+22%',
    description: 'Design, develop, and maintain software applications',
    skills: ['Programming', 'Problem Solving', 'Teamwork'],
    education: "Bachelor's degree in Computer Science",
    workEnvironment: 'Office/Remote',
    image: 'https://images.pexels.com/photos/574071/pexels-photo-574071.jpeg?auto=compress&cs=tinysrgb&w=600'
  },
  {
    id: 2,
    title: 'Registered Nurse',
    category: 'Healthcare',
    riasec: ['S', 'I'],
    salary: '$75,000 - $95,000',
    growth: '+7%',
    description: 'Provide medical care and support to patients',
    skills: ['Patient Care', 'Communication', 'Critical Thinking'],
    education: "Bachelor's degree in Nursing",
    workEnvironment: 'Hospital/Clinic',
    image: 'https://images.pexels.com/photos/4173251/pexels-photo-4173251.jpeg?auto=compress&cs=tinysrgb&w=600'
  },
  {
    id: 3,
    title: 'Marketing Manager',
    category: 'Business',
    riasec: ['E', 'A'],
    salary: '$70,000 - $120,000',
    growth: '+10%',
    description: 'Develop and implement marketing strategies',
    skills: ['Leadership', 'Creativity', 'Analytics'],
    education: "Bachelor's degree in Marketing",
    workEnvironment: 'Office',
    image: 'https://images.pexels.com/photos/3184465/pexels-photo-3184465.jpeg?auto=compress&cs=tinysrgb&w=600'
  },
  {
    id: 4,
    title: 'Mechanical Engineer',
    category: 'Engineering',
    riasec: ['R', 'I'],
    salary: '$80,000 - $110,000',
    growth: '+4%',
    description: 'Design and develop mechanical systems',
    skills: ['CAD', 'Mathematics', 'Problem Solving'],
    education: "Bachelor's degree in Mechanical Engineering",
    workEnvironment: 'Office/Field',
    image: 'https://images.pexels.com/photos/2760241/pexels-photo-2760241.jpeg?auto=compress&cs=tinysrgb&w=600'
  },
  {
    id: 5,
    title: 'Graphic Designer',
    category: 'Creative',
    riasec: ['A', 'E'],
    salary: '$50,000 - $75,000',
    growth: '+3%',
    description: 'Create visual content for various media',
    skills: ['Design Software', 'Creativity', 'Communication'],
    education: "Bachelor's degree in Graphic Design",
    workEnvironment: 'Office/Remote',
    image: 'https://images.pexels.com/photos/196644/pexels-photo-196644.jpeg?auto=compress&cs=tinysrgb&w=600'
  },
  {
    id: 6,
    title: 'Financial Analyst',
    category: 'Finance',
    riasec: ['C', 'I'],
    salary: '$65,000 - $95,000',
    growth: '+6%',
    description: 'Analyze financial data and provide insights',
    skills: ['Excel', 'Analytics', 'Attention to Detail'],
    education: "Bachelor's degree in Finance",
    workEnvironment: 'Office',
    image: 'https://images.pexels.com/photos/7681091/pexels-photo-7681091.jpeg?auto=compress&cs=tinysrgb&w=600'
  }
]

const categories = ['All', 'Technology', 'Healthcare', 'Business', 'Engineering', 'Creative', 'Finance']

export default function CareerExploration() {
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('All')
  const [selectedCareer, setSelectedCareer] = useState<typeof careers[0] | null>(null)
  
  const filteredCareers = careers.filter(career => {
    const matchesSearch = career.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         career.description.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesCategory = selectedCategory === 'All' || career.category === selectedCategory
    return matchesSearch && matchesCategory
  })
  
  return (
    <Layout>
      <div className="career-exploration">
        <div className="exploration-header">
          <h1>Explore Career Paths</h1>
          <p>Discover careers that match your interests and goals</p>
        </div>
        
        <div className="search-section">
          <div className="search-bar">
            <Search size={20} />
            <input
              type="text"
              placeholder="Search careers..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          
          <div className="category-filters">
            {categories.map(category => (
              <button
                key={category}
                className={`filter-button ${selectedCategory === category ? 'active' : ''}`}
                onClick={() => setSelectedCategory(category)}
              >
                {category}
              </button>
            ))}
          </div>
        </div>
        
        <div className="careers-grid">
          {filteredCareers.map(career => (
            <div
              key={career.id}
              className="career-card"
              onClick={() => setSelectedCareer(career)}
            >
              <img src={career.image} alt={career.title} />
              <div className="career-content">
                <h3>{career.title}</h3>
                <p className="career-category">{career.category}</p>
                <p className="career-description">{career.description}</p>
                
                <div className="career-stats">
                  <div className="stat">
                    <DollarSign size={16} />
                    <span>{career.salary}</span>
                  </div>
                  <div className="stat">
                    <TrendingUp size={16} />
                    <span>{career.growth}</span>
                  </div>
                </div>
                
                <div className="riasec-tags">
                  {career.riasec.map(tag => (
                    <span key={tag} className="riasec-tag">{tag}</span>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>
        
        {selectedCareer && (
          <div className="career-modal" onClick={() => setSelectedCareer(null)}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
              <button className="close-button" onClick={() => setSelectedCareer(null)}>×</button>
              
              <img src={selectedCareer.image} alt={selectedCareer.title} />
              
              <h2>{selectedCareer.title}</h2>
              <p className="modal-category">{selectedCareer.category}</p>
              
              <div className="modal-section">
                <h3>Overview</h3>
                <p>{selectedCareer.description}</p>
              </div>
              
              <div className="modal-stats">
                <div className="stat-item">
                  <DollarSign size={20} />
                  <div>
                    <h4>Salary Range</h4>
                    <p>{selectedCareer.salary}</p>
                  </div>
                </div>
                <div className="stat-item">
                  <TrendingUp size={20} />
                  <div>
                    <h4>Job Growth</h4>
                    <p>{selectedCareer.growth}</p>
                  </div>
                </div>
                <div className="stat-item">
                  <MapPin size={20} />
                  <div>
                    <h4>Work Environment</h4>
                    <p>{selectedCareer.workEnvironment}</p>
                  </div>
                </div>
              </div>
              
              <div className="modal-section">
                <h3>Required Skills</h3>
                <div className="skills-list">
                  {selectedCareer.skills.map(skill => (
                    <span key={skill} className="skill-tag">{skill}</span>
                  ))}
                </div>
              </div>
              
              <div className="modal-section">
                <h3>Education Requirements</h3>
                <p>{selectedCareer.education}</p>
              </div>
              
              <div className="modal-section">
                <h3>RIASEC Profile</h3>
                <div className="riasec-tags">
                  {selectedCareer.riasec.map(tag => (
                    <span key={tag} className="riasec-tag large">{tag}</span>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </Layout>
  )
}

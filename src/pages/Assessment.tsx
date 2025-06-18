import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import Layout from '../components/Layout'
import { ChevronRight, ChevronLeft } from 'lucide-react'
import './Assessment.css'

const questions = [
  // Realistic
  { id: 1, text: "I enjoy working with tools and machines", category: "R" },
  { id: 2, text: "I like to build or fix things with my hands", category: "R" },
  { id: 3, text: "I prefer outdoor activities over indoor activities", category: "R" },
  { id: 4, text: "I enjoy working on practical, hands-on projects", category: "R" },
  { id: 5, text: "I like physical activities and sports", category: "R" },
  
  // Investigative
  { id: 6, text: "I enjoy solving complex problems and puzzles", category: "I" },
  { id: 7, text: "I like to understand how things work", category: "I" },
  { id: 8, text: "I enjoy conducting research and experiments", category: "I" },
  { id: 9, text: "I prefer working with ideas and theories", category: "I" },
  { id: 10, text: "I like analyzing data and information", category: "I" },
  
  // Artistic
  { id: 11, text: "I enjoy creative activities like art, music, or writing", category: "A" },
  { id: 12, text: "I like to express myself through creative work", category: "A" },
  { id: 13, text: "I prefer unstructured, flexible environments", category: "A" },
  { id: 14, text: "I enjoy coming up with new ideas and concepts", category: "A" },
  { id: 15, text: "I like to work on projects that allow creativity", category: "A" },
  
  // Social
  { id: 16, text: "I enjoy helping and teaching others", category: "S" },
  { id: 17, text: "I like working in teams and groups", category: "S" },
  { id: 18, text: "I prefer jobs that involve interacting with people", category: "S" },
  { id: 19, text: "I enjoy volunteering and community service", category: "S" },
  { id: 20, text: "I like to mentor or coach others", category: "S" },
  
  // Enterprising
  { id: 21, text: "I enjoy leading and managing projects", category: "E" },
  { id: 22, text: "I like to persuade and influence others", category: "E" },
  { id: 23, text: "I enjoy taking risks and starting new ventures", category: "E" },
  { id: 24, text: "I prefer competitive environments", category: "E" },
  { id: 25, text: "I like to set goals and achieve them", category: "E" },
  
  // Conventional
  { id: 26, text: "I enjoy organizing and structuring information", category: "C" },
  { id: 27, text: "I like following established procedures", category: "C" },
  { id: 28, text: "I prefer working with numbers and data", category: "C" },
  { id: 29, text: "I enjoy detailed, precise work", category: "C" },
  { id: 30, text: "I like maintaining records and files", category: "C" }
]

export default function Assessment() {
  const navigate = useNavigate()
  const [currentQuestion, setCurrentQuestion] = useState(0)
  const [answers, setAnswers] = useState<Record<number, number>>({})
  
  const handleAnswer = (value: number) => {
    setAnswers({ ...answers, [questions[currentQuestion].id]: value })
  }
  
  const handleNext = () => {
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1)
    } else {
      // Calculate results
      const scores = { R: 0, I: 0, A: 0, S: 0, E: 0, C: 0 }
      questions.forEach(q => {
        scores[q.category as keyof typeof scores] += answers[q.id] || 0
      })
      
      // Store results and navigate
      localStorage.setItem('assessmentResults', JSON.stringify(scores))
      navigate('/results')
    }
  }
  
  const handlePrevious = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(currentQuestion - 1)
    }
  }
  
  const progress = ((currentQuestion + 1) / questions.length) * 100
  
  return (
    <Layout>
      <div className="assessment">
        <div className="assessment-header">
          <h1>RIASEC Career Assessment</h1>
          <p>Answer each question based on how much you agree with the statement</p>
        </div>
        
        <div className="assessment-progress">
          <div className="progress-bar">
            <div className="progress-fill" style={{ width: `${progress}%` }} />
          </div>
          <p>Question {currentQuestion + 1} of {questions.length}</p>
        </div>
        
        <div className="question-card">
          <h2>{questions[currentQuestion].text}</h2>
          
          <div className="answer-options">
            {[1, 2, 3, 4, 5].map(value => (
              <button
                key={value}
                className={`answer-button ${answers[questions[currentQuestion].id] === value ? 'selected' : ''}`}
                onClick={() => handleAnswer(value)}
              >
                {value === 1 && 'Strongly Disagree'}
                {value === 2 && 'Disagree'}
                {value === 3 && 'Neutral'}
                {value === 4 && 'Agree'}
                {value === 5 && 'Strongly Agree'}
              </button>
            ))}
          </div>
          
          <div className="navigation-buttons">
            <button
              className="nav-button"
              onClick={handlePrevious}
              disabled={currentQuestion === 0}
            >
              <ChevronLeft size={20} />
              Previous
            </button>
            
            <button
              className="nav-button primary"
              onClick={handleNext}
              disabled={!answers[questions[currentQuestion].id]}
            >
              {currentQuestion === questions.length - 1 ? 'Finish' : 'Next'}
              <ChevronRight size={20} />
            </button>
          </div>
        </div>
      </div>
    </Layout>
  )
}

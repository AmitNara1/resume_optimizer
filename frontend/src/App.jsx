import { useState } from 'react'
import './App.css'

function App() {
  const [file, setFile] = useState(null)
  const [feedback, setFeedback] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleFileUpload = async (e) => {
    const uploadedFile = e.target.files[0]
    setFile(uploadedFile)
  }

  const handleSubmit = async () => {
    if (!file) {
      alert('Please upload a file')
      return
    }

    setLoading(true)
    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch('http://localhost:8000/analyze', {
        method: 'POST',
        body: formData,
      })
      const data = await response.json()
      setFeedback(data)
    } catch (error) {
      console.error('Error:', error)
    }
    setLoading(false)
  }

  return (
    <div className="container">
      <h1>Resume Optimizer</h1>
      <input 
        type="file" 
        onChange={handleFileUpload}
        accept=".pdf,.txt,.docx"
      />
      <button onClick={handleSubmit} disabled={loading}>
        {loading ? 'Analyzing...' : 'Analyze Resume'}
      </button>
      {feedback && (
        <div className="feedback">
          <h2>Feedback</h2>
          <p>{feedback.suggestions}</p>
        </div>
      )}
    </div>
  )
}

export default App

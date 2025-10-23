import { useState } from 'react'
import Header from './components/Header'
import UploadSection from './components/UploadSection'
import AnalysisProgress from './components/AnalysisProgress'
import ResultsDashboard from './components/ResultsDashboard'
import ErrorMessage from './components/ErrorMessage'
import { analyzeResume } from './services/api'

function App() {
  const [stage, setStage] = useState('upload') // 'upload', 'analyzing', 'results', 'error'
  const [analysisResult, setAnalysisResult] = useState(null)
  const [error, setError] = useState(null)
  const [progress, setProgress] = useState(0)
  const [currentStep, setCurrentStep] = useState('')

  const handleFileUpload = async (file) => {
    setStage('analyzing')
    setError(null)
    setProgress(0)

    // Simulate progress steps
    const steps = [
      { progress: 10, message: 'Uploading file...' },
      { progress: 30, message: 'Extracting text...' },
      { progress: 60, message: 'Analyzing skills and experience...' },
      { progress: 80, message: 'Generating AI suggestions...' },
      { progress: 95, message: 'Finalizing results...' },
    ]

    let currentStepIndex = 0

    const progressInterval = setInterval(() => {
      if (currentStepIndex < steps.length) {
        setProgress(steps[currentStepIndex].progress)
        setCurrentStep(steps[currentStepIndex].message)
        currentStepIndex++
      }
    }, 1000)

    try {
      const result = await analyzeResume(file)
      clearInterval(progressInterval)
      setProgress(100)
      setAnalysisResult(result)
      setTimeout(() => {
        setStage('results')
      }, 500)
    } catch (err) {
      clearInterval(progressInterval)
      setError(err.message || 'An error occurred during analysis')
      setStage('error')
    }
  }

  const handleReset = () => {
    setStage('upload')
    setAnalysisResult(null)
    setError(null)
    setProgress(0)
    setCurrentStep('')
  }

  return (
    <div className="min-h-screen bg-background">
      <Header />

      <div className="container mx-auto px-4 py-8 max-w-7xl">
        {stage === 'upload' && (
          <UploadSection onFileUpload={handleFileUpload} />
        )}

        {stage === 'analyzing' && (
          <AnalysisProgress
            progress={progress}
            currentStep={currentStep}
            onCancel={handleReset}
          />
        )}

        {stage === 'results' && analysisResult && (
          <ResultsDashboard
            data={analysisResult}
            onNewAnalysis={handleReset}
          />
        )}

        {stage === 'error' && (
          <ErrorMessage
            error={error}
            onRetry={handleReset}
          />
        )}
      </div>
    </div>
  )
}

export default App

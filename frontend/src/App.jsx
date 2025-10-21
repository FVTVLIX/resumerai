import { useState } from 'react'
import { ThemeProvider, createTheme, CssBaseline, Container, Box } from '@mui/material'
import Header from './components/Header'
import UploadSection from './components/UploadSection'
import AnalysisProgress from './components/AnalysisProgress'
import ResultsDashboard from './components/ResultsDashboard'
import ErrorMessage from './components/ErrorMessage'
import { analyzeResume } from './services/api'

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976D2',
      light: '#42A5F5',
      dark: '#1565C0',
    },
    secondary: {
      main: '#DC004E',
      light: '#F50057',
      dark: '#C51162',
    },
    success: {
      main: '#4CAF50',
    },
    warning: {
      main: '#FF9800',
    },
    error: {
      main: '#F44336',
    },
    info: {
      main: '#2196F3',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontSize: '2.5rem',
      fontWeight: 700,
      letterSpacing: '-0.5px',
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 700,
    },
    h3: {
      fontSize: '1.5rem',
      fontWeight: 500,
    },
  },
})

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
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ minHeight: '100vh', bgcolor: 'background.default' }}>
        <Header />

        <Container maxWidth="lg" sx={{ py: 4 }}>
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
        </Container>
      </Box>
    </ThemeProvider>
  )
}

export default App

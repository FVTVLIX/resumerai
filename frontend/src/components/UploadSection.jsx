import { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, CheckCircle, TrendingUp, Lightbulb, X } from 'lucide-react'
import { Button } from './ui/button'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from './ui/card'
import { Alert, AlertDescription } from './ui/alert'

function UploadSection({ onFileUpload }) {
  const [selectedFile, setSelectedFile] = useState(null)
  const [error, setError] = useState(null)

  const onDrop = useCallback((acceptedFiles, rejectedFiles) => {
    setError(null)

    if (rejectedFiles && rejectedFiles.length > 0) {
      const rejection = rejectedFiles[0]
      if (rejection.errors[0]?.code === 'file-too-large') {
        setError('File size exceeds 5MB limit')
      } else if (rejection.errors[0]?.code === 'file-invalid-type') {
        setError('Only PDF and DOCX files are supported')
      } else {
        setError('File validation failed')
      }
      return
    }

    if (acceptedFiles && acceptedFiles.length > 0) {
      setSelectedFile(acceptedFiles[0])
    }
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
    },
    maxSize: 5 * 1024 * 1024, // 5MB
    multiple: false,
  })

  const handleAnalyze = () => {
    if (selectedFile) {
      onFileUpload(selectedFile)
    }
  }

  const handleClear = () => {
    setSelectedFile(null)
    setError(null)
  }

  return (
    <div className="space-y-8">
      {/* Hero Section */}
      <div className="text-center mt-4 mb-6">
        <h1 className="text-4xl font-bold tracking-tight mb-3">
          Optimize Your Resume with AI
        </h1>
        <p className="text-lg text-muted-foreground mb-4">
          Get instant feedback and improve your job prospects
        </p>
      </div>

      {/* Upload Area */}
      <div
        className={`
          p-8 mb-4 rounded-lg border-2 cursor-pointer transition-all duration-300
          ${isDragActive
            ? 'border-primary bg-primary/5 border-solid'
            : 'border-dashed border-border hover:border-primary hover:bg-accent'
          }
        `}
        {...getRootProps()}
      >
        <input {...getInputProps()} />
        <div className="text-center">
          <Upload className="mx-auto h-20 w-20 text-primary mb-4" />
          <h2 className="text-xl font-semibold mb-2">
            {isDragActive ? 'Drop your resume here' : 'Drag & drop your resume here'}
          </h2>
          <p className="text-muted-foreground mb-2">
            or click to browse
          </p>
          <p className="text-sm text-muted-foreground">
            Supported formats: PDF, DOCX (Max 5MB)
          </p>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <Alert variant="destructive" className="mb-3">
          <AlertDescription className="flex items-center justify-between">
            <span>{error}</span>
            <button
              onClick={() => setError(null)}
              className="ml-4 hover:opacity-70"
              aria-label="Close"
            >
              <X className="h-4 w-4" />
            </button>
          </AlertDescription>
        </Alert>
      )}

      {/* Selected File */}
      {selectedFile && (
        <div className="p-4 mb-4 rounded-lg bg-green-50 border border-green-200">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <CheckCircle className="h-8 w-8 text-green-600" />
              <div>
                <h3 className="font-semibold text-green-900">File Selected</h3>
                <p className="text-sm text-green-700">
                  {selectedFile.name} ({(selectedFile.size / 1024).toFixed(2)} KB)
                </p>
              </div>
            </div>
            <div className="flex gap-2">
              <Button
                size="lg"
                onClick={handleAnalyze}
              >
                Analyze Resume
              </Button>
              <Button
                variant="outline"
                onClick={handleClear}
              >
                Clear
              </Button>
            </div>
          </div>
        </div>
      )}

      {/* Features Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
        <Card>
          <CardContent className="text-center pt-6 pb-6">
            <CheckCircle className="mx-auto h-15 w-15 text-primary mb-4" />
            <CardTitle className="mb-2">Accurate Analysis</CardTitle>
            <CardDescription>
              Advanced NLP algorithms extract skills, experience, and education with high precision
            </CardDescription>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="text-center pt-6 pb-6">
            <TrendingUp className="mx-auto h-15 w-15 text-primary mb-4" />
            <CardTitle className="mb-2">Detailed Insights</CardTitle>
            <CardDescription>
              Comprehensive breakdown of your resume including skills, experience timeline, and metrics
            </CardDescription>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="text-center pt-6 pb-6">
            <Lightbulb className="mx-auto h-15 w-15 text-primary mb-4" />
            <CardTitle className="mb-2">Actionable Suggestions</CardTitle>
            <CardDescription>
              AI-powered recommendations to improve your resume and optimize for ATS systems
            </CardDescription>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

export default UploadSection

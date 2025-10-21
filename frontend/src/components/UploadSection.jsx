import { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import {
  Box,
  Paper,
  Typography,
  Button,
  Grid,
  Card,
  CardContent,
  Alert,
} from '@mui/material'
import CloudUploadIcon from '@mui/icons-material/CloudUpload'
import CheckCircleIcon from '@mui/icons-material/CheckCircle'
import TimelineIcon from '@mui/icons-material/Timeline'
import TipsAndUpdatesIcon from '@mui/icons-material/TipsAndUpdates'

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
    <Box>
      {/* Hero Section */}
      <Box sx={{ textAlign: 'center', mb: 6, mt: 4 }}>
        <Typography variant="h1" gutterBottom>
          Optimize Your Resume with AI
        </Typography>
        <Typography variant="h6" color="text.secondary" sx={{ mb: 4 }}>
          Get instant feedback and improve your job prospects
        </Typography>
      </Box>

      {/* Upload Area */}
      <Paper
        elevation={3}
        sx={{
          p: 4,
          mb: 4,
          border: isDragActive ? '2px solid' : '2px dashed',
          borderColor: isDragActive ? 'primary.main' : 'grey.300',
          bgcolor: isDragActive ? 'primary.light' : 'background.paper',
          cursor: 'pointer',
          transition: 'all 0.3s ease',
          '&:hover': {
            borderColor: 'primary.main',
            bgcolor: 'action.hover',
          },
        }}
        {...getRootProps()}
      >
        <input {...getInputProps()} />
        <Box sx={{ textAlign: 'center' }}>
          <CloudUploadIcon sx={{ fontSize: 80, color: 'primary.main', mb: 2 }} />
          <Typography variant="h5" gutterBottom>
            {isDragActive ? 'Drop your resume here' : 'Drag & drop your resume here'}
          </Typography>
          <Typography variant="body1" color="text.secondary" sx={{ mb: 2 }}>
            or click to browse
          </Typography>
          <Typography variant="caption" color="text.secondary">
            Supported formats: PDF, DOCX (Max 5MB)
          </Typography>
        </Box>
      </Paper>

      {/* Error Message */}
      {error && (
        <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      {/* Selected File */}
      {selectedFile && (
        <Paper elevation={2} sx={{ p: 3, mb: 4, bgcolor: 'success.light', color: 'success.contrastText' }}>
          <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <Box sx={{ display: 'flex', alignItems: 'center' }}>
              <CheckCircleIcon sx={{ mr: 2, fontSize: 32 }} />
              <Box>
                <Typography variant="h6">File Selected</Typography>
                <Typography variant="body2">
                  {selectedFile.name} ({(selectedFile.size / 1024).toFixed(2)} KB)
                </Typography>
              </Box>
            </Box>
            <Box>
              <Button
                variant="contained"
                color="primary"
                size="large"
                onClick={handleAnalyze}
                sx={{ mr: 2 }}
              >
                Analyze Resume
              </Button>
              <Button
                variant="outlined"
                color="inherit"
                onClick={handleClear}
              >
                Clear
              </Button>
            </Box>
          </Box>
        </Paper>
      )}

      {/* Features Grid */}
      <Grid container spacing={3} sx={{ mt: 2 }}>
        <Grid item xs={12} md={4}>
          <Card elevation={2}>
            <CardContent sx={{ textAlign: 'center', py: 4 }}>
              <CheckCircleIcon sx={{ fontSize: 60, color: 'primary.main', mb: 2 }} />
              <Typography variant="h6" gutterBottom>
                Accurate Analysis
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Advanced NLP algorithms extract skills, experience, and education with high precision
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card elevation={2}>
            <CardContent sx={{ textAlign: 'center', py: 4 }}>
              <TimelineIcon sx={{ fontSize: 60, color: 'primary.main', mb: 2 }} />
              <Typography variant="h6" gutterBottom>
                Detailed Insights
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Comprehensive breakdown of your resume including skills, experience timeline, and metrics
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card elevation={2}>
            <CardContent sx={{ textAlign: 'center', py: 4 }}>
              <TipsAndUpdatesIcon sx={{ fontSize: 60, color: 'primary.main', mb: 2 }} />
              <Typography variant="h6" gutterBottom>
                Actionable Suggestions
              </Typography>
              <Typography variant="body2" color="text.secondary">
                AI-powered recommendations to improve your resume and optimize for ATS systems
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  )
}

export default UploadSection

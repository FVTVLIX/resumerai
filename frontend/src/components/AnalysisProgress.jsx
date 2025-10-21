import {
  Box,
  Paper,
  Typography,
  LinearProgress,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Button,
  CircularProgress,
} from '@mui/material'
import CheckCircleIcon from '@mui/icons-material/CheckCircle'
import RadioButtonUncheckedIcon from '@mui/icons-material/RadioButtonUnchecked'
import AutorenewIcon from '@mui/icons-material/Autorenew'

const steps = [
  { id: 1, label: 'File uploaded successfully', threshold: 10 },
  { id: 2, label: 'Text extracted', threshold: 30 },
  { id: 3, label: 'Analyzing skills and experience', threshold: 60 },
  { id: 4, label: 'Generating AI suggestions', threshold: 80 },
  { id: 5, label: 'Finalizing results', threshold: 95 },
]

function AnalysisProgress({ progress, currentStep, onCancel }) {
  const getStepStatus = (stepThreshold) => {
    if (progress >= stepThreshold) {
      return 'completed'
    } else if (progress >= stepThreshold - 20) {
      return 'in-progress'
    }
    return 'pending'
  }

  return (
    <Box sx={{ maxWidth: 800, mx: 'auto', mt: 8 }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        <Typography variant="h4" gutterBottom align="center">
          Analyzing Your Resume...
        </Typography>

        <Typography
          variant="body1"
          color="text.secondary"
          align="center"
          sx={{ mb: 4 }}
        >
          This usually takes 10-15 seconds...
        </Typography>

        {/* Progress Bar */}
        <Box sx={{ mb: 4 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
            <Box sx={{ width: '100%', mr: 2 }}>
              <LinearProgress
                variant="determinate"
                value={progress}
                sx={{ height: 10, borderRadius: 5 }}
              />
            </Box>
            <Box sx={{ minWidth: 50 }}>
              <Typography variant="body2" color="text.secondary">
                {Math.round(progress)}%
              </Typography>
            </Box>
          </Box>
        </Box>

        {/* Steps List */}
        <List>
          {steps.map((step) => {
            const status = getStepStatus(step.threshold)
            return (
              <ListItem key={step.id}>
                <ListItemIcon>
                  {status === 'completed' && (
                    <CheckCircleIcon color="success" />
                  )}
                  {status === 'in-progress' && (
                    <CircularProgress size={24} />
                  )}
                  {status === 'pending' && (
                    <RadioButtonUncheckedIcon color="disabled" />
                  )}
                </ListItemIcon>
                <ListItemText
                  primary={step.label}
                  primaryTypographyProps={{
                    color: status === 'completed' ? 'text.primary' : 'text.secondary',
                    fontWeight: status === 'in-progress' ? 600 : 400,
                  }}
                />
              </ListItem>
            )
          })}
        </List>

        {/* Current Step */}
        {currentStep && (
          <Box
            sx={{
              mt: 3,
              p: 2,
              bgcolor: 'primary.light',
              borderRadius: 1,
              display: 'flex',
              alignItems: 'center',
            }}
          >
            <AutorenewIcon
              sx={{
                mr: 2,
                animation: 'spin 2s linear infinite',
                '@keyframes spin': {
                  '0%': {
                    transform: 'rotate(0deg)',
                  },
                  '100%': {
                    transform: 'rotate(360deg)',
                  },
                },
              }}
            />
            <Typography variant="body1">{currentStep}</Typography>
          </Box>
        )}

        {/* Cancel Button */}
        <Box sx={{ mt: 4, textAlign: 'center' }}>
          <Button variant="outlined" color="error" onClick={onCancel}>
            Cancel Analysis
          </Button>
        </Box>
      </Paper>
    </Box>
  )
}

export default AnalysisProgress

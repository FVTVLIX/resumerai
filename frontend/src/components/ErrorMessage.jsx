import {
  Box,
  Paper,
  Typography,
  Button,
  Alert,
} from '@mui/material'
import ErrorOutlineIcon from '@mui/icons-material/ErrorOutline'
import RefreshIcon from '@mui/icons-material/Refresh'

function ErrorMessage({ error, onRetry }) {
  return (
    <Box sx={{ maxWidth: 600, mx: 'auto', mt: 8 }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        <Box sx={{ textAlign: 'center' }}>
          <ErrorOutlineIcon
            sx={{ fontSize: 80, color: 'error.main', mb: 2 }}
          />
          <Typography variant="h4" gutterBottom>
            Oops! Something went wrong
          </Typography>
          <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
            We encountered an error while analyzing your resume.
          </Typography>
        </Box>

        <Alert severity="error" sx={{ mb: 3 }}>
          <strong>Error:</strong> {error || 'An unexpected error occurred'}
        </Alert>

        <Box sx={{ textAlign: 'center' }}>
          <Button
            variant="contained"
            size="large"
            startIcon={<RefreshIcon />}
            onClick={onRetry}
          >
            Try Again
          </Button>
        </Box>

        <Box sx={{ mt: 4, p: 2, bgcolor: 'grey.100', borderRadius: 1 }}>
          <Typography variant="subtitle2" gutterBottom>
            Common issues:
          </Typography>
          <Typography variant="body2" component="ul" sx={{ mt: 1, pl: 2 }}>
            <li>File size exceeds 5MB limit</li>
            <li>File is password-protected or encrypted</li>
            <li>File contains only images (scanned documents)</li>
            <li>Network connection issues</li>
            <li>Server temporarily unavailable</li>
          </Typography>
        </Box>
      </Paper>
    </Box>
  )
}

export default ErrorMessage

import { AppBar, Toolbar, Typography, Box } from '@mui/material'
import AssessmentIcon from '@mui/icons-material/Assessment'

function Header() {
  return (
    <AppBar position="static" elevation={2}>
      <Toolbar>
        <AssessmentIcon sx={{ mr: 2, fontSize: 32 }} />
        <Typography variant="h6" component="div" sx={{ flexGrow: 1, fontWeight: 600 }}>
          AI Resume Analyzer
        </Typography>
        <Box sx={{ display: { xs: 'none', md: 'block' } }}>
          <Typography variant="body2" color="inherit" sx={{ opacity: 0.8 }}>
            Powered by AI
          </Typography>
        </Box>
      </Toolbar>
    </AppBar>
  )
}

export default Header

import { useState } from 'react'
import {
  Box,
  Paper,
  Typography,
  Button,
  Grid,
  Card,
  CardContent,
  CircularProgress,
  Chip,
  List,
  ListItem,
  ListItemText,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Alert,
  LinearProgress,
  Divider,
} from '@mui/material'
import ExpandMoreIcon from '@mui/icons-material/ExpandMore'
import FileDownloadIcon from '@mui/icons-material/FileDownload'
import RefreshIcon from '@mui/icons-material/Refresh'
import {
  PieChart,
  Pie,
  Cell,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts'

const COLORS = ['#1976D2', '#42A5F5', '#64B5F6', '#90CAF9', '#BBDEFB']

const getScoreLabel = (score) => {
  if (score >= 90) return { label: 'Excellent', color: 'success' }
  if (score >= 75) return { label: 'Good', color: 'info' }
  if (score >= 60) return { label: 'Fair', color: 'warning' }
  return { label: 'Needs Work', color: 'error' }
}

const getPriorityColor = (priority) => {
  const colors = {
    high: 'error',
    medium: 'warning',
    low: 'success',
  }
  return colors[priority] || 'default'
}

const getPriorityIcon = (priority) => {
  const icons = {
    high: '🔴',
    medium: '🟡',
    low: '🟢',
  }
  return icons[priority] || '⚪'
}

function ResultsDashboard({ data, onNewAnalysis }) {
  const [expandedSuggestion, setExpandedSuggestion] = useState(null)

  const scoreInfo = getScoreLabel(data.overall_score)

  // Prepare skills data for charts
  const skillsData = Object.entries(data.skills.categories).map(([category, skills]) => ({
    name: category.replace(/_/g, ' ').replace(/\b\w/g, (l) => l.toUpperCase()),
    count: skills.length,
  }))

  // Prepare metrics data for charts
  const metricsData = [
    {
      name: 'Action Verbs',
      value: data.analysis.action_verb_usage * 100,
      color: '#1976D2',
    },
    {
      name: 'Quantification',
      value: data.analysis.quantification_rate * 100,
      color: '#42A5F5',
    },
    {
      name: 'ATS Score',
      value: data.ats_score,
      color: '#64B5F6',
    },
  ]

  const handleExport = () => {
    // Create a formatted JSON export
    const exportData = JSON.stringify(data, null, 2)
    const blob = new Blob([exportData], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `resume-analysis-${Date.now()}.json`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  return (
    <Box>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
        <Typography variant="h3">Your Resume Analysis</Typography>
        <Box>
          <Button
            variant="outlined"
            startIcon={<FileDownloadIcon />}
            onClick={handleExport}
            sx={{ mr: 2 }}
          >
            Export Results
          </Button>
          <Button
            variant="contained"
            startIcon={<RefreshIcon />}
            onClick={onNewAnalysis}
          >
            New Analysis
          </Button>
        </Box>
      </Box>

      {/* Overall Score */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={4}>
          <Card elevation={3}>
            <CardContent sx={{ textAlign: 'center', py: 4 }}>
              <Typography variant="h6" gutterBottom>
                Overall Score
              </Typography>
              <Box sx={{ position: 'relative', display: 'inline-flex', my: 2 }}>
                <CircularProgress
                  variant="determinate"
                  value={data.overall_score}
                  size={120}
                  thickness={5}
                  color={scoreInfo.color}
                />
                <Box
                  sx={{
                    top: 0,
                    left: 0,
                    bottom: 0,
                    right: 0,
                    position: 'absolute',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                  }}
                >
                  <Typography variant="h4" component="div">
                    {Math.round(data.overall_score)}
                  </Typography>
                </Box>
              </Box>
              <Chip label={scoreInfo.label} color={scoreInfo.color} size="large" />
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={8}>
          <Card elevation={3}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Resume Summary
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <Typography variant="body2" color="text.secondary">
                    Total Experience
                  </Typography>
                  <Typography variant="h6">
                    {data.analysis.total_experience_years} years
                  </Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="body2" color="text.secondary">
                    Skills Identified
                  </Typography>
                  <Typography variant="h6">
                    {data.skills.technical.length + data.skills.soft.length}
                  </Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="body2" color="text.secondary">
                    Education Entries
                  </Typography>
                  <Typography variant="h6">{data.education.length}</Typography>
                </Grid>
                <Grid item xs={6}>
                  <Typography variant="body2" color="text.secondary">
                    ATS Compatibility
                  </Typography>
                  <Typography variant="h6">{Math.round(data.ats_score)}/100</Typography>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* AI Suggestions */}
      <Paper elevation={2} sx={{ p: 3, mb: 4 }}>
        <Typography variant="h5" gutterBottom>
          AI-Powered Suggestions
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
          Prioritized recommendations to improve your resume
        </Typography>

        {data.ai_suggestions.length === 0 ? (
          <Alert severity="info">
            No suggestions available. Your resume looks great!
          </Alert>
        ) : (
          data.ai_suggestions.map((suggestion, index) => (
            <Accordion
              key={index}
              expanded={expandedSuggestion === index}
              onChange={() =>
                setExpandedSuggestion(expandedSuggestion === index ? null : index)
              }
              sx={{ mb: 1 }}
            >
              <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                <Box sx={{ display: 'flex', alignItems: 'center', width: '100%' }}>
                  <Typography sx={{ mr: 2 }}>
                    {getPriorityIcon(suggestion.priority)}
                  </Typography>
                  <Typography sx={{ flexGrow: 1 }}>{suggestion.suggestion}</Typography>
                  <Chip
                    label={suggestion.priority.toUpperCase()}
                    color={getPriorityColor(suggestion.priority)}
                    size="small"
                    sx={{ ml: 2 }}
                  />
                </Box>
              </AccordionSummary>
              <AccordionDetails>
                {suggestion.rationale && (
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                    <strong>Why this matters:</strong> {suggestion.rationale}
                  </Typography>
                )}
                {suggestion.examples && suggestion.examples.length > 0 && (
                  <Box>
                    <Typography variant="body2" fontWeight={600} gutterBottom>
                      Examples:
                    </Typography>
                    {suggestion.examples.map((example, idx) => (
                      <Typography
                        key={idx}
                        variant="body2"
                        sx={{
                          pl: 2,
                          py: 0.5,
                          fontFamily: 'monospace',
                          fontSize: '0.875rem',
                        }}
                      >
                        • {example}
                      </Typography>
                    ))}
                  </Box>
                )}
              </AccordionDetails>
            </Accordion>
          ))
        )}
      </Paper>

      {/* Skills Breakdown */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={6}>
          <Paper elevation={2} sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Skills by Category
            </Typography>
            {skillsData.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={skillsData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={(entry) => `${entry.name}: ${entry.count}`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="count"
                  >
                    {skillsData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <Typography variant="body2" color="text.secondary">
                No skills data available
              </Typography>
            )}
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper elevation={2} sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Content Analysis
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={metricsData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis domain={[0, 100]} />
                <Tooltip />
                <Bar dataKey="value" fill="#1976D2">
                  {metricsData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
      </Grid>

      {/* Skills Details */}
      <Paper elevation={2} sx={{ p: 3, mb: 4 }}>
        <Typography variant="h6" gutterBottom>
          Technical Skills
        </Typography>
        <Grid container spacing={1}>
          {data.skills.technical.slice(0, 20).map((skill, index) => (
            <Grid item key={index}>
              <Chip
                label={`${skill.name} (${skill.count})`}
                color="primary"
                variant="outlined"
                size="small"
              />
            </Grid>
          ))}
        </Grid>

        <Divider sx={{ my: 3 }} />

        <Typography variant="h6" gutterBottom>
          Soft Skills
        </Typography>
        <Grid container spacing={1}>
          {data.skills.soft.slice(0, 10).map((skill, index) => (
            <Grid item key={index}>
              <Chip
                label={`${skill.name} (${skill.count})`}
                color="secondary"
                variant="outlined"
                size="small"
              />
            </Grid>
          ))}
        </Grid>
      </Paper>

      {/* Experience Timeline */}
      {data.experience && data.experience.length > 0 && (
        <Paper elevation={2} sx={{ p: 3, mb: 4 }}>
          <Typography variant="h6" gutterBottom>
            Experience Timeline
          </Typography>
          <List>
            {data.experience.map((exp, index) => (
              <ListItem key={index} sx={{ flexDirection: 'column', alignItems: 'flex-start' }}>
                <Box sx={{ width: '100%' }}>
                  <Typography variant="subtitle1" fontWeight={600}>
                    {exp.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {exp.company} • {exp.start_date} - {exp.end_date}{' '}
                    {exp.duration_months && `(${exp.duration_months} months)`}
                  </Typography>
                  {exp.responsibilities && exp.responsibilities.length > 0 && (
                    <List dense>
                      {exp.responsibilities.slice(0, 3).map((resp, idx) => (
                        <ListItem key={idx} sx={{ py: 0.5 }}>
                          <ListItemText
                            primary={`• ${resp}`}
                            primaryTypographyProps={{ variant: 'body2' }}
                          />
                        </ListItem>
                      ))}
                    </List>
                  )}
                </Box>
                {index < data.experience.length - 1 && <Divider sx={{ width: '100%', mt: 2 }} />}
              </ListItem>
            ))}
          </List>
        </Paper>
      )}

      {/* ATS Recommendations */}
      {data.ats_recommendations && data.ats_recommendations.length > 0 && (
        <Paper elevation={2} sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>
            ATS Optimization Tips
          </Typography>
          <List>
            {data.ats_recommendations.map((rec, index) => (
              <ListItem key={index}>
                <ListItemText
                  primary={`• ${rec}`}
                  primaryTypographyProps={{ variant: 'body2' }}
                />
              </ListItem>
            ))}
          </List>
        </Paper>
      )}
    </Box>
  )
}

export default ResultsDashboard

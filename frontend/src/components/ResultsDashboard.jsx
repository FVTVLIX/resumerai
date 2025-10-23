import { useState } from 'react'
import { Download, RefreshCw, ChevronDown } from 'lucide-react'
import { Button } from './ui/button'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from './ui/card'
import { Badge } from './ui/badge'
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from './ui/accordion'
import { Alert, AlertDescription } from './ui/alert'
import { Progress } from './ui/progress'
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

const COLORS = ['#0EA5E9', '#3B82F6', '#6366F1', '#8B5CF6', '#A855F7']

const getScoreLabel = (score) => {
  if (score >= 90) return { label: 'Excellent', variant: 'default' }
  if (score >= 75) return { label: 'Good', variant: 'secondary' }
  if (score >= 60) return { label: 'Fair', variant: 'outline' }
  return { label: 'Needs Work', variant: 'destructive' }
}

const getPriorityVariant = (priority) => {
  const variants = {
    high: 'destructive',
    medium: 'outline',
    low: 'secondary',
  }
  return variants[priority] || 'default'
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
      color: '#0EA5E9',
    },
    {
      name: 'Quantification',
      value: data.analysis.quantification_rate * 100,
      color: '#3B82F6',
    },
    {
      name: 'ATS Score',
      value: data.ats_score,
      color: '#6366F1',
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
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h2 className="text-3xl font-bold tracking-tight">Your Resume Analysis</h2>
        <div className="flex gap-2">
          <Button variant="outline" onClick={handleExport}>
            <Download className="mr-2 h-4 w-4" />
            Export Results
          </Button>
          <Button onClick={onNewAnalysis}>
            <RefreshCw className="mr-2 h-4 w-4" />
            New Analysis
          </Button>
        </div>
      </div>

      {/* Overall Score */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="md:col-span-1">
          <CardContent className="text-center pt-8 pb-8">
            <h3 className="text-lg font-semibold mb-4">Overall Score</h3>
            <div className="relative inline-flex items-center justify-center my-4">
              <svg className="w-32 h-32 transform -rotate-90">
                <circle
                  cx="64"
                  cy="64"
                  r="56"
                  stroke="currentColor"
                  strokeWidth="8"
                  fill="none"
                  className="text-muted"
                />
                <circle
                  cx="64"
                  cy="64"
                  r="56"
                  stroke="currentColor"
                  strokeWidth="8"
                  fill="none"
                  strokeDasharray={`${(data.overall_score / 100) * 351.86} 351.86`}
                  className="text-primary transition-all duration-1000"
                />
              </svg>
              <div className="absolute">
                <span className="text-4xl font-bold">{Math.round(data.overall_score)}</span>
              </div>
            </div>
            <Badge variant={scoreInfo.variant} className="text-base px-4 py-1">
              {scoreInfo.label}
            </Badge>
          </CardContent>
        </Card>

        <Card className="md:col-span-2">
          <CardContent className="pt-6">
            <h3 className="text-lg font-semibold mb-4">Resume Summary</h3>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-sm text-muted-foreground">Total Experience</p>
                <p className="text-2xl font-semibold">{data.analysis.total_experience_years} years</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Skills Identified</p>
                <p className="text-2xl font-semibold">
                  {data.skills.technical.length + data.skills.soft.length}
                </p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Education Entries</p>
                <p className="text-2xl font-semibold">{data.education.length}</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">ATS Compatibility</p>
                <p className="text-2xl font-semibold">{Math.round(data.ats_score)}/100</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* AI Suggestions */}
      <Card>
        <CardHeader>
          <CardTitle>AI-Powered Suggestions</CardTitle>
          <CardDescription>Prioritized recommendations to improve your resume</CardDescription>
        </CardHeader>
        <CardContent>
          {data.ai_suggestions.length === 0 ? (
            <Alert>
              <AlertDescription>
                No suggestions available. Your resume looks great!
              </AlertDescription>
            </Alert>
          ) : (
            <Accordion type="single" collapsible>
              {data.ai_suggestions.map((suggestion, index) => (
                <AccordionItem key={index} value={`item-${index}`}>
                  <AccordionTrigger className="hover:no-underline">
                    <div className="flex items-center gap-3 flex-1 text-left">
                      <span className="text-lg">{getPriorityIcon(suggestion.priority)}</span>
                      <span className="flex-1">{suggestion.suggestion}</span>
                      <Badge variant={getPriorityVariant(suggestion.priority)} className="ml-2">
                        {suggestion.priority.toUpperCase()}
                      </Badge>
                    </div>
                  </AccordionTrigger>
                  <AccordionContent>
                    {suggestion.rationale && (
                      <p className="text-sm text-muted-foreground mb-3">
                        <strong>Why this matters:</strong> {suggestion.rationale}
                      </p>
                    )}
                    {suggestion.examples && suggestion.examples.length > 0 && (
                      <div>
                        <p className="text-sm font-semibold mb-2">Examples:</p>
                        <ul className="space-y-1">
                          {suggestion.examples.map((example, idx) => (
                            <li key={idx} className="text-sm font-mono pl-4">
                              • {example}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </AccordionContent>
                </AccordionItem>
              ))}
            </Accordion>
          )}
        </CardContent>
      </Card>

      {/* Skills Breakdown */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Skills by Category</CardTitle>
          </CardHeader>
          <CardContent>
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
              <p className="text-sm text-muted-foreground">No skills data available</p>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Content Analysis</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={metricsData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis domain={[0, 100]} />
                <Tooltip />
                <Bar dataKey="value" fill="#0EA5E9">
                  {metricsData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Skills Details */}
      <Card>
        <CardContent className="pt-6">
          <h3 className="text-lg font-semibold mb-3">Technical Skills</h3>
          <div className="flex flex-wrap gap-2">
            {data.skills.technical.slice(0, 20).map((skill, index) => (
              <Badge key={index} variant="outline">
                {skill.name} ({skill.count})
              </Badge>
            ))}
          </div>

          <hr className="my-6 border-border" />

          <h3 className="text-lg font-semibold mb-3">Soft Skills</h3>
          <div className="flex flex-wrap gap-2">
            {data.skills.soft.slice(0, 10).map((skill, index) => (
              <Badge key={index} variant="secondary">
                {skill.name} ({skill.count})
              </Badge>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Experience Timeline */}
      {data.experience && data.experience.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Experience Timeline</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-6">
              {data.experience.map((exp, index) => (
                <div key={index}>
                  <div className="space-y-1">
                    <h4 className="font-semibold text-base">{exp.title}</h4>
                    <p className="text-sm text-muted-foreground">
                      {exp.company} • {exp.start_date} - {exp.end_date}{' '}
                      {exp.duration_months && `(${exp.duration_months} months)`}
                    </p>
                    {exp.responsibilities && exp.responsibilities.length > 0 && (
                      <ul className="mt-2 space-y-1">
                        {exp.responsibilities.slice(0, 3).map((resp, idx) => (
                          <li key={idx} className="text-sm ml-4">
                            • {resp}
                          </li>
                        ))}
                      </ul>
                    )}
                  </div>
                  {index < data.experience.length - 1 && <hr className="mt-4 border-border" />}
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* ATS Recommendations */}
      {data.ats_recommendations && data.ats_recommendations.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>ATS Optimization Tips</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-2">
              {data.ats_recommendations.map((rec, index) => (
                <li key={index} className="text-sm">
                  • {rec}
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      )}
    </div>
  )
}

export default ResultsDashboard

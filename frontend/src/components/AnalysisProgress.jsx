import { CheckCircle, Circle, Loader2 } from 'lucide-react'
import { Button } from './ui/button'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from './ui/card'
import { Progress } from './ui/progress'

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
    <div className="max-w-3xl mx-auto mt-8">
      <Card>
        <CardHeader className="text-center">
          <CardTitle className="text-3xl">Analyzing Your Resume...</CardTitle>
          <CardDescription className="text-base">
            This usually takes 10-15 seconds...
          </CardDescription>
        </CardHeader>

        <CardContent className="space-y-6">
          {/* Progress Bar */}
          <div className="space-y-2">
            <div className="flex items-center gap-3">
              <Progress value={progress} className="flex-1" />
              <span className="text-sm text-muted-foreground min-w-[3rem] text-right">
                {Math.round(progress)}%
              </span>
            </div>
          </div>

          {/* Steps List */}
          <ul className="space-y-3">
            {steps.map((step) => {
              const status = getStepStatus(step.threshold)
              return (
                <li key={step.id} className="flex items-center gap-3">
                  <div className="flex-shrink-0">
                    {status === 'completed' && (
                      <CheckCircle className="h-6 w-6 text-green-600" />
                    )}
                    {status === 'in-progress' && (
                      <Loader2 className="h-6 w-6 text-primary animate-spin" />
                    )}
                    {status === 'pending' && (
                      <Circle className="h-6 w-6 text-muted-foreground" />
                    )}
                  </div>
                  <span
                    className={`
                      ${status === 'completed' ? 'text-foreground' : 'text-muted-foreground'}
                      ${status === 'in-progress' ? 'font-semibold' : 'font-normal'}
                    `}
                  >
                    {step.label}
                  </span>
                </li>
              )
            })}
          </ul>

          {/* Current Step */}
          {currentStep && (
            <div className="mt-4 p-3 bg-primary/10 rounded-lg flex items-center gap-3">
              <Loader2 className="h-5 w-5 text-primary animate-spin" />
              <p className="text-sm font-medium">{currentStep}</p>
            </div>
          )}

          {/* Cancel Button */}
          <div className="mt-6 text-center">
            <Button variant="destructive" onClick={onCancel}>
              Cancel Analysis
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default AnalysisProgress

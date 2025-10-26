import { AlertCircle, RefreshCw } from 'lucide-react'
import { Button } from './ui/button'
import { Card, CardContent } from './ui/card'
import { Alert, AlertDescription } from './ui/alert'

function ErrorMessage({ error, onRetry }) {
  return (
    <div className="max-w-2xl mx-auto mt-8">
      <Card>
        <CardContent className="pt-8 pb-8">
          <div className="text-center">
            <AlertCircle className="mx-auto h-20 w-20 text-destructive mb-4" />
            <h2 className="text-3xl font-bold mb-2">Oops! Something went wrong</h2>
            <p className="text-muted-foreground mb-6">
              We encountered an error while analyzing your resume.
            </p>
          </div>

          <Alert variant="destructive" className="mb-6">
            <AlertDescription>
              <strong>Error:</strong> {error || 'An unexpected error occurred'}
            </AlertDescription>
          </Alert>

          <div className="text-center mb-6">
            <Button size="lg" onClick={onRetry}>
              <RefreshCw className="mr-2 h-4 w-4" />
              Try Again
            </Button>
          </div>

          <div className="mt-6 p-4 bg-muted rounded-lg">
            <h3 className="text-sm font-semibold mb-2">Common issues:</h3>
            <ul className="text-sm space-y-1 ml-4">
              <li>File size exceeds 5MB limit</li>
              <li>File is password-protected or encrypted</li>
              <li>File contains only images (scanned documents)</li>
              <li>Network connection issues</li>
              <li>Server temporarily unavailable</li>
            </ul>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default ErrorMessage

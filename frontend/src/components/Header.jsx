import { FileText } from 'lucide-react'

function Header() {
  return (
    <header className="border-b bg-primary text-primary-foreground">
      <div className="container mx-auto px-4">
        <div className="flex h-16 items-center justify-between">
          <div className="flex items-center gap-3">
            <FileText className="h-8 w-8" />
            <h1 className="text-xl font-semibold">AI Resume Analyzer</h1>
          </div>
          <div className="hidden md:block">
            <p className="text-sm opacity-90">Powered by AI</p>
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header
